#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Type <function_name> -h for help
'''

#------------------
# IMPORTS
#------------------
import argparse
import sys
import pandas as pd
import numpy as np
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
        description='''

    Apply coding scheme to user response data and generate count plots.

        -------------------------------
        Data Formatting Guidelines
        -------------------------------

        - spreadsheet must contain AT LEAST two columns of text data
            + text of user responses
            + comma-separated codes for each response

        - the first row of the spreadsheet is a header containing the column names.
            + valid names response column: responses, response, resp, row
            + valid names for codes column: codes, code, tag, tags
            + naming is case-insensitive

        - use commas (",") to separate multiple codes for the same response

        - use dashes ("-") to separate coding levels within a code
            + levels decrease from left to right (e.g., level 1-level2)

        - empty codes are OK and are ignored

        - for example, first 3 rows of a properly formatted coding sheet:

            | resp                       | codes                         |
            |----------------------------|-------------------------------|
            | video quality sucks        | capturing-video quality       |
            | battery life; not my style | charging-battery,frames-style |

        ''')
    parser.add_argument(
        'response_file',
        metavar='RESP_FILE',
        type=str,
        help='Path to spreadsheet (csv,xls, or xlsx) containing coded response data. If spreadsheet has multiple worksheets, make sure the worksheet of interest is first in order.',
        nargs=1)
    parser.add_argument(
        '-f',
        action='store_true',
        help='Option to plot as a flat coding scheme, even if the default level separator (dash, "-") is present in the coding labels'
    )
    parser.add_argument(
        '-q',
        type=str,
        metavar='question',
        default='open-ended feedback',
        help='Text of the question users were answering. Used to name output filenames.'
    )
    args = parser.parse_args(sys_argv)
    return args.response_file[0], args.f, args.q


def read_data(fname):

    if fname.endswith('.xlsx') | fname.endswith('.xls'):
        df = pd.read_excel(fname, keep_default_na=False, na_values=[''])
    elif fname.endswith('.csv'):
        df = pd.read_csv(fname, keep_default_na=False, na_values=[''])
    else:
        print('Data file must be xlsx, xls, or csv. Exiting.')
        sys.exit(1)
    df.columns = df.columns.str.strip().str.lower()
    df = df.dropna(how='all')
    print('\nN empty cells:')
    print(np.sum(df.isna()))
    return df


def pack_codes(df):

    g = df.groupby('id')
    # dfc = pd.DataFrame(g[['resp', 'cleantag']].first())
    dfc = pd.DataFrame(g[['resp']].first())
    dfc['code'] = pd.DataFrame(g.code.apply(', '.join))
    return dfc


def unpack_codes(df):

    df.rename(
        {
            'tag': 'codes',
            'tags': 'codes',
            'code': 'codes',
            'raw': 'resp',
            'response': 'resp',
            'responses': 'resp'
        },
        axis='columns',
        inplace=True)
    assert 'codes' in df.columns.values
    assert 'resp' in df.columns.values
    n_na = np.sum(df.codes.isna())
    if n_na:
        print(str(n_na) + ' responses have no valid code. Dropping...\n')
        df.dropna(how='all', subset=['codes'], inplace=True)
    df['codes'] = df.codes.astype(str).str.strip().str.lower().str.replace(
        ';', ',').str.split(',')
    dfrep = df.set_index(['resp'])['codes'].apply(pd.Series).stack()
    dfrep = dfrep.reset_index()
    dfrep.drop(columns=['level_1'], inplace=True)
    dfrep.columns = ['resp', 'code']
    dfrep['code'] = dfrep.code.str.strip()
    dfrep['resp'] = dfrep.resp.str.strip().str.lower()
    return dfrep


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
    resp_file, flatflag, question = argument_parser(sys.argv[1:])

    # Read response data file
    resp = read_data(resp_file)
    print('\n\nUser N = ' + str(resp.shape[0]))
    resp = unpack_codes(resp)

    # Get frequencies
    if flatflag:
        freq = pd.DataFrame(resp.code.value_counts().reset_index())
    else:
        resp[['level1', 'level2']] = resp.code.str.split('-', expand=True)
        freq = pd.DataFrame(resp.level1.value_counts().reset_index())

    freq.columns = ['code', 'count']
    print(freq)
    plot_freq(freq, question, 'Response Category')
    if not flatflag:
        freqsub = pd.DataFrame(
            resp.groupby('level1')['level2'].value_counts().rename(
                'count')).reset_index()
        freqsub.columns = ['category', 'code', 'count']
        for cat in freqsub.category.unique():
            outname = question + ' - ' + cat
            outname = outname.replace('/', ' & ')
            print('\n' + cat.upper() + '\n')
            print(freqsub.loc[freqsub.category == cat, ['code', 'count']])
            plot_freq(freqsub[freqsub.category == cat], outname,
                      'Response Subcategory')

    print('\nAll done.\n')
