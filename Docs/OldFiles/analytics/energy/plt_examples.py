from energy_views import *
import matplotlib.pyplot as plt

def frame_quad(business_class=None):
    fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(2, 2)
    plt.subplots_adjust(left=0.05, right=0.95, top=0.90, bottom=0.05, hspace=0.50)
    if isinstance(business_class, basestring):
        title = business_class
    elif business_class:
        title = ' + '.join(business_class)
    else:
        title = ''
    return fig, title, ((ax0, ax1), (ax2, ax3))

def draw_dd(views):
    vs_temp, vs_time = views.dd_plot()

    fig, (ax0, ax1) = plt.subplots(1, 2)
    plt.subplots_adjust(left=0.05, right=0.95, top=0.85, bottom=0.15, hspace=0.50)
    fig.suptitle('Heating / Cooling Degree Days', fontsize=14)
    #
    # scatterplots & regression vs temperature
    #
    vs_temp['hdd regression'].plot(ax=ax0, c='r', alpha=0.75)
    vs_temp['cdd regression'].plot(ax=ax0, c='b', alpha=0.75)
    ax0.scatter(vs_temp.index, vs_temp['hdd scatter'], c='r', alpha=0.75)
    ax0.scatter(vs_temp.index, vs_temp['cdd scatter'], c='b', alpha=0.75)
    #
    # timeplots
    #
    vs_time['HDD'].plot(ax=ax1, c='r', alpha=0.75)
    vs_time['CDD'].plot(ax=ax1, c='b', alpha=0.75)
    #
    # decoration
    #
    patches, labels = ax0.get_legend_handles_labels()
    ax0.legend(patches, ['HDD', 'CDD'])
    ax0.set_xlim(25., 80.)
    ymin, ymax = ax0.get_ylim()
    ax0.set_ylim(0, ymax)
    ax0.set_ylabel('Degree Days', fontsize=12)
    ax0.set_xlabel('degrees F')
    ax1.set_xlabel('')

    fig.set_size_inches(17.07, 8.19)
    fig.savefig('{0}/../figs/degree days.png'.format(PATH), dpi=100)
    vs_temp.to_csv('{0}/../figs/temp vs degree days.csv'.format(PATH))
    vs_time.to_csv('{0}/../figs/time vs degree days.csv'.format(PATH))
    return fig

def emit_quad(df_temp, df_time, path):
    frames = []
    for city_code, aggr, df in df_temp:
        df['city'] = city_code
        df['aggr'] = aggr
        frames.append(df.reset_index())
    df = ps.concat(frames, ignore_index=True)
    df = ps.pivot_table(
        df,
        index='temp',
        columns=['city', 'aggr'],
        values=['scatter', 'heating regression', 'cooling regression'])
    df.to_csv(path + '-temp.csv')

    frames = {}
    for city_code, aggr, ser in df_time:
        frames[(city_code, aggr)] = ser
    df = ps.DataFrame(frames)
    df.to_csv(path + '-time.csv')

def draw_quad(views, what, label, units, business_class):
    fig, title, ((ax0, ax1), (ax2, ax3)) = frame_quad(business_class)
    fig.suptitle('{0} Consumption: {1}'.format(label, title), fontsize=14)
    df_temp = []
    df_time = []
    #
    # Town - aggregate
    #
    vs_temp, vs_time = views.plots(
        what,
        'PRINCETON TWP',
        business_class,
        per_meter=False)
    vs_temp /= 1000.0
    vs_time /= 1000.0
    df_temp.append(('Town', 'aggregate', vs_temp))
    df_time.append(('Town', 'aggregate', vs_time))
    vs_time.plot(ax=ax0, c=COLOR_TOWN)
    vs_temp['heating regression'].plot(ax=ax1, c='r', alpha=0.75)
    vs_temp['cooling regression'].plot(ax=ax1, c='b', alpha=0.75)
    ax1.scatter(vs_temp.index, vs_temp['scatter'], c=COLOR_TOWN, alpha=0.75, marker='s')
    #
    # Boro - aggregate
    #
    vs_temp, vs_time = views.plots(
        what,
        'PRINCETON BORO',
        business_class,
        per_meter=False)
    vs_temp /= 1000.0
    vs_time /= 1000.0
    df_temp.append(('Boro', 'aggregate', vs_temp))
    df_time.append(('Boro', 'aggregate', vs_time))
    vs_time.plot(ax=ax0, c=COLOR_BORO)
    vs_temp['heating regression'].plot(ax=ax1, c='r', alpha=0.75)
    vs_temp['cooling regression'].plot(ax=ax1, c='b', alpha=0.75)
    ax1.scatter(vs_temp.index, vs_temp['scatter'], c=COLOR_BORO, alpha=0.75, marker='s')
    #
    # Town - per meter
    #
    vs_temp, vs_time = views.plots(
        what,
        'PRINCETON TWP',
        business_class,
        per_meter=True)
    df_temp.append(('Town', 'per meter', vs_temp))
    df_time.append(('Town', 'per meter', vs_time))
    vs_time.plot(ax=ax2, c=COLOR_TOWN)
    vs_temp['heating regression'].plot(ax=ax3, c='r', alpha=0.75)
    vs_temp['cooling regression'].plot(ax=ax3, c='b', alpha=0.75)
    ax3.scatter(vs_temp.index, vs_temp['scatter'], c=COLOR_TOWN, alpha=0.75, marker='s')
    #
    # Boro - per meter
    #
    vs_temp, vs_time = views.plots(
        what,
        'PRINCETON BORO',
        business_class,
        per_meter=True)
    df_temp.append(('Boro', 'per meter', vs_temp))
    df_time.append(('Boro', 'per meter', vs_time))
    vs_time.plot(ax=ax2, c=COLOR_BORO)
    vs_temp['heating regression'].plot(ax=ax3, c='r', alpha=0.75)
    vs_temp['cooling regression'].plot(ax=ax3, c='b', alpha=0.75)
    ax3.scatter(vs_temp.index, vs_temp['scatter'], c=COLOR_BORO, alpha=0.75, marker='s')
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
    ax2.set_title('Avg. Usage / Meter', fontsize=12)
    ax2.set_ylabel('{0}'.format(units), fontsize=12)
    ax2.set_xlabel('')
    ax3.set_title('Avg. Usage / Meter vs Temp.', fontsize=12)
    ymin, ymax = ax0.get_ylim()
    ax0.set_ylim(0., ymax)
    xmin, xmax = ax1.get_xlim()
    ax1.set_xlim(25., 80.)
    ymin, ymax = ax2.get_ylim()
    ax2.set_ylim(0., ymax)
    xmin, xmax = ax3.get_xlim()
    ax3.set_xlim(25., 80.)

    if business_class == 'Residential':
        kind = 'resid-' + what
    else:
        kind = 'other-' + what
    fig.set_size_inches(17.07, 8.19)
    fig.savefig('{0}/../figs/{1}.png'.format(PATH, kind), dpi=100)
    path = '{0}/../figs/{1}'.format(PATH, kind)
    emit_quad(df_temp, df_time, path)

    return fig

def draw_sa_plot(views, business_class, per_meter=True):
    fig, title, ((ax0, ax1), (ax2, ax3)) = frame_quad(business_class)
    plt.subplots_adjust(left=0.05, right=0.95, top=0.90, bottom=0.05, hspace=0.55)
    fig.suptitle('Seasonally Adjusted w/o Temp. Correction: {0}'.format(title), fontsize=14)

    ax0.set_title('Gas', fontsize=12)
    ax0.set_ylabel('Town', fontsize=12)
    sadj = views.sa_plot('gas', 'PRINCETON TWP', business_class, per_meter)
    sadj['data'].plot(ax=ax0, alpha=0.75, color=COLOR_TOWN)
    sadj['adjustment'].plot(ax=ax0, alpha=0.75, color=COLOR_TOWN, linestyle='--')
    sadj['variation'].plot(ax=ax0, alpha=1.00, color=COLOR_BLACK)
    sadj['adjusted'].plot(ax=ax0, alpha=1.00, color=COLOR_BLACK, linestyle='--')
    ax0.set_xlabel('')

    ax1.set_title('Power', fontsize=12)
    sadj = views.sa_plot('pwr', 'PRINCETON TWP', business_class, per_meter)
    sadj['data'].plot(ax=ax1, alpha=0.75, color=COLOR_TOWN)
    sadj['adjustment'].plot(ax=ax1, alpha=0.75, color=COLOR_TOWN, linestyle='--')
    sadj['variation'].plot(ax=ax1, alpha=1.00, color=COLOR_BLACK)
    sadj['adjusted'].plot(ax=ax1, alpha=1.00, color=COLOR_BLACK, linestyle='--')
    ax1.set_xlabel('')

    ax2.set_ylabel('Boro', fontsize=12)
    sadj = views.sa_plot('gas', 'PRINCETON BORO', business_class, per_meter)
    sadj['data'].plot(ax=ax2, alpha=0.75, color=COLOR_BORO)
    sadj['adjustment'].plot(ax=ax2, alpha=0.75, color=COLOR_BORO, linestyle='--')
    sadj['variation'].plot(ax=ax2, alpha=1.00, color=COLOR_BLACK)
    sadj['adjusted'].plot(ax=ax2, alpha=1.00, color=COLOR_BLACK, linestyle='--')
    ax2.set_xlabel('')

    sadj = views.sa_plot('pwr', 'PRINCETON BORO', business_class, per_meter)
    sadj['data'].plot(ax=ax3, alpha=0.75, color=COLOR_BORO)
    sadj['adjustment'].plot(ax=ax3, alpha=0.75, color=COLOR_BORO, linestyle='--')
    sadj['variation'].plot(ax=ax3, alpha=1.00, color=COLOR_BLACK)
    sadj['adjusted'].plot(ax=ax3, alpha=1.00, color=COLOR_BLACK, linestyle='--')
    ax3.set_xlabel('')

    patches, labels = ax0.get_legend_handles_labels()
    ax0.legend(patches,
               ['Unadjusted', 'Seasonality', 'Adjusted', 'Variation'],
               bbox_to_anchor=(0., -0.35, 1., .102),
               ncol=2,
               mode='expand',
               borderaxespad=0.)

    if business_class == 'Residential':
        kind = 'resid-sadj'
    else:
        kind = 'other-sadj'
    fig.set_size_inches(17.07, 8.19)
    fig.savefig('{0}/../figs/{1}.png'.format(PATH, kind), dpi=100)
    sadj.to_csv('{0}/../figs/{1}.csv'.format(PATH, kind))
    return fig

def draw_bubba(views):
    points = []
    b, h, c = views.model(
        'pwr', 'PRINCETON TWP', 'Residential', per_meter=True)
    points.append(('Town: Residential per Meter (Electricity)',
                   b, h, c, COLOR_TOWN, COLOR_TOWN, COLOR_TOWN))
    b, h, c = views.model(
        'pwr', 'PRINCETON BORO', 'Residential', per_meter=True)
    points.append(('Boro: Residential per Meter (Electricity)',
                   b, h, c, COLOR_BORO, COLOR_BORO, COLOR_BORO))
    b, h, c = views.model(
        'pwr', 'PRINCETON TWP',
        ['Commercial', 'Industrial', 'Street Lighting'], per_meter=True)
    points.append(('Town: Other per Meter (Electricity)',
                   b, h, c, COLOR_TOWN, COLOR_BLACK, COLOR_BLACK))
    b, h, c = views.model(
        'pwr', 'PRINCETON BORO',
        ['Commercial', 'Industrial', 'Street Lighting'], per_meter=True)
    points.append(('Boro: Other per Meter (Electricity)',
                   b, h, c, COLOR_BORO, COLOR_BLACK, COLOR_BLACK))
    pwr_per = ps.DataFrame(
        points,
        columns=['label', 'b', 'h', 'c', 'color', 'edge', 'center'])

    points = []
    b, h, c = views.model(
        'gas', 'PRINCETON TWP', 'Residential', per_meter=True)
    points.append(('Town: Residential per Meter (Gas)',
                   b, h, c, COLOR_TOWN, COLOR_TOWN, COLOR_TOWN))
    b, h, c = views.model(
        'gas', 'PRINCETON BORO', 'Residential', per_meter=True)
    points.append(('Boro: Residential per Meter (Gas)',
                   b, h, c, COLOR_BORO, COLOR_BORO, COLOR_BORO))
    b, h, c = views.model(
        'gas', 'PRINCETON TWP', ['Commercial', 'Industrial'], per_meter=True)
    points.append(('Town: Other per Meter (Gas)',
                   b, h, c, COLOR_TOWN, COLOR_BLACK, COLOR_BLACK))
    b, h, c = views.model(
        'gas', 'PRINCETON BORO', ['Commercial', 'Industrial'], per_meter=True)
    points.append(('Boro: Other per Meter (Gas)',
                   b, h, c, COLOR_BORO, COLOR_BLACK, COLOR_BLACK))
    gas_per = ps.DataFrame(
        points,
        columns=['label', 'b', 'h', 'c', 'color', 'edge', 'center'])
    points = []
    b, h, c = views.model(
        'pwr', 'PRINCETON TWP', 'Residential', per_meter=False)
    points.append(('Town: Residential Aggregate (Electricity)',
                   b, h, c, COLOR_TOWN, COLOR_TOWN, COLOR_TOWN))
    b, h, c = views.model(
        'pwr', 'PRINCETON BORO', 'Residential', per_meter=False)
    points.append(('Boro: Residential Aggregate (Electricity)',
                   b, h, c, COLOR_BORO, COLOR_BORO, COLOR_BORO))
    b, h, c = views.model(
        'pwr', 'PRINCETON TWP',
        ['Commercial', 'Industrial', 'Street Lighting'], per_meter=False)
    points.append(('Town: Other Aggregate (Electricity)',
                   b, h, c, COLOR_TOWN, COLOR_BLACK, COLOR_BLACK))
    b, h, c = views.model(
        'pwr', 'PRINCETON BORO',
        ['Commercial', 'Industrial', 'Street Lighting'], per_meter=False)
    points.append(('Boro: Other Aggregate (Electricity)',
                   b, h, c, COLOR_BORO, COLOR_BLACK, COLOR_BLACK))
    pwr_all = ps.DataFrame(
        points,
        columns=['label', 'b', 'h', 'c', 'color', 'edge', 'center'])

    points = []
    b, h, c = views.model(
        'gas', 'PRINCETON TWP', 'Residential', per_meter=False)
    points.append(('Town: Residential Aggregate (Gas)', b, h, c, COLOR_TOWN, COLOR_TOWN, COLOR_TOWN))
    b, h, c = views.model(
        'gas', 'PRINCETON BORO', 'Residential', per_meter=False)
    points.append(('Boro: Residential Aggregate (Gas)', b, h, c, COLOR_BORO, COLOR_BORO, COLOR_BORO))
    b, h, c = views.model(
        'gas', 'PRINCETON TWP', ['Commercial', 'Industrial'], per_meter=False)
    points.append(('Town: Other Aggregate (Gas)', b, h, c, COLOR_TOWN, COLOR_BLACK, COLOR_BLACK))
    b, h, c = views.model(
        'gas', 'PRINCETON BORO', ['Commercial', 'Industrial'], per_meter=False)
    points.append(('Boro: Other Aggregate (Gas)', b, h, c, COLOR_BORO, COLOR_BLACK, COLOR_BLACK))
    gas_all = ps.DataFrame(
        points,
        columns=['label', 'b', 'h', 'c', 'color', 'edge', 'center'])

    fig, (ax0, ax1) = plt.subplots(1, 2)
    plt.subplots_adjust(left=0.05, right=0.95, top=0.90, bottom=0.10, hspace=0.50)
    fig.suptitle('"You Are Here"', fontsize=14)

    a, x, y = pwr_per['b'], pwr_per['h'], pwr_per['c']
    ax0.scatter(
        x * 100,
        y * 10,
        (a * 400),
        c=pwr_per['color'],
        edgecolor=pwr_per['edge'],
        alpha=0.50,
        linewidth=2)

    a, x, y = gas_per['b'], gas_per['h'], gas_per['c']
    ax1.scatter(
        x,
        y,
        (a * 4),
        c=pwr_per['color'],
        edgecolor=pwr_per['edge'],
        alpha=0.75,
        linewidth=2)

    ax0.set_ylabel('Sensitivity to Cooling Degree Days', fontsize=12)
    ax0.set_title('Electricity: Per Meter', fontsize=12)
    ax1.set_title('Gas: Per Meter', fontsize=12)
    ax0.set_xlabel('Sensitivity to Heating Degree Days', fontsize=12)
    ax1.set_xlabel('Sensitivity to Heating Degree Days', fontsize=12)

    fig.set_size_inches(17.07, 8.19)
    fig.savefig('{0}/../figs/you are here.png'.format(PATH), dpi=100)
    yah = ps.concat([pwr_per, gas_per, pwr_all, gas_all], ignore_index=True)
    yah.to_csv('{0}/../figs/you are here.csv'.format(PATH))


if __name__ == '__main__':
    COLOR_BLACK = '#000000'
    COLOR_TOWN = '#01DF01'
    COLOR_BORO = '#FF4000'
    views = EnergyViews('http://slacker87.koding.io:3000/api/raw', source='CSV')
    #
    # degree days & temperature
    #
    draw_dd(views)
    #
    # consumption vs time and temperature
    #
    # draw_quad(
    #     views, 'gas', 'Gas', 'Therms',
    #     'Residential')
    # draw_quad(
    #     views, 'gas', 'Gas', 'Therms',
    #     ['Commercial', 'Industrial'])
    # draw_quad(
    #     views, 'pwr', 'Power', 'MWh',
    #     'Residential')
    # draw_quad(
    #     views, 'pwr', 'Power', 'MWh',
    #     ['Commercial', 'Industrial', 'Street Lighting'])
    #
    # seasonally adjusted consumption
    #
    # draw_sa_plot(
    #     views,
    #     'Residential', per_meter=True)
    # draw_sa_plot(
    #     views,
    #     ['Commercial', 'Industrial', 'Street Lighting'], per_meter=True)
    # plt.show()
    draw_bubba(views)
    plt.show()