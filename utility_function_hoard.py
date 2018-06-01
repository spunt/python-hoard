#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Type <function_name> -h for help
'''

# ---------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------
import os
import gc
import pickle
import numpy as np
import pandas as pd
import pytablewriter
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import missingno as msno
from matplotlib import gridspec
from scipy import stats
from geopy.geocoders import GoogleV3
from geopy.geocoders import GeoNames
from geopy.exc import GeocoderTimedOut
from geopy.distance import great_circle
pd.set_option('precision', 2)
pd.set_option('float_format', lambda x: '%.2f' % x)
pd.set_option('date_yearfirst', True)

# ---------------------------------------------------------------------
#   CONSTANTS
# ---------------------------------------------------------------------


def get_holiday():

    us_holidays = {
        '2016-10-31': 'Halloween',
        '2016-11-11': 'Veterans Day',
        '2016-11-24': 'Thanksgiving',
        '2016-11-25': 'Black Friday',
        '2016-12-24': 'Christmas Eve Day',
        '2016-12-25': 'Christmas Day',
        '2016-12-26': 'Christmas Day (Observed)',
        '2016-12-31': "New Year's Eve Day",
        '2017-01-01': "New Year's Day",
        '2017-01-02': "New Year's Day (Observed)",
        '2017-01-16': 'Martin Luther King-Jr. Day',
        '2017-02-20': "Washington's Birthday",
        '2017-05-29': 'Memorial Day',
        '2017-07-04': 'Independence Day',
        '2017-09-04': 'Labor Day',
        '2017-10-31': 'Halloween',
        '2017-11-10': 'Veterans Day (Observed)',
        '2017-11-23': 'Thanksgiving',
        '2017-11-24': 'Black Friday',
        '2017-12-24': 'Christmas Eve Day',
        '2017-12-25': 'Christmas Day',
        '2017-12-31': "New Year's Eve Day",
        '2018-01-01': "New Year's Day",
        '2018-01-15': 'Martin Luther King-Jr. Day',
        '2018-02-19': "Washington's Birthday",
        '2018-05-28': 'Memorial Day',
        '2018-07-04': 'Independence Day',
        '2018-09-03': 'Labor Day',
        '2018-10-08': 'Columbus Day',
        '2018-10-31': 'Halloween',
        '2018-11-11': 'Veterans Day',
        '2018-11-22': 'Thanksgiving',
        '2018-11-24': 'Black Friday',
        '2018-12-24': 'Christmas Eve Day',
        '2018-12-25': 'Christmas Day',
        '2018-12-31': "New Year's Eve Day"
    }
    return us_holidays


def get_rename_dict():

    renamedict = {
        'relative_day_days_tw_capture_count': 'Number of Captures',
        'relative_day_days_tw_capture_days': 'Number of Active Days',
        'relative_day_weeks_tw_capture_weeks': 'Number of Active Weeks',
        'relative_day_days_max_streak': 'Longest Streak of Active Days',
        'relative_day_weeks_max_streak': 'Longest Streak of Active Weeks',
        'miles_from_first_mean': 'Average Miles from 1st Location',
        'miles_from_first_median': 'Median Miles from 1st Location',
        'miles_from_first_std': 'SD Distance from 1st Location',
        'miles_from_first_max': 'Max Distance from 1st Location',
        'ambient_light_intensity_cat_mode': 'Most Common Ambient Light Level',
        'dayofweek_mode': 'Most Common Day',
        'holiday_name_mode': 'Most Common Day (incl. Specific Holidays)',
        'is_holiday_prop_is': 'Proportion of Captures on Holidays',
        'is_weekend_prop_is': 'Proportion of Captures on Weekends',
        'is_business_hour_prop_is': 'Proportion of Captures during Business Hours',
        'is_night_prop_is': 'Proportion of Captures at Night',
        'city_nunique': 'Number of Cities',
        'country_nunique': 'Number of Countries',
        'latlon_nunique': 'Number of Unique Capture Locations',
        'hourofday_mean': 'Average Capture Hour of Day',
        'hourofday_mode': 'Most Common Capture Hour of Day',
        'hourofday_ord_mode': 'Most Common Capture Time of Day',
        'hourofday_std': 'Hour of Day Variation across Captures',
        'inferred_age_bucket': 'Age Bucket',
        'gender': 'Gender',
        'snapchat_total_per_day': 'Daily Snapchat Use',
        'snapchat_total_per_day_cat': 'Daily Snapchat Use Bucket',
        'sentcount_per_day_cat': 'Snaps/Day Bucket',
        'storycount_per_day_cat': 'Stories/Day Bucket',
        'friendcount_per_day_cat': 'Friends/Day Bucket',
        'device_num_users': 'Number of Users Per Device',
        'proportion_total_use': 'Proportion of Total Device Usage',
        'age_cat': 'Age',
        'gender': 'Gender',
        'os_type': 'OS',
        'specs_adoption_speed_days': 'Adoption Speed',
        'sentcount_cat': 'Snap Count',
        'storycount_cat': 'Story Count',
        'friendcount_cat': 'Friend Count',
        'snapchat_tenure_months_cat': 'Snapchat Tenure',
        'specs_tenure_days_ord': 'Spectacles Tenure (Ordinal)',
        'sentcount': 'Snap Count (Raw)',
        'storycount': 'Story Count (Raw)',
        'friendcount': 'Friend Count (Raw)',
        'sentcount_ord': 'Snap Count (Ordinal)',
        'storycount_ord': 'Story Count (Ordinal)',
        'friendcount_ord': 'Friend Count (Ordinal)',
        'snapchat_tenure_months_ord': 'Snapchat Tenure (Ordinal)',
        'sentcount_per_day': 'Snaps/Day',
        'storycount_per_day': 'Stories/Day',
        'friendcount_per_day': 'Friends/Day',
        'specs_tenure_days': 'Spectacles Retention',
        'snapchat_tenure_months': 'Snapchat Tenure (Raw)',
        'num_captured_sum': 'Number of Captures',
        'capture_date_count': 'Number of Active Days',
        'snapchat_start_date': 'Snapchat Start Date'
    }
    return renamedict


def get_snap_color_palette(N=12, as_color_palette=False):

    if N <= 2:
        pal = ['FFFC00', 'A7AAA9']
        pal = ['#' + p for p in pal]
    else:
        pal = ['FFFC00', '0EADFF', 'F23C57', 'A05DCD', 'FF8A00', '02B790',
               'E95080', 'FFD838', 'CED4DA', 'A7AAA9', '656D78', '000000']
        pal = ['#' + p for p in pal]

    if as_color_palette:
        return sns.palettes.color_palette(pal[:N])
    else:
        return pal[:N]


def set_sns(scale=1.5):

    sns.set(font_scale=scale, style='ticks', color_codes=True)
    sns.set_palette(get_snap_color_palette())


def set_font_sizes(sizes=(11, 13, 14)):

    plt.rc('font', size=sizes[0])         # controls default text sizes
    plt.rc('axes', titlesize=sizes[0])    # fontsize of the axes title
    plt.rc('axes', labelsize=sizes[1])    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=sizes[0])   # fontsize of the tick labels
    plt.rc('ytick', labelsize=sizes[0])   # fontsize of the tick labels
    plt.rc('legend', fontsize=sizes[0])   # legend fontsize
    plt.rc('figure', titlesize=sizes[2])  # fontsize of the figure title


def get_bins():

    # Source for levels:
    # https://msdn.microsoft.com/en-us/library/windows/desktop/dd319008(v=vs.85).aspx

    dfdict = {
        'sentcount_per_day': [[0, 1/7, 1, 5, 10, 25, np.inf], ['< 1/wk.', '< 1/day', '< 5/day', '< 10/day', '< 25/day', '25+/day']],
        'storycount_per_day': [[0, 1/14, 1/4, 1/2, 1, 2, np.inf], ['< 1/2wk.', '< 1/4day', '< 1/2day', '< 1/day', '< 2/day', '2+/day']],
        'specs_tenure_days': [[0, 2, 10, 25, 50, 75, 100, np.inf], ['0-1', '2-9', '10-24', '25-49', '50-74', '75-99', '100-120']],
        'snapchat_tenure_months': [[0, 1, 6, 12, 24, 36, np.inf], ['< 1 mo.', '< 6 mo.', '< 1 yr.', '< 2 yr.', '< 3 yr.', '3+ yr.']],
        'snapchat_score': [[0, 100, 1000, 10000, 50000, 100000, np.inf], ['< 100', '< 1,000', '< 10,000', '< 50,000', '< 100,000', '100,000+']],
        'friendcount': [[0, 10, 20, 50, 150, 300, np.inf], ['< 10', '< 20', '< 50', '< 150', '< 300', '300+']],
        'sentcount': [[0, 50, 250, 1000, 5000, 25000, np.inf], ['< 50', '< 250', '< 1,000', '< 5,000', '< 25,000', '25,000+']],
        'storycount': [[0, 25, 100, 500, 1000, 2500, np.inf], ['< 25', '< 100', '< 500', '< 1,000', '< 2,500', '2,500+']],
        'age': [[0, 18, 21, 25, 35, np.inf], ['13-17', '18-20', '21-24', '25-34', '35-plus']],
        'ambient_light_intensity': [[0, 10, 50, 200, 400, 1000, 5000, 10000, 30000, np.inf], ['Pitch Black', 'Very Dark', 'Dark Indoors', 'Dim Indoors', 'Normal Indoors', 'Bright Indoors', 'Dim Outdoors', 'Cloudy Outdoors', 'Direct Sunlight']],
        'hourofday': [[0, 3, 6, 9, 12, 15, 18, 21, np.inf], ['12-2:59 AM', '3-5:59 AM', '6-8:59 AM', '9-11:59 AM', '12-2:59 PM', '3-5:59 PM', '6-8:59 PM', '9-11:59 PM']]
    }
    return dfdict

# ---------------------------------------------------------------------
#   STATS FUNCTIONS
# ---------------------------------------------------------------------


def describe(df, aggdict={'mean': 'Mean', 'median': 'Median', lambda x: int(x.mode()): 'Mode', 'std': 'SD', 'min': 'Min', 'max': 'Max', 'skew': 'Skew'}):

    dfnum = df.select_dtypes(include=[int, float])
    if aggdict == None:
        d = df.describe().reset_index()
    else:
        d = pd.DataFrame()
        for col, s in dfnum.iteritems():
            d = d.append(s.agg(list(aggdict.keys())))
        d = d.reset_index()
        d.columns = ['N = {:,}'.format(len(dfnum))] + list(aggdict.values())
    display(d)
    return d


def info(df, details=True):

    o = pd.DataFrame(df.count())
    o.columns = ['count']
    o['dtype'] = df.dtypes.values.astype(str)
    if details:
        dt = df.dtypes
        o.loc[dt == 'category', 'details'] = dt[dt ==
                                                'category'].apply(lambda x: list(x.categories))
        idx = o.dtype.str.contains('time|float|int')
        o.loc[idx, 'details'] = df[o.index[idx]].apply(
            lambda x: [x.min(), x.max()])
    return o.sort_values(by='dtype')


def describe_str(s, aggdict={'mean': 'Mean', 'median': 'Median', lambda x: int(x.mode()): 'Mode', 'std': 'SD'}):
    d = s.agg(list(aggdict.keys()))
    d = [np.round(x, 2) if x % 1 > 0 else int(x) for x in list(d)]
    str = ', '.join(['{} = {:,}'.format(n, y)
                     for n, y in zip(aggdict.values(), d)])
    return str


def groupby(df, group, transpose=False, metrics=['count', 'mean', 'std']):

    dfnum = df.select_dtypes(include=[int, float])
    aggregator = dict(zip(dfnum.columns.values, [metrics] * dfnum.shape[1]))
    gbg = df.groupby(group).agg(aggregator)
    display(gbg)
    print('\n\n')
    return gbg


def effectsize(df, dv_col, group_col):

    if type(dv_col) == list:
        dv_col = ''.join(dv_col)
    if type(group_col) == list:
        group_col = ''.join(group_col)

    group_means = df.groupby(group_col)[dv_col].mean().values
    group_diff = np.diff(group_means)
    effsize = group_diff / np.std(df[dv_col])
    return effsize


def corr(df, tomd=False, method='spearman'):

    rho = df.corr(method=method)
    row = list(rho.columns)
    for idx, col in enumerate(row):
        if tomd:
            row[idx] = '{} - {}'.format(idx+1, col)
        else:
            row[idx] = '{} - {}'.format(col, idx+1)
    rho.columns = np.arange(len(row)) + 1
    rho.index = row
    rho.index.rename('', inplace=True)
    if tomd:
        rho = rho.reset_index()
        writer = pytablewriter.MarkdownTableWriter()
        writer.header_list = list(df.columns.values)
        writer.from_dataframe(rho.round(2))
        writer.write_table()
    else:
        return rho


def corrplot(df, method='spearman', annot=True):

    # Compute the correlation matrix
    corr = df.corr(method=method)

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    # Set up the matplotlib figure
    ht = np.max([corr.shape[0], 3.5])
    f, ax = plt.subplots(figsize=(ht*1.30, ht))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr.round(2), mask=mask, cbar=False, cmap=cmap, vmax=1, center=0, xticklabels=False,
                square=True, annot=annot, linewidths=.5, cbar_kws={"shrink": .5})

    pad = .35

    yloc = ax.yaxis.get_ticklocs()
    for i, t in enumerate(list(corr.index)[:-1]):
        ax.text(yloc[i], yloc[i] + pad, t, fontsize=plt.rcParams['ytick.labelsize'],
                va='bottom', ha='left', rotation=45)
    ylim = ax.get_ylim()
    xlim = ax.get_xlim()
    ax.set_xlim((xlim[0], xlim[1]-1))
    ax.set_ylim((ylim[0], ylim[1]+1))
    return f, ax


def regress(DATA, DV, IV, transform=None, verbose=True):

    import statsmodels.formula.api as smf
    import statsmodels.api as sm
    from sklearn.metrics import mean_squared_error

    if transform:
        formula = '{}({})'.format(transform, DV) + ' ~ ' + \
            ' + '.join(['{}('.format(transform) + e + ')' for e in IV])
    else:
        formula = DV + ' ~ ' + ' + '.join(IV)
    ols = smf.ols(formula=formula, data=DATA).fit()
    rlm = smf.rlm(formula=formula, data=DATA).fit()
    poisson = smf.glm(formula=formula, data=DATA, family=sm.families.Poisson(
        sm.families.links.log)).fit()
    nbinom = smf.glm(formula=formula, data=DATA, family=sm.families.NegativeBinomial(
        sm.families.links.log)).fit()
    results = dict(zip(['ols', 'rlm', 'poisson', 'nbinom'],
                       [ols, rlm, poisson, nbinom]))
    if verbose:
        for k, v in results.items():
            print(k)
            Y_pred = v.predict(DATA[IV])
            rmse = np.sqrt(mean_squared_error(DATA[DV], Y_pred))
            print(rmse)
            print(v.summary2())


def oneoutzscore(s):

    s = np.random.normal(10, 5, [50, 1])
    if s.ndim == 1:
        s = s.reshape((s.shape[0], 1))
    nrow, ncol = s.shape
    cin = np.repeat(s, nrow, axis=1)
    cout = cin[np.eye(nrow) == 1]
    cin[np.eye(nrow) == 1] = np.nan
    ooz = ((cout - np.nanmean(cin, axis=0)) /
           np.nanstd(cin, axis=0)).reshape((nrow, 1))
    return ooz


def zscore(s):
    return (s - s.mean()) / s.std()


def zscore_modified_asymmetric(s):
    if s.ndim == 1:
        s = s[:, None]
    m = np.median(s)
    abs_dev = np.abs(s - m)
    left_mad = np.median(abs_dev[s <= m])
    right_mad = np.median(abs_dev[s >= m])
    s_mad = left_mad * np.ones(len(s))
    s_mad[s > m] = right_mad
    modified_z_score = 0.6745 * abs_dev / s_mad
    modified_z_score[s == m] = 0
    return modified_z_score
# ---------------------------------------------------------------------
#   DISPLAY ITEM FUNCTIONS
# ---------------------------------------------------------------------


def save_plot(figh=plt.gcf(), bbox='tight', outname='myfig.png', pad=2, tight=True, dpi=300, transparent=False):

    if tight:
        plt.tight_layout(pad=pad)

    figh.savefig(outname, dpi=dpi, bbox_inches='tight', transparent=transparent)
    plt.close()
    print('\nFIGURE SAVED TO: ' + outname)


def df2md(df, precision=2, tablename='table_name'):

    dft = df.round(precision).copy()
    writer = pytablewriter.MarkdownTableWriter()
    writer.header_list = list(dft.columns.values)
    writer.from_dataframe(dft)
    writer.write_table()


def annotate_plot(ax, fontsize):

    yloc = ax.yaxis.get_ticklocs()
    labelpad = ax.get_xlim()[-1] * .005

    for y, p in enumerate(ax.patches):
        width = p.get_width()
        height = yloc[y]
        ax.text(width + labelpad, height, '{}'.format(int(width)),
                fontsize=fontsize, va='center')


def add_footnote(figh, footnote, pad=-.01):

    t = figh.text(.98, pad, footnote, ha='right', va='bottom',
                  fontsize='x-small', fontstyle='italic', color='#555555')
    return t


def format_ticks(ax):

    tickfmt = ticker.FuncFormatter(lambda x, p: format(int(x), ','))
    ax.yaxis.set_major_locator(ticker.AutoLocator())
    ax.xaxis.set_major_locator(ticker.AutoLocator())
    if ax.get_xlim()[1] >= 1000:
        ax.xaxis.set_major_formatter(tickfmt)
    if ax.get_ylim()[1] >= 1000:
        ax.yaxis.set_major_formatter(tickfmt)


def format_yticks(ax):

    tickfmt = ticker.FuncFormatter(lambda x, p: format(int(x), ','))
    ax.yaxis.set_major_locator(ticker.AutoLocator())
    if ax.get_ylim()[1] >= 1000:
        ax.yaxis.set_major_formatter(tickfmt)


def format_xticks(ax):

    tickfmt = ticker.FuncFormatter(lambda x, p: format(int(x), ','))
    ax.xaxis.set_major_locator(ticker.AutoLocator())
    if ax.get_xlim()[1] >= 1000:
        ax.xaxis.set_major_formatter(tickfmt)


def plot_bin(df, bin_col, dv_col, type='barplot', palette='coolwarm', ci=99, n_boot=1000):

    g = sns.PairGrid(df, x_vars=IV, y_vars=DV, size=6, despine=True, aspect=1)
    g.map(sns.barplot, palette=palette, ci=ci, n_boot=n_boot)


def plot_dists(y, saveplot=False, ylabel='Count', xlabel=None, title=None, xlim=None, percentile=100, footnote=None, describe_inset=True):

    y = force_dataframe(y)
    ncol = y.shape[1]
    ax = []
    pal = get_snap_color_palette()
    for c in y.columns:
        figh, (ax_box, ax_hist) = plt.subplots(2, figsize=(12, 7),
                                               sharex=False, gridspec_kw={"height_ratios": (.20, .80)})
        if percentile < 100:
            footpad = -0.04
            cidx = y[c] > y[c].quantile(percentile/100)
            xlabel = c + \
                '\n(Upper {}% of distribution omitted)'.format(100-percentile)
            s = y.loc[~cidx, c]
        else:
            footpad = -0.01
            s = y[c]
        sns.boxplot(s, ax=ax_box, color=pal[0], orient='h')
        # https://blog.modeanalytics.com/violin-plot-examples/
        # sns.violinplot(y[c], ax=ax_box, palette='Dark2', orient='h')
        sns.distplot(
            s, ax=ax_hist, color=pal[1], hist=True, kde=False, rug=False)
        ax_box.set(xlabel='', xticks=[])
        ax_hist.set(ylabel=ylabel)
        ax_hist.yaxis.labelpad = 1

        if xlabel:
            ax_hist.set(xlabel=xlabel)
            ax_hist.xaxis.labelpad = 1
        xmax = np.max(ax_hist.get_xlim())
        ymax = np.max(ax_hist.get_ylim())
        if ymax > 1000:
            format_yticks(ax_hist)
        if xmax > 1000:
            format_xticks(ax_hist)
        if describe_inset:
            ax_hist.text(xmax*.99, ymax*.975, describe_str(s),
                         ha='right', va='top', fontsize=16)
        if footnote:
            figh.tight_layout()
            figh.text(.99, footpad, footnote, ha='right', va='bottom',
                      fontsize='small', fontstyle='italic', color='#555555')
        plt.subplots_adjust(hspace=.05)
        # plt.show()
        ax.append(ax_hist)
        if saveplot:
            save_plot(figh=figh, outname='DistPlot_{}.png'.format(
                c.replace(' ', '_')))
    if ncol == 1:
        ax = ax[0]
    return ax


def ecdf(data):
    """Compute ECDF for a one-dimensional array of measurements."""
    x = np.sort(data)
    y = np.arange(1, len(data) + 1) / len(data)
    return x, y


def plot_ecdf(s):

    x, y = ecdf(s)
    figh, ax = plt.subplots(figsize=(8, 4))
    plt.plot(x, y, marker='.', linestyle='none', color='#37474F', alpha=0.5)


def to_percent(y, position):
    return '{0:.0f}%'.format(y*100)


def plot_hist_stacked(x_list, bins, labels, xl, cumulative=False, as_percent=False, xticks=None):

    set_sns(1.4)
    yl1 = ['Cumulative' if cumulative else 'Probability']
    yl2 = ['Percentage' if as_percent else 'Density']
    yl = '{} {}'.format(yl1[0], yl2[0])
    pal = get_snap_color_palette()
    colors = [pal[i] for i in [2, 1]]
    figh, ax = plt.subplots(1, 1, figsize=(8, 4))
    for idx, s in enumerate(x_list):
        ax.hist(s, bins, density=True, cumulative=cumulative,
                color=colors[idx], label=labels[idx])
    if xticks:
        ax.set_xticks(xticks)
    xlim = [np.floor(np.concatenate(x_list).min()),
            np.ceil(np.concatenate(x_list).max())]
    ax.set(xlabel=xl, ylabel=yl, xlim=xlim)
    if as_percent:
        formatter = ticker.FuncFormatter(to_percent)
        ax.yaxis.set_major_formatter(formatter)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.legend()
    return figh, ax


def plot_hist(x, bins, xl, color='b', cumulative=False, as_percent=False, xticks=None):

    set_sns(1.4)
    yl1 = ['Cumulative' if cumulative else 'Probability']
    yl2 = ['Percentage' if as_percent else 'Density']
    yl = '{} {}'.format(yl1[0], yl2[0])
    pal = get_snap_color_palette()
    figh, ax = plt.subplots(1, 1, figsize=(8, 4))
    ax.hist(x, bins, density=True, cumulative=cumulative, color=color)
    if xticks:
        ax.set_xticks(xticks)
    xlim = [np.floor(x.min()), np.ceil(x.max())]
    ax.set(xlabel=xl, ylabel=yl, xlim=xlim)
    if as_percent:
        formatter = ticker.FuncFormatter(to_percent)
        ax.yaxis.set_major_formatter(formatter)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    return figh, ax


def plot_hists(y, saveplot=False, bins='auto', normed=True, ylabel='Count', xlabel=None, title=None, xlim=None, percentile=100, footnote=None, cumulative=False, describe_inset=False):

    y = force_dataframe(y)
    ncol = y.shape[1]
    ax = []
    pal = get_snap_color_palette()
    for c in y.columns:
        if percentile < 100:
            footpad = -0.04
            cidx = y[c] > y[c].quantile(percentile/100)
            xlabel = c + \
                '\n(Upper {}% of distribution omitted)'.format(100-percentile)
            s = y.loc[~cidx, c]
        else:
            footpad = -0.01
            s = y[c]
        figh, ax_hist = plt.subplots(figsize=(8, 4))
        ax_hist.hist(s, bins=bins, density=normed,
                     cumulative=cumulative, color=pal[1])
        ax_hist.set(ylabel=ylabel)
        ax_hist.yaxis.labelpad = 1
        if xlabel:
            ax_hist.set(xlabel=xlabel)
        xmax = np.max(ax_hist.get_xlim())
        ymax = np.max(ax_hist.get_ylim())
        if ymax > 1000:
            format_yticks(ax_hist)
        if xmax > 1000:
            format_xticks(ax_hist)
        if describe_inset:
            ax_hist.text(xmax*.99, ymax*.975, describe_str(s),
                         ha='right', va='top', fontsize=16)
        if footnote:
            figh.tight_layout()
            figh.text(.99, footpad, footnote, ha='right', va='bottom',
                      fontsize='small', fontstyle='italic', color='#555555')
        ax.append(ax_hist)
        if saveplot:
            save_plot(figh=figh, outname='DistPlot_{}.png'.format(
                c.replace(' ', '_')))
    if ncol == 1:
        ax = ax[0]
    return ax


def plot_pointplot(x, y, groups, df, size=5, ci=99, palette='dark', showit=True):

    if type(x) == str:
        f, ax = plt.subplots(figsize=(size, size))
        sns.pointplot(x=x, y=y, hue=groups, data=df, size=size,
                      ax=ax, palette=palette, ci=ci, n_boot=1000)
    else:
        ncol = len(x)
        f, axarr = plt.subplots(
            figsize=(size * ncol * 1.33, size), nrows=1, ncols=ncol, sharey=False)
        for idx, ax in enumerate(axarr):
            sns.pointplot(x=x[idx], y=y, hue=groups, data=df,
                          size=size, ax=ax, palette=palette, ci=ci, n_boot=1000)
    if showit:
        plt.show()
    return f


def plot_counts(x, df, xl=None, yl='Number of Users', winsorize_at=None, describe_inset=True, saveplot=False, order=None, orient=None, saturation=.90, font_scale=1.5):

    sns.set(font_scale=font_scale, style='ticks', color_codes=True)
    pal = get_snap_color_palette(1)
    nval = df[x].nunique()
    if orient == 'h':
        figsize = (6, nval)
    else:
        figsize = (nval, 6)
    figh, ax = plt.subplots(1, figsize=figsize)
    if winsorize_at:
        xwin = x + ' (Winsorized)'
        df[xwin] = df[x].apply(
            lambda x: winsorize_at if x >= winsorize_at else x)
        sns.countplot(x=xwin, data=df, ax=ax,
                      color=pal[0], order=order, orient=orient, saturation=saturation)
        xticklab = ax.get_xticklabels()
        xticklab[-1] = '{}+'.format(winsorize_at)
        ax.set_xticklabels(xticklab)
    else:
        sns.countplot(x=x, data=df, ax=ax,
                      color=pal[0], order=order, orient=orient, saturation=saturation)
    nxtick = len(ax.get_xticks())
    figh.set_size_inches((len(ax.get_xticks())*(4/3), 6))
    xmax = np.max(ax.get_xlim())
    ymax = np.max(ax.get_ylim())
    if ymax > 1000:
        format_yticks(ax)
    if xl:
        ax.set(xlabel=xl)
    if yl:
        ax.set(ylabel=yl)
    if describe_inset:
        if winsorize_at:
            aggdict = {'mean': 'Mean', 'median': 'Median', lambda x: int(
                x.mode()): 'Mode', 'max': 'Max', 'std': 'SD'}
        else:
            aggdict = {'mean': 'Mean', 'median': 'Median',
                       lambda x: int(x.mode()): 'Mode', 'std': 'SD'}
        ax.text(xmax*.99, ymax*.975,
                describe_str(df[x], aggdict=aggdict), ha='right', va='top', fontsize='small')
    if saveplot:
        save_plot(figh=figh, outname='DistPlot_{}.png'.format(
            c.replace(' ', '_')))
    return figh


def plot_violin(df):

    # Plot
    fig, axarr = plt.subplots(1, 4, figsize=(9, 6), sharey=False)
    sns.violinplot(x='gender', y='capture_latest_days',
                   data=usage, ax=axarr[0])
    sns.violinplot(x='os_type', y='capture_latest_days',
                   data=usage, ax=axarr[1])
    sns.violinplot(x='gender', y='capture_latest_days',
                   data=usage, ax=axarr[2])
    sns.violinplot(x='os_type', y='capture_latest_days',
                   data=usage, ax=axarr[3])
    plt.tight_layout()
    plt.show()


def plot_ts(ts, saveplot=True):

    figh, ax = plt.subplots(1, figsize=(12, 4))
    # tscount = df.groupby('capture_date')['num_captured'].count()
    tscount.plot(kind='area', title='Daily Active User Count', ax=ax)
    ax.set(ylabel='User Count', xlabel='')

    # Format the ticks
    import matplotlib.dates as mdates
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))

    # round to nearest months...
    # datemin = np.datetime64(df.capture_date.min(), 'M')
    # datemax = np.datetime64(df.capture_date.max(), 'M') + np.timedelta64(1, 'M')
    datemin = np.datetime64(df.capture_date.min(), 'M')
    datemax = np.datetime64(df.capture_date.max(), 'M') + \
        np.timedelta64(1, 'M')
    ax.set_xlim(df.capture_date.min(), df.capture_date.max())
    # ax.grid(True)
    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    figh.autofmt_xdate(rotation=0, ha='center')
    ax.tick_params(axis='both', which='minor', labelsize=12)
    ax.tick_params(axis='both', which='major', labelsize=15, pad=15)
    # tickfmt = ticker.FuncFormatter(lambda x, p: format(int(x), ','))
    # ax.yaxis.set_major_formatter(tickfmt)
    # figh, (ax_count, ax_total) = plt.subplots(2, figsize=(12, 8), sharex=False, gridspec_kw={"height_ratios": (.50, .50)})
    # ax_count.set(xlabel='', xticks=[], ylabel='User Count')
    # tstotal = df.groupby('capture_date')['num_captured'].sum()
    # plt.subplots_adjust(hspace=.1)
    # tstotal.plot(xlim=(tstotal.index.min(), tstotal.index.max()), kind='area', ax=ax_total)
    # ax_total.set(xlabel='Date', ylabel='Capture Count')

    # turnpoint = [pd.to_datetime('2017-12-25'), pd.to_datetime('2016-12-25')]
    # for t in turnpoint :
    #     ax.axvline(x=t, color='r', linestyle='--', linewidth=4, label='Christmas Day')

    if saveplot:
        save_plot(figh=figh, outname='Plot_Daily_Capture_Counts.png')
    return figh


def plot_user_ts(df, saveplot=True):
    # figh, (ax_count, ax_total) = plt.subplots(2, figsize=(12, 8),
    #                                           sharex=False, gridspec_kw={"height_ratios": (.50, .50)})
    # tscount = df.groupby('capture_date')['num_captured'].count()
    # tstotal = df.groupby('capture_date')['num_captured'].sum()
    # plt.subplots_adjust(hspace=.1)
    # tscount.plot(xlim=(tscount.index.min(), tscount.index.max()),
    #              kind='rug', title='Daily Captures', ax=ax_count)
    # tstotal.plot(xlim=(tstotal.index.min(), tstotal.index.max()),
    #              kind='area', ax=ax_total)
    # ax_count.set(xlabel='', xticks=[], ylabel='User Count')
    # ax_total.set(xlabel='Date', ylabel='Capture Count')
    # plt.show()
    # return figh
    # if saveplot:
    #     save_plot(figh=figh, outname='Plot_Daily_Capture_Counts.png')

    tsmat = np.zeros((1, TIME_WINDOW_DAYS), dtype=int)[0]
    idx = day <= TIME_WINDOW_DAYS
    tsmat[day[idx]] = count[idx]
    plt.plot(np.arange(1, TIME_WINDOW_DAYS+1), tsmat)


def plot_reg(y, x, df, robust=False, x_bins=None, logx=False, x_partial=None, truncate=True):

    figh, ax = plt.subplots(figsize=(10, 4))
    sns.regplot(x=x, y=y, ax=ax, x_partial=x_partial, data=df,
                x_bins=None, logx=False, robust=robust, truncate=truncate)
    plt.tight_layout(pad=1)
    plt.show()

# ---------------------------------------------------------------------
#   SUPPORTING FUNCTIONS
# ---------------------------------------------------------------------


def get_elements(s, idx):
    return [s[i] for i in idx]


def apply_groupby_agg(df, aggregator, groupby=['user_id'], testrun=False):

    if testrun:
        um = df.sample(
            len(df)//100).groupby(groupby).agg(aggregator).reset_index()
        colnames = ['_'.join(col) if col[-1] else ''.join(col)
                    for col in um.columns]
        um.columns = um.columns.levels[1][um.columns.labels[1]]
        um.columns = colnames
    else:
        um = df.groupby(groupby).agg(aggregator).reset_index()
        colnames = ['_'.join(col) if col[-1] else ''.join(col)
                    for col in um.columns]
        um.columns = um.columns.levels[1][um.columns.labels[1]]
        um.columns = colnames
    return um


def winsorize(s, limits=(None, .05), inclusive=(True, True)):

    return stats.mstats.winsorize(s, limits=limits, inclusive=inclusive)


def geocode_address(address, geolocator):
    """Google Maps v3 API: https://developers.google.com/maps/documentation/geocoding/"""
    # https://stackoverflow.com/questions/27914648/geopy-catch-timeout-error
    try:
        location = geolocator.geocode(address, exactly_one=True, timeout=5)
    except GeocoderTimedOut as e:
        print("GeocoderTimedOut: geocode failed on input %s with message %s" %
              (address, e.msg))
    except AttributeError as e:
        print("AttributeError: geocode failed on input %s with message %s" %
              (address, e.msg))
    if location:
        address_geo = location.address
        latitude = location.latitude
        longitude = location.longitude
        return address_geo, latitude, longitude
    else:
        print("Geocoder couldn't geocode the following address: %s" % address)


def geolocate(locstr):
    # google_locator = GoogleV3(api_key="AIzaSyAXKcZ_c5WmJrl7 - GMWhsbXvzd5mfGDMh4")
    geoname_locator = GeoNames(username='bobspunt', timeout=5)
    loc = []
    for index, row in locstr.iterrows():
        try:
            s = list(row.values)
            address2 = '{}'.format(s[0])
            # result = geocode_address(address2, google_locator)
            result = geocode_address(address2, geoname_locator)
            d = {'index': index, 'address_geo': result[0], 'latitude': result[1],
                 'longitude': result[2]}
            if d['address_geo'] is not None:
                loc.append(d)
                print(d)
        except:
            print(row)
            continue
    return loc


def geoplot(loc):

    # |   | latitude | longitude |  color |  size | label |
    # |---|----------|-----------|--------|-------|-------|
    # | 0 |  48.8770 |  2.30698  |  blue  |  tiny |       |
    # | 1 |  48.8708 |  2.30523  |   red  | small |       |
    # | 2 |  48.8733 |  2.32403  | orange |  mid  |   A   |
    # | 3 |  48.8728 |  2.30491  |  black |  mid  |   Z   |
    # | 4 |  48.8644 |  2.33160  | purple |  mid  |   0   |
    # mplt.plot_markers(df)
    from mapsplotlib import mapsplot as mplt
    mplt.register_api_key("AIzaSyAXKcZ_c5WmJrl7 - GMWhsbXvzd5mfGDMh4")
    mplt.density_plot(df['latitude'], df['longitude'])
    # mplt.scatter(df['latitude'], df['longitude'], colors=df['cluster'])


def force_dataframe(col):
    if ~isinstance(col, pd.DataFrame):
        col = pd.DataFrame(col)
    return col


def force_list(col):
    if ~isinstance(col, list):
        col = [col]
    return col


def get_cols(df, pattern):
    cols = df.columns[df.columns.str.contains(pattern)]
    dfs = df[cols]
    print(dfs.info())
    return dfs


def get_num(df):
    dfs = df.select_dtypes(include=[int, float])
    return dfs


def get_cat(df):
    dfs = df.select_dtypes(include='category')
    return dfs


def cat_to_dummy(df):
    dummy = pd.get_dummies(df.select_dtypes(include='category'), prefix='is')
    dummy.columns = dummy.columns.str.lower()
    return df.join(dummy.iloc[:, 0::2])


def make_categorical(df, bindict, make_ordinal=False, right=False):

    # shared_cols = list(set(bindict.keys()) & set(df.columns.values))
    for colkey, cutvals in bindict.items():

        if colkey in list(df.columns):
            df[colkey + '_cat'] = pd.cut(
                df[colkey],
                cutvals[0],
                labels=cutvals[1],
                right=right,
                include_lowest=True
            )
            if make_ordinal:
                df[colkey + '_ord'] = df[colkey + '_cat'].cat.codes

    return df


def strjoin_columns(data, cols, sep=','):
    j = data[cols].fillna('').apply(lambda x: '{}'.format(sep).join(x), axis=1)
    return j.str.split(',').apply(lambda x: '{}'.format(sep).join(x)).str.replace(r'^,|,$', '')


def apply_transforms(df, opt='log1p'):

    dfnum = df.select_dtypes(include=[int, float])
    for col in dfnum.columns:
        if opt == 'log1p':
            dfnum[col + '_' + opt] = np.log1p(dfnum[col])
        elif opt == 'boxcox':
            dfnum[col + '_' + opt] = stats.boxcox(dfnum[col] + 1)[0]
        elif opt == 'sqrt':
            dfnum[col + '_' + opt] = np.sqrt(dfnum[col])
        else:
            print('UNRECOGNIZED TRANSFORMATION: {}', opt)
    return dfnum


def apply_exclusions(df, mindict, method='serial'):

    if method.lower() == 'serial':
        for key, val in mindict.items():
            if val:
                IDX = df[key] < val
                print_update(
                    IDX, 'Excluded users with values less than {} on "{}"'.format(val, key))
                df = df[~IDX]
    elif method.lower() == 'parallel':
        # initializes Series of boolean False values
        IDX = pd.Series(np.zeros(df.shape[0], dtype=bool))
        IDX.index = df.index
        for key, val in mindict.items():
            IDX = (IDX | (df[key].values < val))
            print_update(
                IDX, 'Number of users with values less than {} on "{}"'.format(val, key))
        print_update(IDX, 'Exluding users not meeting any of the minimums')
        df = df[~IDX]
    else:
        print('Invalid method name. Valid options are ''parallel'' & ''serial''.')

    print('N = {:,} after applying exclusions\n'.format(df.shape[0]))
    return df


def print_update(idx, description='True values in index'):

    print('{}: {:,}/{:,} ({:.2f}%)'.format(description,
                                           np.sum(idx), len(idx), 100 * (np.sum(idx) / len(idx))))

# ---------------------------------------------------------------------
#   TIMESERIES FUNCTIONS
# ---------------------------------------------------------------------


def calc_distance_from_first(df):

    df.sort_values(by='toc', inplace=True)
    if ~df.columns.contains('latlon'):
        df['latlon'] = list(zip(df.latitude, df.longitude))
    df['latitude_first'] = df.groupby(
        'user_id')['latitude'].transform(lambda x: x.iloc[0])
    df['longitude_first'] = df.groupby(
        'user_id')['longitude'].transform(lambda x: x.iloc[0])
    geoloccol = ['latitude', 'longitude']
    geoloccol0 = ['latitude_first', 'longitude_first']
    df['distance_from_first'] = df[geoloccol0 +
                                   geoloccol].apply(lambda x: great_circle((x[0], x[1]), (x[2], x[3])), axis=1)
    df['miles_from_first'] = df.distance_from_first.apply(lambda x: x.miles)
    return df


def calc_distance_array(df):

    def calc_distance(u):
        u = u.sort_values(by='toc')
        ll = u[['latitude', 'longitude']]
        idx = list(np.abs(np.diff(ll.prod(axis=1))) > 0)
        if np.sum(idx) == 0:
            return [0]
        else:
            return [great_circle(t2, t1).miles for t2, t1 in zip(ll[idx + [False]].values, ll[[False] + idx].values)]
    udistance = df.groupby('user_id').apply(calc_distance).reset_index()
    udistance.columns = ['user_id', 'distance_array']
    udistance['Total Miles Traveled'] = udistance.distance_array.apply(np.sum)
    udistance['Number of Trips > 100 Miles'] = udistance.distance_array.apply(
        lambda x: np.sum(np.array(x) > 100))
    udistance['Number of Trips > 1000 Miles'] = udistance.distance_array.apply(
        lambda x: np.sum(np.array(x) > 1000))
    return udistance


def tdeltas_to_numeric(df, units=['Days', 'Weeks', 'Months']):

    tdeltas = df.select_dtypes(include='timedelta')
    for u in units:
        newname = tdeltas.columns.values + '_' + u.lower()
        good = [dupe for dupe in newname if dupe not in df.columns]
        for col in good:
            df[col] = (tdeltas[col.replace('_' + u.lower(), '')] /
                       np.timedelta64(1, u[0])).astype(int)
    return df


def lookup(s):

    dates = {date: pd.to_datetime(date) for date in s.unique()}
    return s.map(dates)


def to_dates_lookup(s):

    fmt1 = '%Y-%m-%d %H:%M:%S %Z'
    fmt2 = '%Y-%m-%d %H:%M:%S.%f %Z'
    dates = {date: pd.to_datetime(date) for date in s.unique()}
    return s.map(dates)


def get_dt_dict(s):

    # usage: df.my_datetime.dt.year
    dt_dict = {
        'year': 'The year of the datetime',
        'month': 'The month of the datetime',
        'day': 'The days of the datetime',
        'hour': 'The hour of the datetime',
        'minute': 'The minutes of the datetime',
        'second': 'The seconds of the datetime',
        'microsecond': 'The microseconds of the datetime',
        'nanosecond': 'The nanoseconds of the datetime',
        'date': 'Returns datetime.date (does not contain timezone information)',
        'time': 'Returns datetime.time (does not contain timezone information)',
        'dayofyear': 'The ordinal day of year',
        'weekofyear': 'The week ordinal of the year',
        'week': 'The week ordinal of the year',
        'dayofweek': 'The number of the day of the week with Monday=0, Sunday=6',
        'weekday': 'The number of the day of the week with Monday=0, Sunday=6',
        'weekday_name': 'The name of the day in a week (ex: Friday)',
        'quarter': 'Quarter of the date: Jan-Mar = 1, Apr-Jun = 2, etc.'
    }
    return dt_dict


def get_datetime(df):
    dfs = df.select_dtypes(include='datetime')
    return dfs


def get_timedelta(df):
    dfs = df.select_dtypes(include='timedelta')
    return dfs


def parse_time(df):

    df['holiday_name'] = df.datestr.map(get_holiday())
    df.holiday_name.fillna('Non-Holiday', inplace=True)
    df['is_holiday'] = df.holiday_name != 'Non-Holiday'
    df['dayofweek'] = df.toc.dt.weekday_name.astype(str)
    df['hourofday'] = df.toc.dt.hour.astype(int)
    df['is_night'] = (df.hourofday > 17) | (df.hourofday < 4)
    df.loc[df.is_holiday, 'dayofweek'] = 'Holiday'
    df.loc[~df.is_holiday, 'holiday_name'] = df.loc[~df.is_holiday, 'dayofweek']
    df['is_business_hour'] = ((df.hourofday >= 8) & (df.hourofday <= 17)) & ~(df.dayofweek.str.contains(
        'Saturday') | df.dayofweek.str.contains('Sunday') | df.dayofweek.str.contains('Holiday'))
    df['is_weekend'] = ((df.dayofweek.str.contains('Friday')) & (df.hourofday > 17)) | (
        df.dayofweek.str.contains('Saturday')) | (df.dayofweek.str.contains('Sunday'))

# ---------------------------------------------------------------------
#   CORE FUNCTIONS
# ---------------------------------------------------------------------


def load_data_healthy_user_metric(datafiles, params):

    DATERANGE = params['DATERANGE']
    cf = pd.read_pickle(datafiles['captures'])
    cfcols = ['user_id', 'time_of_capture',
              'ambient_light_intensity', 'device_id']
    uf = pd.read_pickle(datafiles['users'])
    ufcols = ['user_id', 'activation_date', 'activation_device', 'os_type',
              'activation_city', 'activation_country', 'activation_region']
    uf.columns = ufcols
    idx = (cf.time_of_capture < DATERANGE[0]) | (
        cf.time_of_capture > DATERANGE[1])
    cf = cf[~idx]
    print_update(idx)
    idx = (uf.activation_date < DATERANGE[0]) | (
        uf.activation_date > DATERANGE[1])
    uf = uf[~idx]
    print_update(idx)
    uc = cf.groupby(['user_id', 'device_id']).agg(
        {'time_of_capture': ['count', 'min']}).reset_index()
    colnames = ['_'.join(col) if col[-1] else ''.join(col)
                for col in uc.columns]
    uc.columns = uc.columns.levels[1][uc.columns.labels[1]]
    uc.columns = colnames
    renamedict = {
        'time_of_capture_count': 'capture_count',
        'time_of_capture_min': 'time_of_first_capture'
    }
    uc.rename(renamedict, axis='columns', inplace=True)
    dc = pd.DataFrame(uc.groupby(['device_id'])[
                      'capture_count'].sum()).reset_index()
    dc.columns = ['device_id', 'device_count']
    uc = pd.merge(uc, dc, on=['device_id'], how='left')
    uc['proportion_total_use'] = uc.capture_count / uc.device_count
    uf = pd.merge(uf, uc, left_on='user_id', right_on='user_id', how='inner')
    idx = uf.proportion_total_use < params['PROPORTION_TOTAL_USE']
    print_update(idx, 'Excluded users with values less than {} on "{}"'.format(
        params['PROPORTION_TOTAL_USE'], 'PROPORTION_TOTAL_USE'))
    uf = uf[~idx]
    idx = uf.proportion_total_use < params['PROPORTION_TOTAL_USE']
    print_update(idx, 'Excluded users with values less than {} on "{}"'.format(
        params['PROPORTION_TOTAL_USE'], 'PROPORTION_TOTAL_USE'))
    uf = uf[~idx]

    transfer = pd.merge(cf, uf, left_on=['user_id', 'device_id'], right_on=[
                        'user_id', 'device_id'], how='inner')
    renamedict = {
        'time_of_capture': 'toc',
        'time_of_first_capture': 'toc_first'
    }
    transfer.rename(renamedict, axis='columns', inplace=True)
    transfer.sort_values(by='toc', inplace=True)
    outname = 'data/clean_capture_times_ownersonly_20180318.pickle'
    cols = ['user_id', 'device_id', 'toc',
            'toc_first', 'ambient_light_intensity']
    transfer[cols].to_pickle(outname)
    return transfer


def load_transfer_data(clean_pickle='data/clean_transfers.pickle'):

    if os.path.isfile(clean_pickle):

        transfer = pd.read_pickle(clean_pickle)
        return transfer

    else:

        # get cumulative log of users who have activated on 1 or more devices
        fn = 'data/raw/spectacles_pairing_user_device_summary_cumulative_20180220.csv'
        cols_to_use = [
            'user_id',
            'activation_time',
            'activation_device',
            'os_type',
            'app_build'
        ]
        TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
        TIMESTAMP_FORMAT_LONG = '%Y-%m-%d %H:%M:%S.%f %Z'

        def to_datetime(d): return pd.to_datetime(d, format=TIMESTAMP_FORMAT)
        df = pd.read_csv(
            fn, converters={'activation_time': to_datetime}, usecols=cols_to_use)
        # incl only rows where 'app_build' is empty
        df = df[df.app_build.isnull()].drop(['app_build'], axis=1)

        # get aggregated log data describing number of captures per day per user/device (deduped by Shiyu Zhao)
        transfer = pd.read_csv('data/transfers_deduped.csv', converters={
                               'capture_date': lambda d: pd.to_datetime(d, format='%Y-%m-%d')})
        transfer = pd.merge(transfer, df, left_on=['user_id', 'device_id'], right_on=[
                            'user_id', 'activation_device'], how='inner')
        renamedict = {
            'num_captured_count': 'device_days_used',
            'num_captured_sum': 'device_num_captures',
            'user_id_nunique': 'device_num_users'
        }
        device = transfer.groupby('device_id').agg(
            {'num_captured': ['count', 'sum'], 'user_id': pd.Series.nunique}).reset_index()
        colnames = ['_'.join(col) if col[-1] else ''.join(col)
                    for col in device.columns]
        device.columns = device.columns.levels[1][device.columns.labels[1]]
        device.columns = colnames
        device.rename(renamedict, axis='columns', inplace=True)
        transfer = pd.merge(transfer, device, left_on='device_id',
                            right_on='device_id', how='left')
        renamedict = {
            'count': 'user_days_used',
            'sum': 'user_num_captures'
        }
        user = transfer.groupby('user_id')['num_captured'].agg(
            ['sum', 'count']).reset_index().rename(renamedict, axis='columns')
        transfer = pd.merge(transfer, user, left_on='user_id',
                            right_on='user_id', how='left')
        transfer['proportion_total_use'] = transfer.user_days_used / \
            transfer.device_days_used
        df = None
        transfer['activation_date'] = transfer.activation_time.dt.floor('D')
        cols = ['user_id', 'device_id', 'proportion_total_use', 'capture_date',
                'num_captured', 'os_type', 'activation_date', 'device_num_users']
        transfer[cols].to_pickle(clean_pickle)
        return transfer


def load_user_data(transfer, clean_pickle='data/clean_user.pickle'):

    if os.path.isfile(clean_pickle):

        user = pd.read_pickle(clean_pickle)
        return user

    else:

        SPECS_LAUNCH_DATE = pd.to_datetime('2016-11-10')
        AGE_BOUNDS = [13, ]
        fname = 'data/raw/user_specs_start_date_20180130.csv'

        def to_datetime(d): return pd.to_datetime(d, format='%Y-%m-%d')
        user = pd.read_csv(fname, converters={
                           'snapchat_start_date': to_datetime, 'specs_start_date': to_datetime})
        count_cols = ['age', 'friendCount', 'sentCount',
                      'receivedCount', 'storyCount', 'snapsPaidToBeReplayedCount']
        if ~user.user_id.is_unique:
            user = user.sort_values(by=count_cols, ascending=False)
            user.drop_duplicates(subset='user_id', keep='first', inplace=True)
        user[count_cols] = user[count_cols].fillna(0).astype(int)
        user.loc[(user.age < AGE_BOUNDS[0]) | (
            user.age > AGE_BOUNDS[1]), 'age'] = np.nan
        user['snapsPaidToBeReplayedCount'] = 100 * \
            user['snapsPaidToBeReplayedCount']
        user['gender'] = user.gender.str.title().astype('category')
        user['snapchat_score'] = np.sum(user[count_cols[2:]], axis=1)
        user.columns = user.columns.str.lower()
        # N days since user joined Snapchat (rel. to Specs activation date)
        user['snapchat_tenure'] = user.specs_start_date - \
            user.snapchat_start_date
        # N days since user activated (rel. to last date in log data)
        user['specs_adoption_speed'] = user.specs_start_date - SPECS_LAUNCH_DATE
        # N days since usage activated (rel. to last date in log data)
        user['specs_time_since_activation'] = transfer.capture_date.max() - \
            user.specs_start_date
        user = tdeltas_to_numeric(user)
        user['gender'] = user.gender.str.title()
        user.to_pickle(clean_pickle)
        return user


def join_user_demos(user, demofname=os.path.join('data', 'spectacles_user_20180316_new.csv'), usecols=['user_id', 'snapchat_start_date', 'gender', 'inferred_age_bucket']):

    uf = pd.read_csv(demofname, usecols=usecols)
    uf.loc[uf.inferred_age_bucket == 'unknown', 'inferred_age_bucket'] = np.nan
    uf = uf.drop_duplicates().set_index('user_id').dropna(how='all')
    uf['snapchat_start_date'] = to_dates_lookup(uf['snapchat_start_date'])
    uf['gender'] = pd.Categorical(uf.gender)
    uf['inferred_age_bucket'] = pd.Categorical(
        uf.inferred_age_bucket, ordered=True)
    user = pd.merge(user, uf.reset_index(), on='user_id', how='left')
    return user


def load_user_windowed_timeseries(df, timewindow=84):

    vday = df.groupby('user_id')['relative_day_days'].value_counts()
    vday.index.rename(['user_id', 'day_number'], inplace=True)
    vday = vday.reset_index().sort_values(by='day_number')
    vday.columns = ['user_id', 'day', 'count']
    uday = vday.groupby('user_id')
    N_USER = len(uday)

    def to_daily_timeseries(s):
        utsmat = np.zeros((1, timewindow), dtype=int)
        utsmat[0, s['day']-1] = s['count']
        return utsmat[0]
    user_activity_ts = uday.apply(to_daily_timeseries).reset_index()
    user_activity_ts.columns = ['user_id', 'daily_activity_array']
    return user_activity_ts


def get_usage(df, uf, TIME_WINDOW_DAYS, do_exclusions=True, get_day_num_list=False):

    # Restrict by Window Starting Point
    if do_exclusions:
        TOO_EARLY = df.activation_date > df.capture_date.dt.ceil('D')
        print_update(
            TOO_EARLY, 'Excluded captures logged before device activation')
        df = df[~TOO_EARLY]
    # Restrict by Window Endpoint
    if do_exclusions:
        TOO_LATE = df.capture_date > (
            df.activation_date + pd.Timedelta(days=(TIME_WINDOW_DAYS - 1)))
        df = df[~TOO_LATE]
        print_update(TOO_LATE, 'Excluded captures logged after {} day window'.format(
            TIME_WINDOW_DAYS))
        ENOUGH_HISTORY = uf.specs_time_since_activation_days >= TIME_WINDOW_DAYS
        uf = uf[ENOUGH_HISTORY]
        print_update(~ENOUGH_HISTORY,
                     'Excluded users with insufficient historical data')
    aggregator = {
        'num_captured': ['sum', 'max', 'median', 'std'],
        'capture_date': ['count', 'max'],
    }

    um = df.groupby(['user_id', 'activation_date', 'os_type',
                     'proportion_total_use', 'device_num_users']).agg(aggregator).reset_index()
    colnames = ['_'.join(col) if col[-1] else ''.join(col)
                for col in um.columns]
    um.columns = um.columns.levels[1][um.columns.labels[1]]
    um.columns = colnames
    usage = pd.merge(um, uf, left_on='user_id',
                     right_on='user_id', how='inner')
    if get_day_num_list:
        df['day_num'] = (((df.capture_date - df.activation_date +
                           pd.Timedelta(days=1))) / np.timedelta64(1, 'D')).astype(int)
        df = df.sort_values(by=['user_id', 'day_num'])
        days_used = pd.DataFrame(df.groupby('user_id')['day_num'].apply(list))
        days_used.columns = ['days_used']
        days_used = days_used.reset_index()
        usage = pd.merge(usage, days_used, left_on='user_id',
                         right_on='user_id', how='left')

    assert usage.user_id.is_unique
    usage.num_captured_std.fillna(0, inplace=True)
    usage.sort_index(axis=1, inplace=True)
    usage['specs_tenure'] = (usage.capture_date_max -
                             usage.activation_date) + pd.Timedelta(days=1)
    usage['specs_tenure_days'] = (
        usage['specs_tenure'] / np.timedelta64(1, 'D')).astype(int)
    usage['story_to_snap_ratio'] = usage['storycount'] / usage['sentcount']
    usage.loc[usage.story_to_snap_ratio.isna(), 'story_to_snap_ratio'] = 0
    usage['snapchat_total'] = usage['storycount'] + usage['sentcount']
    usage['gender'] = usage.gender.astype('category')
    usage['os_type'] = usage.os_type.astype('category')
    usage['snapchat_tenure_days'] += 1
    for c in ['snapchat_total', 'sentcount', 'storycount', 'friendcount']:
        usage[c + '_per_day'] = usage[c] / usage['snapchat_tenure_days']
    usage = cat_to_dummy(usage)
    return usage


def apply_aggregator(df, groupby='user_id', testrun=False, timewindow=84):

    def items(x): return list(x.unique())

    def avg_diff(x): return np.mean(np.diff(x))

    def max_streak(x):
        x = np.unique(x)
        longest = 0
        current = 0
        for num in np.diff(x):
            if num == 1:
                current += 1
            else:
                longest = max(longest, current)
                current = 0
        return (max(longest, current) + 1)

    def tw_capture_count(x): return np.sum(x <= timewindow)

    def tw_capture_days(x): return x[x <= timewindow].nunique()

    def tw_capture_weeks(x): return x[x <= timewindow/7].nunique()

    def find(x): return np.array([i for i, x in enumerate(idx) if x])

    def valcounts(x):
        return(list(x.value_counts(normalize=True).sort_index()))

    def prop_is(x): return(np.sum(x) / len(x))

    def mode(x): return x.value_counts().idxmax()

    aggregator = {
        'relative_day_days': [avg_diff, max_streak, 'max', tw_capture_count, tw_capture_days],
        'relative_day_weeks': [avg_diff, max_streak, 'max', tw_capture_weeks],
        'miles_from_first': ['mean', 'median', 'std', 'max'],
        'ambient_light_intensity_cat': [mode],
        'dayofweek': [mode],
        'latlon':  ['nunique'],
        'country': ['nunique'],
        'city': ['nunique'],
        'hourofday': [mode, 'mean', 'std'],
        'hourofday_ord': [mode],
        'holiday_name': [mode],
        'is_holiday': [prop_is],
        'is_weekend': [prop_is],
        'is_business_hour': [prop_is],
        'is_night': [prop_is],
        'device_id': 'nunique'
    }

    if testrun:
        um = df.sample(
            len(df)//100).groupby(groupby).agg(aggregator).reset_index()
        colnames = ['_'.join(col) if col[-1] else ''.join(col)
                    for col in um.columns]
        um.columns = um.columns.levels[1][um.columns.labels[1]]
        um.columns = colnames
    else:
        um = df.groupby(groupby).agg(aggregator).reset_index()
        colnames = ['_'.join(col) if col[-1] else ''.join(col)
                    for col in um.columns]
        um.columns = um.columns.levels[1][um.columns.labels[1]]
        um.columns = colnames
    return um

# =====================================================================
#
# END PROGRAM
#
# =====================================================================
