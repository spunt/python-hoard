#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#------------------
# IMPORTS
#------------------
import argparse
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from os.path import join as fullfile
from os import getcwd as pwd

# --------------------
# FUNCTIONS
# --------------------


def argument_parser(sys_argv):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Apply coding scheme to user response data for Q3 (last use)')
    parser.add_argument(
        'response_file',
        metavar='RESP_FILE',
        type=str,
        help='Path to spreadsheet (csv,xls, or xlsx) containing coded response data. If spreadsheet has multiple worksheets, make sure the worksheet of interest is first in order.',
        nargs=1)
    parser.add_argument(
        '-c',
        type=int,
        metavar='mincount',
        default=3,
        help='Integer value specifying the minimum number of times a label needs to be used to be included in the final plot.'
    )
    args = parser.parse_args(sys_argv)
    return args.response_file[0], args.c


def read_data(fname):

    if fname.endswith('.xlsx') | fname.endswith('.xls'):
        df = pd.read_excel(fname, keep_default_na=False, na_values=[''])
    elif fname.endswith('.csv'):
        df = pd.read_csv(fname, keep_default_na=False, na_values=[''])
    else:
        print('Data file must be xlsx, xls, or csv. Exiting.')
        sys.exit(1)
    df.columns = df.columns.str.strip().str.lower()
    df.replace(r'^\s+$', np.nan, inplace=True, regex=True)
    df = df.dropna(how='all')
    print('\nN empty cells:')
    print(np.sum(df.isna()))
    return df


def unpack_codes(df):

    assert 'codes' in df.columns.values
    assert 'resp' in df.columns.values

    n_na = np.sum(df.codes.isna())
    if n_na:
        print(str(n_na) + ' responses have no valid code. Dropping...\n')
        df.dropna(how='all', subset=['codes'], inplace=True)

    df.fillna(value='', inplace=True)
    df['codes'] = df.codes.astype(str).str.strip().str.lower().str.replace(
        ';', ',').str.split(',')

    dfrep = df.set_index(['resp'])['codes'].apply(pd.Series).stack()
    dfrep = dfrep.reset_index()
    dfrep.drop(columns=['level_1'], inplace=True)
    dfrep.columns = ['resp', 'code']
    dfrep['code'] = dfrep.code.str.strip()
    dfrep['resp'] = dfrep.resp.str.strip().str.lower()
    return dfrep


def get_freq(df, colname):

    print('\n' + '-' * len(colname) + '\n' + colname.upper() + '\n' + '-' * len(colname))
    n_na_code = np.sum(df[colname].isna())
    if n_na_code:
        print('\n' + str(n_na_code) + ' responses found with no code in the "' + colname + '"" column. Dropping...')
        df.dropna(subset=[colname], inplace=True)
    df[colname] = df[colname].astype(str).str.strip().str.lower().str.replace(
        ';', ',').str.split(',')
    df = df.set_index(['resp'])[colname].apply(pd.Series).stack()
    df = df.reset_index()
    df.drop(columns=['level_1'], inplace=True)
    df.columns = ['resp', 'code']
    df['count'] = df.groupby('code')['code'].transform('count')
    df.sort_values(by='count', ascending=False, inplace=True)

    freq = pd.DataFrame(df['code'].value_counts().reset_index())
    freq.columns = ['code', 'count']
    if mincount > 1:
        freq['count'].replace(np.arange(mincount), np.nan, inplace=True)
        n_submin_code = np.sum(freq['count'].isna())
        print(str(n_submin_code) + ' responses found with count less than ' + str(mincount) + ' in the "' + colname + '"" column. Dropping...\n')
        freq.dropna(subset=['count'], inplace=True)
        df['count'].replace(np.arange(mincount), np.nan, inplace=True)
        df.dropna(subset=['count'], inplace=True)

    # write_to_excel(df, colname + '.xlsx')
    print(freq)
    return freq


def write_to_excel(codedresp, outname):

    writer = pd.ExcelWriter(outname)
    codedresp.set_index('code').to_excel(writer, sheet_name='coded_diff_row')
    codedresp.groupby('code').head().set_index('code').to_excel(writer, sheet_name='examples')
    writer.save()
    print('Results written to: ' + outname)


def annotate_plot(ax, fontsize):

    yloc = ax.yaxis.get_ticklocs()
    labelpad = ax.get_xlim()[-1] * .005

    for y, p in enumerate(ax.patches):
        width = p.get_width()
        height = yloc[y]
        ax.text(width + labelpad, height, '{}'.format(int(width)), fontsize=fontsize, va='center')


def save_plot(figh, outname):
    figh.tight_layout()
    figh.savefig(
        outname,
        dpi=300,
        papertype=None,
        format=None,
        transparent=True,
        bbox_inches=None,
        pad_inches=0.1,
        frameon=None)
    plt.close()
    print('\nFIGURE SAVED TO: ' + outname)


def plot_freq(df, label, ylabel):

    palette = 'coolwarm_r'
    sns.set_color_codes("pastel")
    xlabel = 'Count'
    axisfontsize = 21
    tickfontsize = 16
    height_inches = 8
    width_inches = (16 / 9) * 6
    image_format = 'png'
    sns.set(style="ticks")
    # --------------
    ax = sns.barplot(y='code', x='count', data=df, label=label, color='b')
    plt.gcf().set_size_inches(h=height_inches, w=width_inches)
    ax.set_xlabel('Count', fontsize=axisfontsize)
    ax.set_ylabel(ylabel, fontsize=axisfontsize)
    ax.set_xlim(np.ceil(ax.get_xlim()))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.tick_params(labelsize=tickfontsize)
    annotate_plot(ax, tickfontsize * .90)
    save_plot(plt.gcf(), fullfile(pwd(), label + '.' + image_format))


# --------------------
# MAIN PROGRAM
# --------------------
if __name__ == "__main__":

    # Parse arguments
    resp_file, mincount = argument_parser(sys.argv[1:])

    # Read response data file
    df = read_data(resp_file)
    df['id'] = df.index
    df.rename(
        {
            'raw_resp': 'resp',
            'raw': 'resp',
            'response': 'resp',
            'responses': 'resp'
        },
        axis='columns',
        inplace=True)
    assert 'resp' in df.columns.values
    assert 'when' in df.columns.values
    assert 'activity' in df.columns.values
    assert 'location' in df.columns.values
    print('\n\nUser N = ' + str(df.shape[0]))

    # When
    colname = 'Time Since Last Use'
    print('\n' + '-' * len(colname) + '\n' + colname.upper() + '\n' + '-' * len(colname))
    freq_when = pd.DataFrame(df['when'].value_counts().reset_index())
    mapping = {
        'Today': 1,
        'Yesterday': 2,
        'Sometime this week': 3,
        'Last week': 4,
        '2-3 weeks ago': 5,
        '1-2 months ago': 6,
        '3+ months ago': 7,
    }
    freq_when.columns = ['code', 'count']
    freq_when['order'] = freq_when.code
    freq_when['order'] = freq_when.replace({'code': mapping})
    freq_when.sort_values(by='order', inplace=True)
    question = 'When was the last time you used your Spectacles - Time Since Last Use'
    print(freq_when)
    plot_freq(freq_when, question, 'Time Since Last Use')

    # ACTIVITY
    question = "What was the last occasion when you used your Spectacles - Activity"
    freq_activity = get_freq(df.copy(), 'activity')
    plot_freq(freq_activity, question, 'Activity')

    # LOCATION
    question = "What was the last occasion when you used your Spectacles - Location"
    freq_location = get_freq(df, 'location')
    plot_freq(freq_location, question, 'Location')

    print('\nAll done.\n')
