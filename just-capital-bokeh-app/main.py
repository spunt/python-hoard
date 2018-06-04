import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from os import path
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.layouts import row, column, layout, widgetbox
from bokeh.models import ColumnDataSource, HoverTool, Div, CustomJS
from bokeh.models.widgets import Button, DataTable, TableColumn, NumberFormatter, Slider, Select, TextInput

# Read JUST Capital Data File(s)
cwd = path.dirname(__file__)  # Current Working Directory
# cwd = '/Users/bobspunt/Dropbox/Sync/PycharmProjects/dti-challenge-2/july/finalist-interview/webapp'
datafile = path.join(cwd, 'COMPANY_SCORES_TOP_HALF.csv')
if path.isfile(datafile):
    df = pd.read_csv(datafile)
else:
    print('Could not read datafile')

# Extract Data
jc_driver_varnames = ['PAY', 'TREAT', 'SUPPLY', 'COMM',
                      'JOBS', 'PROD', 'CUST', 'LEAD', 'ENV', 'INVEST']
# jc_driver_names = [
# 'WORKER PAY & BENEFITS',
# 'WORKER TREATMENT',
# 'SUPPLY CHAIN IMPACT',
# 'COMMUNITY WELL-BEING',
# 'DOMESTIC JOB CREATION',
# 'PRODUCT ATTRIBUTES',
# 'CUSTOMER TREATMENT',
# 'LEADERSHIP & ETHICS',
# 'ENVIRONMENTAL IMPACT',
# 'INVESTOR ALIGNMENT'
# ]
jc_driver_names = [
    'Provides Fair Pay & Benefits',
    'Treats Employees Well',
    'Protects human rights',
    'Plays a positive role in the community',
    'Creates US Jobs',
    'Makes safe & beneficial products',
    'Satisfies customers & provides good value',
    'Behaves ethically & honestly',
    'Minimizes its environmental impact',
    'Is well-governed & makes money'
]
jc_driver_names = [a.title() for a in jc_driver_names]
ndrivers = len(jc_driver_varnames)
jc_driver_scores = np.array(df[jc_driver_varnames])

jc_score = np.array(df['WGT_SCORE'])

# Compute JUST Capital Weights
lr = LinearRegression()
lr.fit(jc_driver_scores, jc_score)
jc_weights = lr.coef_
jc_weights_onetoten = np.round(100*(jc_weights/jc_weights.max()))

# Scatter Plot
source = ColumnDataSource(
    data=dict(jc_rank=[], user_rank=[], title=[], color=[], alpha=[]))
# source = ColumnDataSource(data=dict())

# source = ColumnDataSource(data=dict())
p = figure(plot_height=350, plot_width=450)
p.yaxis.axis_label = 'User Rank'
p.xaxis.axis_label = 'JUST Capital Rank'
p.title.align = 'center'
p.circle(x="jc_rank", y="user_rank", source=source, size=5, fill_alpha=0.9)

# >>>> INTERFACE <<<<<

# Read HTML document containing introductory text
intro_text = Div(text=open(path.join(cwd, 'intro.html')).read(), width=1000)

# Sliders
# - Callback for Registering Slider Changes


def slider_callback():
    user_weights = [s.value for s in sliders]
    user_weights = np.array(user_weights / np.sum(user_weights))
    user_score = np.dot(user_weights, np.transpose(jc_driver_scores))
    jc_rank = pd.Series(jc_score).rank()
    user_rank = pd.Series(user_score).rank()
    rankcorr = jc_rank.corr(user_rank, method='spearman')
    p.title.text = 'Spearman\'s rank correlation = %.2f' % rankcorr
    source.data = dict(
        jc_rank=jc_rank,
        user_rank=user_rank,
        company_name=df['id']
    )


# - Primary Callback for Updating
sliders = [None] * len(jc_driver_names)
for idx, val in enumerate(jc_driver_names):
    sliders[idx] = Slider(
        title=val, value=jc_weights_onetoten[idx], start=1, end=100, step=1)
    sliders[idx].on_change('value', lambda attr, old, new: slider_callback())

# Data Table
columns = [
    TableColumn(field="company_name", title="Company ID"),
    TableColumn(field="jc_rank", title="JUST Rank"),
    TableColumn(field="user_rank", title="User Rank"),
]
data_table = DataTable(source=source, columns=columns, width=400,
                       height=300, fit_columns=True, scroll_to_selection=False)

# Combine Layout
sizing_mode = 'fixed'  # 'scale_width' also looks nice with this example
# slider_box = column(widgetbox(*sliders, width=400, sizing_mode=sizing_mode))
slider_box1 = column(
    widgetbox(*sliders[0:5], width=425, sizing_mode=sizing_mode))
slider_box2 = column(
    widgetbox(*sliders[5:], width=425, sizing_mode=sizing_mode))
slider_box = row([slider_box1, slider_box2],
                 height=280, sizing_mode=sizing_mode)
output_box = row([p, data_table], sizing_mode=sizing_mode)
l = layout([
    [intro_text],
    [slider_box],
    [output_box]
], sizing_mode=sizing_mode)

# Initial Update
slider_callback()

curdoc().add_root(l)
curdoc().title = "JUST Rank Explorer"
