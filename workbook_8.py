#%%
import pandas as pd
from input_gen import row_diff, kmean_columns, export_to_pyccoli, filter_columns
from pyccoli import pyccoli

# %%
#An example of how to use PYCCOLI for your own time series
# in this case we are looking at bitcoin data from 2016 till 2020
def make_the_file():
    data = pd.read_csv('./Stocks/1Bitcoin4y.csv')
    date = pd.to_datetime(data['<DATE>'],format= '%Y%m%d')
    del data['<TIME>']
    data = row_diff(data)
    data = kmean_columns(data,5)
    data['<DATE>'] = date
    del data['<DATE>_-LB']
    data.to_excel('bitcoin2016.xlsx')

    export_to_pyccoli(filter_columns(data,'LB'), 'bitcoin2016')

# %%
def run_pyccoli():
    pyccoli('bitcoin2016')

#then do 
#make_the_file
#run_pyccoli
'''
if __name__ == "__main__":
    run_pyccoli()
'''

import numpy as np
import pandas as pd
from bokeh.io import curdoc, show
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Grid, HoverTool, LinearAxis, Range1d
from bokeh.models.glyphs import MultiLine
from bokeh.plotting import figure, output_file, show

from add_rem import add
from cover import cov_order
from import_data import import_dat
from output_gen import load_dictionary, painter, xyc
from pattern_finder import finder

# Load the dictionary to see the patterns
btc_dict = load_dictionary('./output/workbook8/bitcoin2016.dict')
# Remove the singletons
btc_dict = {k:v for k,v in btc_dict.items() if v[1]>1} 
# Turn it into a dataframe
df = pd.DataFrame.from_dict(btc_dict, orient='Index',
                            columns=['Support','Length','Time'])
# Sort them by support
df = df.sort_values(by='Support')[::-1]
st, d = import_dat('./output/workbook8/bitcoin2016.dat')
ct = st.copy()


for key in list(df.index[:10]):
    ct = add(key,ct,d)
    #patterns[key]=value
    

patterns = {}
for key, value in ct.items():
    if value[1]>1:
        patterns[key]=value

ordered_p = cov_order(patterns)

val_d ={}
sign = -100
for x in ordered_p:
    # 'Paint' the dataset with 0's where covered and return p amount
    d = painter(x,d,sign)
    val_d[sign] = x
    sign *= 2


d2 = [[val_d[x] if x in val_d else 'None' for x in row]for row in d]
df2 = pd.read_excel('./output/workbook8/bitcoin2016.xlsx')
df2['Date'] = pd.to_datetime(df2['<DATE>'])
df2['ToolTipDates'] = df2.Date.map(lambda x: x.strftime("%d %b %y"))

#%%
colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', 
          '#42d4f4', '#f032e6',  '#e6beff', '#9A6324', 
           '#800000',  '#000075']
P_TO_COLOR = { x:colors[i] for i,x in enumerate(patterns)}
P_TO_COLOR['None'] = '#f1f1f1'

# Add original values
og_v = pd.read_csv('./Stocks/1Bitcoin4y.csv').iloc[:,2:]
for i,x in enumerate(og_v):
    df2[f'og{x}'] = og_v[x]
    df2[f'pattern{x}'] = [str(x) for x in d2[i]]
    df2[f'color{x}'] = [P_TO_COLOR[x] for x in d2[i]]

#for every column we generate the line we need
open_ = xyc(df2,'Date','og<OPEN>','color<OPEN>')
high_ = xyc(df2,'Date','og<HIGH>','color<HIGH>')
low_ = xyc(df2,'Date','og<LOW>','color<LOW>')
close_ = xyc(df2,'Date','og<CLOSE>','color<CLOSE>')
vol_ = xyc(df2,'Date','og<VOL>','color<VOL>')

df2['labOPEN']= df2['pattern<OPEN>']
df2['labHIGH']= df2['pattern<HIGH>']
df2['labLOW']= df2['pattern<LOW>']
df2['labCLOSE']= df2['pattern<CLOSE>']
df2['labVOL']= df2['pattern<VOL>']

#%%

source2 = ColumnDataSource(df2)



output_file('bitcoindaily.html')



p = figure(x_axis_type='datetime' ,plot_width=1440, plot_height=600,
            title="Bitcoin Stock Price")


p.circle(x='Date', y='og<OPEN>',name='open', alpha=0,
         source=source2,size=3)
p.circle(x='Date', y='og<CLOSE>',name='close', alpha=0,
         source=source2,size=3)

p.circle(x='Date', y='og<HIGH>',name='high', alpha=0,
         source=source2,size=3)


p.circle(x='Date', y='og<LOW>',name='low', alpha=0,
         source=source2,size=3)



p.multi_line(name='q',
             xs=open_[0], 
             ys=open_[1],
             color=open_[2],
             line_width=3)
p.multi_line(name='e',
             xs=high_[0], 
             ys=high_[1],
             color=high_[2],
             line_width=3)
p.multi_line(name='ee',
             xs=low_[0], 
             ys=low_[1],
             color=low_[2],
             line_width=3)
p.multi_line(name='w',
             xs=close_[0], 
             ys=close_[1],
             color=close_[2],
             line_width=3)
q = figure(x_range=p.x_range,x_axis_type='datetime'  ,plot_width=1440, plot_height=200,
            title="Stock Volume",y_axis_type='linear')

q.circle(x='Date', y='og<VOL>',name='VOL', alpha=0,
         source=source2,size=3)
p.circle(x='Date', y='og<LOW>',name='low', alpha=0,
         source=source2,size=3)


q.multi_line(name='qw',
             xs=vol_[0], 
             ys=vol_[1],
             color=vol_[2],
             line_width=3)


p.add_tools(HoverTool(names=['low'],
                      mode = "vline",
                      line_policy='nearest',
                      point_policy='snap_to_data',
                                tooltips=[
                                ('Date : ','@ToolTipDates'),
                                ('Low Price : ','@{og<LOW>}{0.2f}'),
                                ('Low Pattern : ','@labLOW'),
                                ('High Price : ','@{og<HIGH>}{0.2f}'),
                                ('High Pattern : ','@labHIGH'),
                                ('Open Price : ','@{og<OPEN>}{0.2f}'),
                                ('Open Pattern : ','@labOPEN'),
                                ('Close Price : ','@{og<CLOSE>}{0.2f}'),
                                ('Close Pattern : ','@labCLOSE'),
                                                                
                                ]))


p.add_tools(HoverTool(names=['open'],
                      mode = "vline",
                      line_policy='nearest',
                      point_policy='snap_to_data',
                                tooltips=[
                                ('Name','Open'),
                                ]))
p.add_tools(HoverTool(names=['close'],
                      mode = "vline",
                      line_policy='nearest',
                      point_policy='snap_to_data',
                                tooltips=[
                                ('Name','Close'),
                                ]))

p.add_tools(HoverTool(names=['high'],
                      mode = "vline",
                      line_policy='nearest',
                      point_policy='snap_to_data',
                                tooltips=[
                                ('Name','High'),
                                ]))
p.add_tools(HoverTool(names=['low'],
                      mode = "vline",
                      line_policy='nearest',
                      point_policy='snap_to_data',
                                tooltips=[
                                ('Name','Low'),
                                ]))

q.add_tools(HoverTool(names=['VOL'],
                      mode = "vline",
                      line_policy='nearest',
                      point_policy='snap_to_data',
                                tooltips=[
                                ('Date : ','@ToolTipDates'),
                                ('High Price : ','@{og<VOL>}{0.2f}'),
                                ('High Pattern : ','@labVOL'),
                                ]))
show(column(p,q))

# %%
