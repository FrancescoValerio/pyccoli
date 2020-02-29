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
from pattern_finder import finder

#%%
st, d = import_dat('./output/UNHMCD/UNH_MCD_5y_close.dat')

d_og = d

ct = st.copy()

#index patterns
ct = add(((0, (4,)), (1, (4,))),ct,d)
ct = add(((0, (4,)), (1, (3,))),ct,d)
ct = add(((0, (2,)), (1, (4,))),ct,d)

ct = add(((0, (5, 4)), (1, (4,))),ct,d)
ct = add(((0, (4,)), (1, (5, 3))),ct,d)
#stock pattens
ct = add(((0, (3,)), (1, (3,))),ct,d)
ct = add(((0, (3,)), (1, (4,))),ct,d)

ct = add(((0, (3,)), (1, (2,))),ct,d)
ct = add(((0, (2,)), (1, (2,))),ct,d)

patterns = {}
for key, value in ct.items():
    if value[1]>1:
        patterns[key]=value

ordered_p = cov_order(patterns)

#%%

val_d ={}
sign = -100
for x in ordered_p:
    # 'Paint' the dataset with 0's where covered and return p amount
    d = painter(x,d,sign)
    val_d[sign] = x

    sign *= 2

#%%
d2 = [[val_d[x] if x in val_d else 'None' for x in row]for row in d]

df2 = pd.read_excel('./output/UNHMCD/UNH_MCD_5y_close.xlsx')
df2['Date'] = pd.to_datetime(df2['Date'])
df2['ToolTipDates'] = df2.Date.map(lambda x: x.strftime("%d %b %y"))
df2['MCDclose'] = list(pd.read_csv('./Stocks/MCD.csv').iloc[-1500:,:]['Close'])
df2['UNHclose'] = list(pd.read_csv('./Stocks/UNH.csv').iloc[-1500:,:]['Close'])
df2['patterns'] = [str(x) for x in d2[0]]



#%%
config = { 
          #Red
          ((0, (4,)), (1, (3,))):'crimson', 
          #Orange
          ((0, (4,)), (1, (4,))):'crimson', 
          #Cyan blue
          ((0, (5, 4)), (1, (4,))):'crimson',
          #Red
          ((0, (2,)), (1, (4,))):'crimson',
          ((0, (4,)), (1, (5, 3))):'crimson',
          
        #Red
          ((0, (3,)), (1, (3,))):'deepskyblue', 
          #Orange
          ((0, (3,)), (1, (4,))):'deepskyblue', 
          #Cyan blue
          ((0, (3,)), (1, (2,))):'deepskyblue',
          #Red
          ((0, (2,)), (1, (2,))):'deepskyblue',
                   
 'None':'#f1f1f1'}
# %%


df2['colors'] = [config[x] for x in d2[1]]



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



mcd = xyc(df2,'Date','MCDclose','colors')
unh = xyc(df2,'Date','UNHclose','colors')
df2['labMCD']= df2['Close-MCD_-LB']
df2['labUNH']= df2['Close-UNH_-LB']
df2['patstr']= [ str(x) for x in df2['patterns']]


source2 = ColumnDataSource(df2)



output_file('MCD_UNH(nowmixed).html')


p = figure(x_axis_type='datetime' ,plot_width=1440, plot_height=600,
            title="United Health and McDonalds price")


p.circle(x='Date', y='UNHclose',name='unh', alpha=0,
         source=source2,size=3)


p.circle(x='Date', y='MCDclose',name='mcd', alpha=0,
         source=source2,size=3)


p.multi_line(name='bill',
             xs=unh[0],
             ys=unh[1],
             color=unh[2],
             line_width=3)

p.multi_line(name='steve',
             xs=mcd[0], 
             ys=mcd[1],
             color=mcd[2],
             line_width=3)


p.add_tools(HoverTool(names=['unh'],
                      mode = "vline",
                      line_policy='nearest',
                      point_policy='snap_to_data',
                                tooltips=[

                                ]))

p.add_tools(HoverTool(names=['mcd'],
                      mode = "vline",
                      line_policy='nearest',
                      point_policy='snap_to_data',
                                tooltips=[
                                ('Date : ','@ToolTipDates'),

                                
                                ('Close United Health : ','@UNHclose'),
                                ('Close McDonalds : ','@MCDclose'),

                                ('Label United Health : ','@labUNH'),
                                ('Label McDonalds : ','@labMCD'),

                                ('Pattern : ','@patstr')



                                ]))

p.toolbar.logo = None


show(p)

# %%
