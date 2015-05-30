import os
import urllib2
import json
import numpy as np
import pandas as ps
from dateutil.parser import parse
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

PATH = os.path.dirname(os.path.realpath(__file__))

def line(x, m, c):
    '''
    Equation of a line, for regressions to temprature

    :param x: temprature value
    :param m: slope of regression line
    :param c: intercept
    :return: estmated energy usage
    '''
    return m * x + c


def regress(x, y):
    '''
    Compute line coefficients, uncertainty and R-Squared

    :param x: x values (np.array or Series)
    :param y: y values (np.array or Series)
    :return: slope, intercept, r-square
    '''
    y = y.dropna()
    x = x.ix[y.index]
    if y.shape[0] > 0:
        (m, c), cov = curve_fit(line, x, y)
        err = y - line(x, m, c)
        sqr_err = (err * err).sum()
        dev = y - y.mean()
        sqr_dev = (dev * dev).sum()
        r_sqr = 1.0 - sqr_err / sqr_dev
        return m, c, r_sqr
    else:
        return np.NaN, np.NaN, np.NaN

class EnergyData(object):
    """
    Energy usage data
    TODO: smooth spikes caused by estimated observations
    TODO: compute seasonally adjusted time series
    """
    def __init__(self, usage, users, basetemp):
        '''
        Initialize (note provided values)

        :param usage: usage data time series
        :param users: number of meters
        :param basetemp: baseload temprature
        '''
        self.usage = usage
        self.users = users
        self.basetemp = basetemp

    def plots(self, temp, city_code, business_class, per_meter, scale=1.0):
        '''
        Regress measured usage to tempratures in cold and hot months and
        generate x- and y-vectors for plotting this data set

        :param temp: temprature time series to regress to
        :param business_class: a single business_class or a collection thereof
            - if a collection is given, the values are summed up
        :param city_code: 'PRINCETON TWP' or 'PRINCETON BORO'
        :param per_meter: True for consumption per meter, False for aggregate
        :param scale: Divisor for values
        :return: a dictionary with the following entries:
            - 'ln_cool' => (x-vector, y-vector) - cold months regression line
            - 'ln_warm' => (x-vector, y-vector) -  warm months regression line
            - 'scatter' => (x-vector, y-vector) - scatterplot of samples vs temprature
            - 'ln_time' => (x-vector, y-vector) - time plot of samples
        '''
        #
        # split monthly average temprature series into two:
        # cool => samples when temps are cool basetemp
        # warm => samples when temps are warm basetemp
        #
        temp = temp.ix[self.usage.index]['temp']
        cool = temp[temp <  self.basetemp]
        warm = temp[temp >= self.basetemp]
        #
        # select subset of data for the given business class & city_code
        # add up usage and meter counts for given business classes
        #
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
        data = data / scale
        m_cool, c_cool, rsqr_cool = regress(cool, data[cool.index])
        m_warm, c_warm, rsqr_warm = regress(warm, data[warm.index])
        # print rsqr_cool, rsqr_warm

        return {
            'ln_time': data,
            'ln_cool': (cool, line(cool, m_cool, c_cool)),
            'ln_warm': (warm, line(warm, m_warm, c_warm)),
            'scatter': (temp, data[temp.index]),
        }


class EnergyViews(object):
    """
    Simple municipal energy use analytics for visualization
    """
    def __init__(self, url, basetemps=(70, 60), force=False):
        '''
        Initialize
        - read in energy data (locally cached or from API url)
        - note baseload tempratures (i.e. when energy is not used for heating or cooling)
        - tabulate usage data into separate gas and power datasets

        :param url: URL to raw data API
        :param basetemps: baseload tempratures (gas, power)
        '''
        loc = '{0}/../data/Energy.json'.format(PATH)
        #
        # Use locally cached copy of data if one was saved
        # previously and force=False
        #
        if not force and os.path.exists(loc):
            with open('{0}/../data/Energy.json'.format(PATH)) as f:
                txt = f.read()
        #
        # Otherwise fetch data from the API url
        #
        else:
            req = urllib2.Request(url)
            txt = urllib2.urlopen(req).read()
            with open('{0}/../data/Energy.json'.format(PATH), 'w') as f:
                f.write(txt)
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
        self.gas = EnergyData(gas_usage, gas_users, basetemps[0])
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
        self.pwr = EnergyData(pwr_usage, pwr_users, basetemps[1])
        #
        # all tables should have identical date indexing
        #
        assert(all(gas_usage.index == pwr_usage.index))
        assert(all(gas_users.index == pwr_users.index))
        assert(all(gas_usage.index == pwr_users.index))

    def unstack_temp(self):
        '''
        Read in average monthly temprature for each month
        Reindex to retain only months for which energy use data exists
        '''
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

    def plots(self, what, city_code, business_class, per_meter, scale=1000.0):
        assert(what in ('gas', 'pwr'))
        return getattr(self, what).plots(
            self.temp, city_code, business_class, per_meter, scale)

def draw_quad(views, what, label, units, scale, business_class):
    fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(2, 2)
    plt.subplots_adjust(left=0.05, right=0.95, top=0.90, bottom=0.05, hspace=0.50)
    if isinstance(business_class, basestring):
        title = business_class
    else:
        title = ' + '.join(business_class)
    fig.suptitle('{0} Consumption: {1}'.format(label, title), fontsize=14)
    #
    # Town gas consumption - aggregate
    #
    plots = views.plots(
        what,
        'PRINCETON TWP',
        business_class,
        per_meter=False,
        scale=scale * 1000.0)
    plots['ln_time'].plot(ax=ax0,  c=COLOR_TOWN)
    ax1.plot(*plots['ln_cool'],  c='r', alpha=0.5)
    ax1.plot(*plots['ln_warm'],  c='k', alpha=0.5)
    ax1.scatter(*plots['scatter'], c=COLOR_TOWN, alpha=0.75, marker='s')
    #
    # Boro gas consumption - aggregate
    #
    plots = views.plots(
        what,
        'PRINCETON BORO',
        business_class,
        per_meter=False,
        scale=scale * 1000.0)
    plots['ln_time'].plot(ax=ax0, c=COLOR_BORO)
    ax1.plot(*plots['ln_cool'],  c='r', alpha=0.5)
    ax1.plot(*plots['ln_warm'],  c='k', alpha=0.5)
    ax1.scatter(*plots['scatter'], c=COLOR_BORO, marker='s')
    #
    # Town gas consumption - per meter
    #
    plots = views.plots(
        what,
        'PRINCETON TWP',
        business_class,
        per_meter=True,
        scale=scale)
    plots['ln_time'].plot(ax=ax2,  c=COLOR_TOWN)
    ax3.plot(*plots['ln_cool'],  c='r', alpha=0.5)
    ax3.plot(*plots['ln_warm'],  c='k', alpha=0.5)
    ax3.scatter(*plots['scatter'], c=COLOR_TOWN, alpha=0.75, marker='s')
    #
    # Boro gas consumption - per meter
    #
    plots = views.plots(
        what,
        'PRINCETON BORO',
        business_class,
        per_meter=True,
        scale=scale)
    plots['ln_time'].plot(ax=ax2, c=COLOR_BORO)
    ax3.plot(*plots['ln_cool'],  c='r', alpha=0.5)
    ax3.plot(*plots['ln_warm'],  c='k', alpha=0.5)
    ax3.scatter(*plots['scatter'], c=COLOR_BORO, marker='s')
    #
    # decoration
    #
    ax0.set_title('Total Usage', fontsize=12)
    ax0.set_ylabel('{0} (thousands)'.format(units), fontsize=12)
    ax0.set_xlabel('')
    patches, labels = ax0.get_legend_handles_labels()
    ax0.legend(patches,
               ['Town', 'Borough'],
               bbox_to_anchor=(0., -0.25, 1., .102),
               ncol=2,
               mode='expand',
               borderaxespad=0.)
    ax1.set_title('Total Usage vs Temp.', fontsize=12)
    ax1.set_xlabel('degrees F', fontsize=12)
    xmin, xmax = ax1.get_xlim()
    ax1.set_xlim(25., 80.)

    ax2.set_title('Avg. Usage / Meter', fontsize=12)
    ax2.set_ylabel('{0}'.format(units), fontsize=12)
    ax2.set_xlabel('')
    ax3.set_title('Avg. Usage / Meter vs Temp.', fontsize=12)
    xmin, xmax = ax3.get_xlim()
    ax3.set_xlim(25., 80.)

    fig.set_size_inches(17.07, 8.19)
    return fig

if __name__ == '__main__':
    COLOR_TOWN = '#01DF01'
    COLOR_BORO = '#FF4000'
    views = EnergyViews('http://slacker87.koding.io:3000/api/raw', force=True)
    fig1 = draw_quad(
        views, 'gas', 'Gas', 'Therms', 1.0,
        'Residential')
    fig2 = draw_quad(
        views, 'gas', 'Gas', 'Therms', 1.0,
        ['Commercial', 'Industrial'])
    fig3 = draw_quad(
        views, 'pwr', 'Electricity', 'MWh', 1000.0,
        'Residential')
    fig4 = draw_quad(
        views, 'pwr', 'Electricity', 'MWh', 1000.0,
        ['Commercial', 'Industrial', 'Street Lighting'])
    fig1.savefig('{0}/../figs/resid-gas.png'.format(PATH), dpi=100)
    fig2.savefig('{0}/../figs/other-gas.png'.format(PATH), dpi=100)
    fig3.savefig('{0}/../figs/resid-pwr.png'.format(PATH), dpi=100)
    fig4.savefig('{0}/../figs/other-pwr.png'.format(PATH), dpi=100)
