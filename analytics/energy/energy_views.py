import os
import re
import urllib2
import json
from datetime import datetime
import numpy as np
import pandas as ps
from dateutil.parser import parse
from scipy.optimize import curve_fit
from scipy.interpolate import spline
from energy_time_series import *

PATH = os.path.dirname(os.path.realpath(__file__))


class EnergyViews(object):
    """
    Simple municipal energy use analytics for visualization
    """
    def __init__(self, url, basetemps=(60, 55), source='CSV'):
        '''
        Initialize
        - read in energy data (locally cached or from API url)
        - note baseload tempratures (i.e. when energy is not used for heating or cooling)
        - tabulate usage data into separate gas and power datasets

        :param url: URL to raw data API
        :param basetemps: baseload tempratures (gas, power)
        '''
        assert(source in ('API', 'CSV', 'cache'))

        if source == 'cache':
            loc = '{0}/../data/Energy.json'.format(PATH)
            if os.path.exists(loc):
                with open('{0}/../data/Energy.json'.format(PATH)) as f:
                    txt = f.read()

        elif source == 'API':
            req = urllib2.Request(url)
            txt = urllib2.urlopen(req).read()
            with open('{0}/../data/Energy.json'.format(PATH), 'w') as f:
                f.write(txt)

        if source in ('API', 'cache'):
            #
            # parse JSON and convert strings to dates and numeric types
            #
            jsn = json.loads(txt)
            self.data = ps.DataFrame(jsn)
            self.data['read_date'] = self.data['read_date'].map(parse)
            self.data['electric_billed'] = self.data['electric_billed'].map(float)
            self.data['electric_customer'] = self.data['electric_customer'].map(float)
            self.data['gas_billed'] = self.data['gas_billed'].map(lambda x: float(x) if x else np.NaN)
            self.data['gas_customer'] = self.data['gas_customer'].map(lambda x: float(x) if x else np.NaN)

        if source == 'CSV':
            loc = '{0}/../data/Energy.csv'.format(PATH)
            exp = re.compile(r'[A-Z]|[a-z]|,')
            self.data = ps.DataFrame.from_csv(loc).reset_index()
            self.data['electric_billed'] = self.data['electric_billed'].map(
                lambda x: float(re.sub(exp, '', x)))
            self.data['electric_customer'] = self.data['electric_customer'].map(
                lambda x: float(re.sub(exp, '', x)))
            self.data['gas_billed'] = self.data['gas_billed'].map(
                lambda x: float(re.sub(exp, '', x)) if ps.notnull(x) and x else np.NaN)
            self.data['gas_customer'] = self.data['gas_customer'].map(
                lambda x: float(re.sub(exp, '', x)) if ps.notnull(x) and x else np.NaN)

        #
        # tabulate data and run regressions over heating and cooling/cooking tempratures
        #
        self.crosstab_ener(basetemps)
        self.unstack_temp()

    def crosstab_ener(self, basetemps=(60, 70)):
        '''
        Cross-tabulate gas and power usage and meter counts by
            date x [business_class, city_code]
        '''
        #
        # gas
        #
        gas_usage = ps.pivot_table(
            self.data,
            index='read_date',
            columns=['city_code', 'business_class'],
            values='gas_billed',
            aggfunc=np.sum)
        gas_users = ps.pivot_table(
            self.data,
            index='read_date',
            columns=['city_code', 'business_class'],
            values='gas_customer',
            aggfunc=np.sum)
        self.gas = EnergyTimeSeries(gas_usage, gas_users, basetemps[0], 1.0)
        #
        # electricity
        #
        pwr_usage = ps.pivot_table(
            self.data,
            index='read_date',
            columns=['city_code', 'business_class'],
            values='electric_billed',
            aggfunc=np.sum)
        pwr_users = ps.pivot_table(
            self.data,
            index='read_date',
            columns=['city_code', 'business_class'],
            values='electric_customer',
            aggfunc=np.sum)
        self.pwr = EnergyTimeSeries(pwr_usage, pwr_users, basetemps[1], 1000.0)
        #
        # all tables should have identical date indexing
        #
        assert(all(gas_usage.index == pwr_usage.index))
        assert(all(gas_users.index == pwr_users.index))
        assert(all(gas_usage.index == pwr_users.index))
        self.tz = gas_usage.index.tz

    def unstack_temp(self):
        '''
        Read in heating/cooling degree day data and average monthly
        temprature for each month reindex to retain only months for
        which energy use data exists
        '''
        path = '{0}/../data/DegreeDays.csv'.format(PATH)
        self.degd = ps.DataFrame.from_csv(path, parse_dates=True)
        self.degd['date'] = self.degd['date'].map(parse)
        self.degd = self.degd.set_index('date')
        self.degd.index.tz = self.tz

        path = '{0}/../data/Temprature.csv'.format(PATH)
        temp = ps.DataFrame.from_csv(path)
        rows = []
        for ix, row in temp.iterrows():
            year = int(row.YEAR)
            for mth in row.index[1:13]:
                rows.append(('1/{0}/{1}'.format(mth, year), float(row[mth])))
        self.temp = ps.DataFrame(rows, columns=['date', 'temp'])
        self.temp['date'] = self.temp['date'].map(parse)
        self.temp = self.temp.set_index('date')
        self.temp.index.tz = self.tz

    def dd_plot(self):
        data = ps.merge(self.temp, self.degd, left_index=True, right_index=True, how='inner')

        hdd = data[ps.notnull(data['HDD'])]
        cdd = data[ps.notnull(data['CDD'])]

        hday = hdd[hdd['temp'] < 60]
        cday = cdd[cdd['temp'] > 55]

        mH, cH, r_sqrH = regress(hday['temp'], hday['HDD'])
        mC, cC, r_sqrC = regress(cday['temp'], cday['CDD'])

        print 'HDD = {1} + {0} * temp (R Sq. = {2})'.format(mH, cH, r_sqrH)
        print 'CDD = {1} + {0} * temp (R Sq. = {2})'.format(mC, cC, r_sqrC)

        xH = hday['temp']
        xC = cday['temp']

        vs_temp = ps.DataFrame(
            {'temp': hdd['temp'], 'hdd scatter': hdd['HDD']}
        ).merge(
            ps.DataFrame({'temp': cdd['temp'], 'cdd scatter': cdd['CDD']}),
            on='temp', how='outer', suffixes=('', '')
        ).merge(
            ps.DataFrame({'temp': xH, 'hdd regression': line(xH, mH, cH)}),
            on='temp', how='outer', suffixes=('', '')
        ).merge(
            ps.DataFrame({'temp': xC, 'cdd regression': line(xC, mC, cC)}),
            on='temp', how='outer', suffixes=('', ''))

        data = data.fillna(0)
        vs_time = ps.DataFrame({
            'time': data.index,
            'HDD': data['HDD'],
            'CDD': data['CDD']})

        return vs_temp.set_index('temp'), vs_time.set_index('time')

    def plots(self, what, city_code, business_class, per_meter):
        assert(what in ('gas', 'pwr'))
        return getattr(self, what).plots(
            self.temp, city_code, business_class, per_meter)

    def acorr(self, what, city_code, business_class):
        assert(what in ('gas', 'pwr'))
        return getattr(self, what).acorr(city_code, business_class)

    def sa_plot(self, what, city_code, business_class, per_meter):
        assert(what in ('gas', 'pwr'))
        return getattr(self, what).sa_plot(12, city_code, business_class, per_meter)

    def model(self, what, city_code, business_class, per_meter):
        assert(what in ('gas', 'pwr'))
        return getattr(self, what).model(self.degd, city_code, business_class, per_meter)
