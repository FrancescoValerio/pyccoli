
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

d = load_dictionary('./output/AAPL_5y_comp.dict')
ct = { k:v for k,v in d.items() if v[1]>1}
ct_df = pd.DataFrame.from_dict(ct,
        orient='index',columns=['Support',
        'Length','Time'])


ct_df.sort_values('Support')[::-1][:10]

st, d = import_dat('./output/AAPL_5y_comp.dat')
d_og = d

ct = st.copy()
lijst = list(ct_df.sort_values('Support')[::-1][:20].index)
#this gives 66% coverage of line 1 and 3`
ct = add(lijst[0],ct,d)
ct = add(lijst[1],ct,d)
ct = add(lijst[5],ct,d)
ct = add(lijst[9],ct,d)

#ththese two cover 33% of line 4

# deze dekken 150 meer (dus 10% meer)
#ct = add(lijst[3],ct,d)
#ct = add(lijst[6],ct,d)

#deze zijn natuurlijk veel interessanter en dekken 30 ipv 40 procent
ct = add(lijst[13],ct,d)
ct = add(lijst[17],ct,d)




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

df2 = pd.read_csv('./Stocks/AAPL.csv').iloc[-1500:,:]
for i,x in enumerate(['Open','High','Low','Close']):
    df2[f'{x}Dif'] = df2[x].pct_change()
df2 = df2.iloc[1:,:]

#%%
for i,x in enumerate(['OpenK','HighK','LowK','CloseK','VolumeK']):
    df2[f'{x}']=d_og[i]
    df2[f'{x}Named']=d2[i]
df2['Date'] = pd.to_datetime(df2['Date'])

df2['ToolTipDates'] = df2.Date.map(lambda x: x.strftime("%d %b %y"))
config2 = { 
          #Red
          ((1, (2,)), (2, (2,))):'red', 
          #Orange
          ((1, (2,)), (2, (3,))):'red', 
          #Cyan blue
          ((1, (2,)), (2, (4,))):'red',
          #Red
           ((1, (3,)), (2, (4,))):'red',
 'None':'Grey'}

config = { 
          #Red
          ((1, (2,)), (2, (2,))):'crimson', 
          #Orange
          ((1, (2,)), (2, (3,))):'gold', 
          #Cyan blue
          ((1, (2,)), (2, (4,))):'lawngreen',
          #Red
           ((1, (3,)), (2, (4,))):'deepskyblue',
 'None':'gainsboro'}
config=config2
df2['highColor'] = [config[x] for x in df2['HighKNamed'] ]
df2['highAlpha'] = [0 if x=='Grey' else 1 for x in df2['highColor'] ]
df2['volCode'] = d2[4]


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



high = xyc(df2,'Date','High','highColor')
low = xyc(df2,'Date','Low','highColor')

source2 = ColumnDataSource(df2)
output_file('test.html')


dd2={
    'None':'gainsboro',
    ((4, (1, 2, 1)),):'Blue',
    ((4, (1, 2, 2)),):'Purple'
}
df2['volColor']=[dd2[x] for x in df2['volCode']]

vol = xyc(df2,'Date','Volume','volColor')
           


#%%
#! FIRST RUN W2.PY IN JUPYTHER THEN THIS CODE TO GET GRAPHS

df2 = pd.read_csv('./Stocks/AAPL.csv').iloc[-1500:,:]
for i,x in enumerate(['Open','High','Low','Close']):
    df2[f'{x}Dif'] = df2[x].pct_change()
df2 = df2.iloc[1:,:]

for i,x in enumerate(['OpenK','HighK','LowK','CloseK','VolumeK']):
    df2[f'{x}']=d_og[i]
    df2[f'{x}Named']=d2[i]
df2['Date'] = pd.to_datetime(df2['Date'])

df2['ToolTipDates'] = df2.Date.map(lambda x: x.strftime("%d %b %y"))

config = { 
          #Red
          ((1, (2,)), (2, (2,))):'crimson', 
          #Orange
          ((1, (2,)), (2, (3,))):'gold', 
          #Cyan blue
          ((1, (2,)), (2, (4,))):'lawngreen',
          #Red
           ((1, (3,)), (2, (4,))):'deepskyblue',
 'None':'gainsboro'}
df2['highColor'] = [config[x] for x in df2['HighKNamed'] ]
df2['highAlpha'] = [0 if x=='Grey' else 1 for x in df2['highColor'] ]
df2['volCode'] = d2[4]

df2['VolumeKNamedstr'] = [str(x) for x in df2['VolumeKNamed']]
df2['LowKNamedstr']= [str(x) for x in df2['LowKNamed']]

source2 = ColumnDataSource(df2)

output_file('Apple.html')

p = figure(x_axis_type='datetime' ,plot_width=1440, plot_height=600,
            title="Apple Stock (6 patterns)",y_range=[50,250],y_axis_type='linear')

p.circle(x='Date', y='Low',name='low', alpha=0,
         source=source2,size=3)

p.circle(x='Date', y='High',name='high', alpha=0,
         source=source2,size=3)



p.add_tools(HoverTool(names=['low'],
                      mode = "vline",
                      line_policy='nearest',
                      point_policy='snap_to_data',
                                tooltips=[

                                ]))





high = xyc(df2,'Date','High','highColor')
low = xyc(df2,'Date','Low','highColor')
p.multi_line(name='steve',
             xs=high[0], 
             ys=high[1],
             color=high[2],
             line_width=3)

p.multi_line(name='bill',
             xs=low[0],
             ys=low[1],
             color=low[2],
             line_width=3)
df2['volColor']=[dd2[x] for x in df2['volCode']]

q = figure(x_range=p.x_range ,plot_width=1440, plot_height=200,
            title="Stock Volume",y_axis_type='linear')
vol = xyc(df2,'Date','Volume','volColor')
         
q.multi_line(name='vol',
             xs=vol[0],
             ys=vol[1],
             color=vol[2],
             line_width=3)

q.circle(x='Date', y='Volume',name='volli', alpha=0,
         source=source2,size=3)

q.add_tools(HoverTool(names=['volli'],
                      mode = "vline",
                      line_policy='nearest',
                      point_policy='snap_to_data',
                                tooltips=[
                                ('Date : ','@ToolTipDates'),

                                ('Volume : ','@Volume'),
                                ('Volume Class : ','@VolumeK'),
                                ('Pattern : ','@VolumeKNamedstr')



                                ]))


p.add_tools(HoverTool(names=['high'],
                      mode = "vline",
                      line_policy='nearest',
                      point_policy='snap_to_data',
                                tooltips=[
                                ('Date : ','@ToolTipDates'),
                                ('High : ','@High'),
                                ('Low : ','@Low'),
                                ('High class : ','@HighK'),
                                ('Low class : ','@LowK'),
                                
                                ('Pattern : ','@LowKNamedstr')



                                ]))


q.toolbar.logo = None
p.toolbar.logo = None

show(column(p,q))
# %%
