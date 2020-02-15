
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
from output_gen import load_dictionary, painter

'''
We found a relation of interest between Exxon and the dowj index,
 the patterns are the following
((20, (4,)), (27, (2,)))
((20, (3,)), (27, (3,)))
((20, (3,)), (27, (2,)))
((20, (2,)), (27, (2,)))

also explore

((18, (3,)), (20, (4,)), (24, (3, 2)))	51	4	2
((12, (3,)), (14, (4,)), (20, (4,)), (22, (3,)), (27, (3,)))	48	5	1
'''
#%%

d = load_dictionary('./output/dowj_5y_close.dict')
ct = { k:v for k,v in d.items() if v[1]>1}
ct_df = pd.DataFrame.from_dict(ct,
        orient='index',columns=['Support',
        'Length','Time'])

#%%
st, d = import_dat('./output/dowj_5y_close.dat')
#%%
d_og = d

ct = st.copy()

#this gives 42% coverage of line 20 and 27`
ct = add(((20, (4,)), (27, (2,))),ct,d)
ct = add(((20, (3,)), (27, (3,))),ct,d)
ct = add(((20, (3,)), (27, (2,))),ct,d)
ct = add(((20, (2,)), (27, (2,))),ct,d)


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
df2 = pd.read_excel('./output/dowj_5y_close.xlsx')
df2['Date'] = pd.to_datetime(df2['Date'])
df2['ToolTipDates'] = df2.Date.map(lambda x: x.strftime("%d %b %y"))
df2['dowjclose'] = list(pd.read_csv('./Stocks/1ndex_DOW.csv').iloc[-1500:,:]['Close'])
df2['XOMclose'] = list(pd.read_csv('./Stocks/XOM.csv').iloc[-1500:,:]['Close'])
df2['patterns'] = d2[20]


config = { 
          #Red
          ((20, (4,)), (27, (2,))):'crimson', 
          #Orange
          ((20, (3,)), (27, (3,))):'gold', 
          #Cyan blue
          ((20, (3,)), (27, (2,))):'lawngreen',
          #Red
          ((20, (2,)), (27, (2,))):'deepskyblue',
 'None':'#f1f1f1'}


config2 = { 
          #Red
          ((20, (4,)), (27, (2,))):'red', 
          #Orange
          ((20, (3,)), (27, (3,))):'red', 
          #Cyan blue
          ((20, (3,)), (27, (2,))):'red',
          #Red
          ((20, (2,)), (27, (2,))):'red',
 'None':'#f1f1f1'}
df2['colors'] = [config[x] for x in d2[20]]


# %%
def xyc(df2,date,data,color):
    xs=[]
    ys=[]
    x=[df2.iloc[0,:][date]]
    y=[df2.iloc[0,:][data]]
    c=[df2.iloc[0,:][color]]

    for row in df2.iterrows():
        row=row[1]
        if not c[-1] == row[color]:
            xs.append(x)
            ys.append(y)
            
            c.append(row[color])

            x=[x[-1]]
            y=[y[-1]]

        y.append(row[data])
        x.append(row[date])


    xs.append(x)
    ys.append(y)
    return xs,ys,c



dowj = xyc(df2,'Date','dowjclose','colors')
xom = xyc(df2,'Date','XOMclose','colors')
df2['labdowj']= df2['Close-1ndex_DOW_-LB']
df2['labXOM']= df2['Close-XOM_-LB']
df2['patstr']= [ str(x) for x in df2['patterns']]
source2 = ColumnDataSource(df2)



output_file('DOWJEXXON_red.html')


p = figure(x_axis_type='datetime' ,plot_width=1440, plot_height=600,
            title="DowJones index & Exxon (4 patterns)")


p.circle(x='Date', y='dowjclose',name='dowj', alpha=0,
         source=source2,size=3)


p.circle(x='Date', y='XOMclose',name='xom', alpha=0,
         source=source2,size=3,
             y_range_name='foo')


# Setting the second y axis range name and range
p.extra_y_ranges = {"foo": Range1d(start=50, end=150)}

# Adding the second axis to the plot.  
p.add_layout(LinearAxis(y_range_name="foo"), 'right')

p.multi_line(name='bill',
             xs=xom[0],
             ys=xom[1],
             color=xom[2],
             line_width=3,
             y_range_name='foo')

p.multi_line(name='steve',
             xs=dowj[0], 
             ys=dowj[1],
             color=dowj[2],
             line_width=3)


p.add_tools(HoverTool(names=['dowj'],
                      mode = "vline",
                      line_policy='nearest',
                      point_policy='snap_to_data',
                                tooltips=[

                                ]))



p.add_tools(HoverTool(names=['xom'],
                      mode = "vline",
                      line_policy='nearest',
                      point_policy='snap_to_data',
                                tooltips=[
                                ('Date : ','@ToolTipDates'),

                                ('Close DowJones : ','@dowjclose'),
                                ('Close Exxon : ','@XOMclose'),

                                ('Label Dowjones : ','@labdowj'),
                                ('Label Exxon : ','@labXOM'),
                                ('Pattern : ','@patstr')



                                ]))
p.toolbar.logo = None


show(p)

# %%
