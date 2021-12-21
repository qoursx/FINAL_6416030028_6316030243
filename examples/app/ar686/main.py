''' A weather chart for three cities using a csv file.
This illustration demonstrates different interpretation of the same data
with the distribution option.

.. note::
    This example needs the Scipy and Pandas package to run. See
    ``README.md`` for more information.

'''
import datetime
from os.path import dirname, join

import pandas as pd
from scipy.signal import savgol_filter

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, DataRange1d, Select
from bokeh.palettes import Blues4
from bokeh.plotting import figure
from bokeh.layouts import gridplot


def get_dataset(src, name):
    df = src[src.COUNTRY == name].copy()
    del df['COUNTRY']
    df['DATE'] = pd.to_datetime(df.DATE)
    # timedelta here instead of pd.DateOffset to avoid pandas bug < 0.18 (Pandas issue #11925)
    # df['left'] = df.date - datetime.timedelta(days=0.5)
    # df['right'] = df.date + datetime.timedelta(days=0.5)
    df = df.set_index(['DATE'])

    return ColumnDataSource(data=df)

def make_plot(source, title):
  plot = figure(x_axis_type="datetime", width=1500, tools="", toolbar_location=None)
  plot.title.text = title

  plot.line(x='DATE', y='VALUE', source=source)
  # fixed attributes
  plot.xaxis.axis_label = None
  plot.yaxis.axis_label = "Value"
  plot.axis.axis_label_text_font_style = "bold"
  plot.x_range = DataRange1d(range_padding=0.0)
  plot.grid.grid_line_alpha = 0.4

  return plot

def make_plot_cases(source, title):
  plot_cases = figure(x_axis_type="datetime", width=1500, tools="", toolbar_location=None)
  plot_cases.title.text = title

  plot_cases.line(x='DATE', y='CASES', source=source)
  # fixed attributes
  plot_cases.xaxis.axis_label = None
  plot_cases.yaxis.axis_label = "Cases"
  plot_cases.axis.axis_label_text_font_style = "bold"
  plot_cases.x_range = DataRange1d(range_padding=0.0)
  plot_cases.grid.grid_line_alpha = 0.4

  return plot_cases

def update_plot(attrname, old, new):
    city = country_select.value
    plot.title.text = "Exchange Rate : " + country[city]['title']

    src = get_dataset(df, country[city]['COUNTRY'])
    source.data.update(src.data)

city = 'Japan'

country = {
    'Japan': {
        'COUNTRY': 'Japan',
        'title': 'Japan',
    },
    'South Korea': {
        'COUNTRY': 'Korea',
        'title': 'South Korea',
    },
    'Hong Kong': {
        'COUNTRY': 'Hong Kong',
        'title': 'Hong Kong',
    },
    'Singapore': {
        'COUNTRY': 'Singapore',
        'title': 'Singapore',
    },
    'Taiwan': {
        'COUNTRY': 'Taiwan',
        'title': 'Taiwan',
    },
    'China': {
        'COUNTRY': 'China',
        'title': 'China',
    },
}

def update_plot_cases(attrname, old, new):
    city = country_select.value
    plot_cases.title.text = "Coronavirus [New Cases] : " + country[city]['title']

    src = get_dataset(df, country[city]['COUNTRY'])
    source.data.update(src.data)

city = 'Japan'

country = {
    'Japan': {
        'COUNTRY': 'Japan',
        'title': 'No.1 Japan',
    },
    'South Korea': {
        'COUNTRY': 'Korea',
        'title': 'No.2 South Korea',
    },
    'Hong Kong': {
        'COUNTRY': 'Hong Kong',
        'title': 'No.3 Hong Kong',
    },
    'Singapore': {
        'COUNTRY': 'Singapore',
        'title': 'No.4 Singapore',
    },
    'Taiwan': {
        'COUNTRY': 'Taiwan',
        'title': 'No.5 Taiwan',
    },
    'China': {
        'COUNTRY': 'China',
        'title': 'No.6 China',
    },
}

country_select = Select(value=city, title='COUNTRY', options=sorted(country.keys()))
country_select_cases = Select(value=city, title='COUNTRY', options=sorted(country.keys()))

df = pd.read_excel(join(dirname(__file__), 'data/686 FINAL.xlsx'), sheet_name=0)
source = get_dataset(df, country[city]['COUNTRY'])
plot = make_plot(source, "Exchange Rate : " + country[city]['title'])
plot_cases = make_plot_cases(source, "Coronavirus [New Cases] : " + country[city]['title'])


country_select.on_change('value', update_plot, update_plot_cases)
# country_select_cases.on_change('value', update_plot_cases)


controls = column(country_select)
# controls_cases = column(country_select_cases)


curdoc().add_root(gridplot([[row(plot, controls)],[row(plot_cases)]]))
curdoc().title = "AR686"
