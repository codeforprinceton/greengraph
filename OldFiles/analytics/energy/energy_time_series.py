import os
import urllib2
import json
from datetime import datetime, timedelta
import numpy as np
import pandas as ps
from dateutil.parser import parse
from scipy.optimize import curve_fit
from scipy.interpolate import spline

PATH = os.path.dirname(os.path.realpath(__file__))
BASEDATE = datetime(1700, 1, 1)

def line(x, m, c):
    '''
    Equation of a line, for showing regressions to temperature

    :param x: temperature value
    :param m: slope of regression line
    :param c: intercept
    :return: estmated energy usage
    '''
    return m * x + c

def biline(h, c, b, mH, mC):
    '''
    Bivariate line, for showing regression to heating / cooling days

    :param h: heating degree days
    :param c: cooling degree days
    :param b: baseload
    :param xH: coeff of heating degree days
    :param xC: coeff of cooling degree days
    :return: estmated energy usage
    '''
    return b + h * mH + c * mC

class EnergyTimeSeries(object):
    """
    Energy usage data
    TODO: smooth spikes caused by estimated observations
    TODO: compute seasonally adjusted time series
    """
    def __init__(self, usage, users, basetemp, scale):
        '''
        Initialize (note provided values)

        :param usage: usage data time series
        :param users: number of meters
        :param basetemp: baseload temperature
        :param scale: units divisor for usage values
        '''
        self.usage = usage / scale
        self.users = users
        self.basetemp = basetemp
        self.scale = scale

    def select(self, city_code, business_class, per_meter):
        '''
        Select subset of data for the given business class & city_code.
        Add up usage and meter counts for given business classes

        :param city_code: 'PRINCETON TWP' or 'PRINCETON BORO'
        :param business_class: a single business_class or a collection thereof
            - if a collection is given, the values are summed up
        :return: selected column
        '''
        if isinstance(business_class, basestring):
            usage = self.usage[city_code][business_class]
            users = self.users[city_code][business_class]
        else:
            usage = self.usage[city_code][business_class[0]]
            users = self.users[city_code][business_class[0]]
            for b in business_class[1:]:
                if self.usage[city_code][b].dropna().shape[0] > 0:
                    usage += self.usage[city_code][b].dropna()
                if self.users[city_code][b].dropna().shape[0] > 0:
                    users += self.users[city_code][b].dropna()
        data = usage / users if per_meter else usage
        data.name = 'usage'
        return data

    def acorr(self, city_code, business_class):
        '''
        Return autocorrelation plots for lags 1 - 12 for a energy usage series.
        Per-meter and aggregate data will have the same seasonal characteristics,
        so per-meter plotting is not supported.

        :param city_code: 'PRINCETON TWP' or 'PRINCETON BORO'
        :param business_class: a single business_class or a collection thereof
            - if a collection is given, the values are summed up
        :return: correlation values of data with itself at 1-12 sample lags
        '''
        data = self.select(city_code, business_class, per_meter=True)
        #
        # compute autocorrelation coeffients at lags of 1 to 12 mths
        #
        autocorr = []
        lag_0_mean, lag_0_var = data.mean(), data.var()
        lag_0_residual = data - lag_0_mean
        for k in range(1, 13):
            lag_k_residual = data.shift(k) - lag_0_mean
            num = (lag_0_residual * lag_k_residual).sum()
            den = lag_0_var * data.shape[0]
            autocorr.append((k, num / den))

        return ps.Series(dict(autocorr))

    def plots(self, temp, city_code, business_class, per_meter):
        '''
        Regress measured usage to temperatures in cold and hot months and
        generate x- and y-vectors for plotting this data set

        :param temp: temperature time series to regress to
        :param city_code: 'PRINCETON TWP' or 'PRINCETON BORO'
        :param business_class: a single business_class or a collection thereof
            - if a collection is given, the values are summed up
        :param per_meter: True for consumption per meter, False for aggregate
        :return: frame containing scatterplot and regression lines to temperature
        '''
        data = self.select(city_code, business_class, per_meter)
        #
        # split monthly average temperature series into two:
        # cool => samples when temps are cool basetemp
        # warm => samples when temps are warm basetemp
        # use the full time period over which any usage data exists
        #
        temp = temp.ix[self.usage.index]['temp']
        cool = temp[temp <  self.basetemp]
        warm = temp[temp >= self.basetemp]
        #
        # regress separately for cool and warm months
        #
        model = ps.ols(x=cool, y=data[cool.index])
        m_cool, c_cool = model.beta.x, model.beta.intercept
        model = ps.ols(x=warm, y=data[warm.index])
        m_warm, c_warm = model.beta.x, model.beta.intercept

        vs_temp = ps.DataFrame(
            {'temp': temp, 'scatter': data[temp.index]}
        ).merge(
            ps.DataFrame(
                {'temp': cool, 'heating regression': line(cool, m_cool, c_cool)}),
            on='temp', how='outer', suffixes=('', '')
        ).merge(
            ps.DataFrame(
                {'temp': warm, 'cooling regression': line(warm, m_warm, c_warm)}),
            on='temp', how='outer', suffixes=('', ''))

        vs_time = data
        return vs_temp.set_index('temp'), vs_time

    def sa_plot(self, period, city_code, business_class, per_meter):
        '''
        Compute seasonally adjusted time series using a simple subtraction of
        deviations from means averaged for each seasonal interval

        :param period: freq in months (3, 6, 12)
            => (monthly, semi, quarterly, annual)
        :param city_code: 'PRINCETON TWP' or 'PRINCETON BORO'
        :param business_class: a single business_class or a collection thereof
            - if a collection is given, the values are summed up
        :param per_meter: True for consumption per meter, False for aggregate
        :return: frame containing raw data and its decomposition
        '''
        assert(period in (3, 6, 12))
        data = self.select(city_code, business_class, per_meter)
        #
        # index by date, add a column for residual and one for group label
        #
        grouper = lambda date: date.month % period
        labeled = ps.DataFrame({'date': data.index,
                                'data': data,
                                'residual': data - data.mean(),
                                'group': data.index.map(grouper)})
        #
        # get seasonal adjustment factor
        #
        factors = labeled.groupby('group').mean().rename(
            columns={'residual': 'adjustment'}
        ).reindex(columns=['adjustment'])
        #
        # apply seasonal adjustment
        #
        df = ps.merge(labeled,
                      factors,
                      left_on='group',
                      right_index=True,
                      how='inner',
                      suffixes=('', ''))
        df['adjusted'] = df['data'] - df['adjustment']
        #
        # decompose variation
        #
        factors = labeled.groupby('group').mean().rename(
            columns={'data': 'varadj'}
        ).reindex(columns=['varadj'])
        #
        # correspondence
        #
        df = ps.merge(df,
                      factors,
                      left_on='group',
                      right_index=True,
                      how='inner',
                      suffixes=('', ''))
        df['variation'] = df['data'] - df['varadj']
        df = df.set_index('date')
        return df.reindex(columns=[
            'data', 'adjustment', 'variation', 'adjusted'
        ])

    def model(self, dd, city_code, business_class, per_meter):
        '''
        Regress usage data to heating and cooling degree days

        :param dd: heating and cooling degree days
        :param city_code: 'PRINCETON TWP' or 'PRINCETON BORO'
        :param business_class: a single business_class or a collection thereof
            - if a collection is given, the values are summed up
        :param per_meter: True for consumption per meter, False for aggregate
        :return: series of first differences
        '''
        data = ps.DataFrame(self.select(city_code, business_class, per_meter))
        data['year'] = data.index.map(lambda d: d.year)
        data = data[data['year'] > 2009]['usage']
        #
        # index degree days frame for correspondence to usage data
        #
        dd = dd.ix[data.index].fillna(0.0)
        #
        # regress to heating and cooling degree days
        #
        model = ps.ols(x=dd, y=data)
        print city_code, business_class, per_meter
        print model
        print '-' * 60
        return model.beta.intercept, model.beta.HDD, model.beta.CDD
