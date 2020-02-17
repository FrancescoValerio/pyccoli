from input_gen import example5
# We need to put this in a function to allow python multiprocessing
# to work.

def make_files():
    """
        Make all the files that we'll need for PYCCOLI
    """

    example5()

#Now that we have the files we can run PYCCOLI

from pyccoli import pyccoli
def run_pyccoli():
    pyccoli('ixdow_5y_close')

#Uncomment to run pyccoli
'''
if __name__ == "__main__":
    make_files()
    run_pyccoli()
'''

'''
These results confirm the idea we had in the previous
comparison between data taken from an index and data
mined on itself, data from an index hides patterns because 
overlap isnt allowed and thus shows the most important 
patterns. In effect, our analysis is very rigid and harsh
but we already  knew that because we dont allow gaps
and dont allow any combination that isnt on the first index
that being said, if we already find this many patterns 
we should only find many more much better ways to krimp the
data if we allow our algorithm more shapeful patterns
'''

#%%
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
ct = load_dictionary('./output/workbook10/ixdow_5y_close.dict')
# Remove the singletons
ct = {k:v for k,v in ct.items() if v[1]>1} 
# Turn it into a dataframe
ct_df = pd.DataFrame()
ct_df['index'] = list(ct.keys())
ct_df['value'] = list(ct.values())
ct_df['Support'] = [ct_df.iloc[i,1][0] for i in range(len(ct_df))]
ct_df['Length'] = [ct_df.iloc[i,1][1] for i in range(len(ct_df))]
ct_df['Time'] = [ct_df.iloc[i,1][2] for i in range(len(ct_df))]
del ct_df['value']
ct_df = ct_df.set_index('index')
#Now we sort it based on support
ct_df = ct_df.sort_values('Support')[::-1]


st, d = import_dat('./output/workbook10/ixdow_5y_close.dat')

d_og = d

ct = st.copy()

#this gives  33% coverage of line 0 and 1
ct = add(list(ct_df.index)[0],ct,d)
ct = add(list(ct_df.index)[1],ct,d)
ct = add(list(ct_df.index)[2],ct,d)
ct = add(list(ct_df.index)[3],ct,d)
ct = add(list(ct_df.index)[4],ct,d)


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


df2 = pd.read_excel('./output/workbook10/ixdow_5y_close.xlsx')
df2['Date'] = pd.to_datetime(df2['Date'])
df2['ToolTipDates'] = df2.Date.map(lambda x: x.strftime("%d %b %y"))

df2['IBMclose'] = list(pd.read_csv('./Stocks/IBM.csv'
                                   ).iloc[-1500:,:]['Close'])

df2['XOMclose'] = list(pd.read_csv('./Stocks/XOM.csv'
                                   ).iloc[-1500:,:]['Close'])

df2['DOWclose'] = list(pd.read_csv('./Stocks/1ndex_DOW.csv'
                                        ).iloc[-1500:,:]['Close'])

df2['IBMpatterns'] = [str(x) for x in d2[0]]
df2['XOMpatterns'] = [str(x) for x in d2[1]]
df2['DOWpatterns'] = [str(x) for x in d2[2]]

colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', 
          '#42d4f4', '#f032e6',  '#e6beff', '#9A6324', 
           '#800000',  '#000075']

config = { 
          #Red
          list(ct_df.index)[0]:colors[0], 
          #Orange
          list(ct_df.index)[1]:colors[1], 
          #Cyan blue
          list(ct_df.index)[2]:colors[2],
          #Red
          list(ct_df.index)[3]:colors[3],
          list(ct_df.index)[4]:colors[4],
 'None':'#f1f1f1'}
df2['IBMcolors'] = [config[x] for x in d2[0]]
df2['XOMcolors'] = [config[x] for x in d2[1]]
df2['DOWcolors'] = [config[x] for x in d2[2]]




ibm = xyc(df2,'Date','IBMclose','IBMcolors')
xom = xyc(df2,'Date','XOMclose','XOMcolors')
dow = xyc(df2,'Date','DOWclose','DOWcolors')

df2['labIBM']= df2['Close-IBM_-LB']
df2['labXOM']= df2['Close-XOM_-LB']
df2['labDOW']= df2['Close-1ndex_DOW_-LB']


source2 = ColumnDataSource(df2)


output_file('idex.html')


p = figure(x_axis_type='datetime' ,plot_width=1440, plot_height=600,
            title="Dowjones Index, IBM, Exxon Mobile (5 patterns)")


p.circle(x='Date', y='IBMclose',name='ibm', alpha=0,
         source=source2,size=3,
             y_range_name='foo')


p.circle(x='Date', y='XOMclose',name='xom', alpha=0,
         source=source2,size=3,
             y_range_name='foo')


p.circle(x='Date', y='DOWclose',name='dow', alpha=0,
         source=source2,size=3)
p.extra_y_ranges = {"foo": Range1d(start=10, end=210)}

# Adding the second axis to the plot.  
p.add_layout(LinearAxis(y_range_name="foo"), 'right')


p.multi_line(name='bill',
             xs=xom[0],
             ys=xom[1],
             color=xom[2],
             line_width=3,
             y_range_name='foo')


p.multi_line(name='steve',
             xs=dow[0], 
             ys=dow[1],
             color=dow[2],
             line_width=3)


p.multi_line(name='bill',
             xs=ibm[0],
             ys=ibm[1],
             color=ibm[2],
             line_width=3,
             y_range_name='foo')


p.add_tools(HoverTool(names=['dow'],
                      mode = "vline",
                      line_policy='nearest',
                      point_policy='snap_to_data',
                                tooltips=[

                                ]))



p.add_tools(HoverTool(names=['dow'],
                      mode = "vline",
                      line_policy='nearest',
                      point_policy='snap_to_data',
                                tooltips=[
                                ('Date : ','@ToolTipDates'),

                                ('Close DowJ index : ','@{DOWclose}{0.2f}'),

                                ('Label DowJ index : ','@labDOW'),
                                ('Pattern : ','@DOWpatterns')



                                ]))
p.add_tools(HoverTool(names=['xom'],
                      mode = "vline",
                      line_policy='nearest',
                      point_policy='snap_to_data',
                                tooltips=[
                                ('Date : ','@ToolTipDates'),

                                ('Close Exxon : ','@XOMclose'),

                                ('Label Exxon : ','@labXOM'),
                                ('Pattern : ','@XOMpatterns')



                                ]))


p.add_tools(HoverTool(names=['ibm'],
                      mode = "vline",
                      line_policy='nearest',
                      point_policy='snap_to_data',
                                tooltips=[
                                ('Date : ','@ToolTipDates'),

                                ('Close Exxon : ','@IBMclose'),

                                ('Label Exxon : ','@labIBM'),
                                ('Pattern : ','@IBMpatterns')



                                ]))


p.toolbar.logo = None

show(p)


# %%
