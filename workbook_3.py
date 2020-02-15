'''

Observation, most stocks within the dowj jones index seem to flow 
together, that is what can not only be seen from the top patterns
but also further down. Stocks seem to all head in one way, regardless
of their industry (for most of the time). They also seem to either
contribute or be pushed by movements in the dow jones

This all seems obvious but machine learning arriving at this 
by itself is no trivial conclusion

Further note, the proning straight after expanding may be great 
for computations but most likely severly impacts findings patterns
take the pattern ((1, (4,)), (2, (4,))) and 
((1, (4,)), (2, (4,)),(3, (4,))) if the former start taking too much 
space due to inclusion of the lattern there still may be new combinations
further down the road that only fit the ((1, (4,)), (2, (4,))) 
and not the 3 part. In essence, pruning so early forces the algorithm 
to always head down branches rather than to explore the whole tree
of possibilities



Now for workbook 4 we will forcefull match UNH and mcdonalds with the 
following patterns:


((1, (4,)), (2, (4,)))
((1, (4,)), (2, (3,)))
((1, (2,)), (2, (4,)))

#These are not tested but are interesting
((1, (2,)), (2, (3,))) [missing but theres child pattern]
((1, (2,)), (2, (2,))) [missing but theres child pattern]
((1, (3,)), (2, (4,))) [missing but theres child pattern]
#Summaries of these patterns, when UNH does well so does McDonalds

((1, (4,)), (2, (4,)), (12, (4,)), (27, (4,))) [58]
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
from output_gen import load_dictionary, painter

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

#this gives 26% coverage of line 1 and 2`
ct = add(((1, (4,)), (2, (2,))),ct,d)
ct = add(((1, (3,)), (2, (3,))),ct,d)
ct = add(((1, (3,)), (2, (2,))),ct,d)


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
df2['dowjclose'] = list(pd.read_csv('./Stocks/MCD.csv').iloc[-1500:,:]['Close'])
df2['XOMclose'] = list(pd.read_csv('./Stocks/UNH.csv').iloc[-1500:,:]['Close'])
df2['patterns'] = d2[2]


config = { 
          #Red
          ((1, (4,)), (2, (2,))):'crimson', 
          #Orange
          #Cyan blue
          ((1, (3,)), (2, (3,))):'lawngreen',
          #Red
          ((1, (3,)), (2, (2,))):'deepskyblue',
 'None':'#f1f1f1'}

df2['colors'] = [config[x] for x in d2[2]]


# %%
def xyc(df2,date,data,color):
    xs=[]
    ys=[]
    x=[df2.iloc[0,:][date]]
    y=[df2.iloc[0,:][data]]
    c=[df2.iloc[0,:][color]]

    for row in df2.iterrows():
        row = row[1]
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
df2['labdowj']= df2['Close-MCD_-LB']
df2['labXOM']= df2['Close-UNH_-LB']
df2['patstr']= [ str(x) for x in df2['patterns']]
source2 = ColumnDataSource(df2)



output_file('McDonalds_UNH.html')


p = figure(x_axis_type='datetime' ,plot_width=1440, plot_height=600,
            title="United Health, McDonalds (3 patterns)")


p.circle(x='Date', y='dowjclose',name='dowj', alpha=0,
         source=source2,size=3)


p.multi_line(name='bill',
             xs=xom[0],
             ys=xom[1],
             color=xom[2],
             line_width=3)

p.multi_line(name='steve',
             xs=dowj[0], 
             ys=dowj[1],
             color=dowj[2],
             line_width=3)

p.circle(x='Date', y='XOMclose',name='xom', alpha=0,
         source=source2,size=3)


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

                                
                                ('Close United Health : ','@XOMclose'),
                                ('Close McDonalds : ','@dowjclose'),

                                ('Label United Health : ','@labXOM'),
                                ('Label McDonalds : ','@labdowj'),

                                ('Pattern : ','@patstr')



                                ]))

p.toolbar.logo = None


show(p)
