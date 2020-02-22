"""
    With the expectation that similair stocks
    will behave alike, we analyze United Health
    Group and the travelers companyt, as they are both DowJones
    components and we expect them to behave the 
    same as they are both insurance companies
    
    United Health Group has the symbol UNH
    travelers comapny has the marking TRV
    
    Thus they occupy spot 1 and 6 in the dataset 
    respectively
"""

#Imports 
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
# First we load out dictionary to get the 
# results from PYCOLLI

ddict = load_dictionary('./output/dowj_5y_close.dict')

# Filter out the singletons 
ct = { k:v for k,v in ddict.items() if (v[1]>1 )}

#add the column values to the dictionary
for key in ct:
    rr =[]
    for i in key:
        rr.append(i[0])
    ct[key] = (ct[key],rr)

#Filter out all non-travelers and unh stock
patterns = []
for k,v in ct.items():
    if (1 in v[1]) and (6 in v[1]):
        patterns.append(k)

#We print our findings
''' omitted for cleanliness
for x in patterns:
    print(x)
    print(ddict[x])
'''

'''
Looking for patterns given that we only care about 1 
and 6, that is United Health and Travelrs respectively
we cut out the excess fat from patterns

((1, (1,)), (6, (1,)), (9, (1,)), (12, (1,)))
((1, (2,)), (6, (4,)), (26, (4, 3)))
((1, (5,)), (6, (4,)), (13, (3,)), (21, (3, 3)))
((1, (3,)), (2, (2,)), (6, (3, 3)), (14, (3,)), (19, (4,)))

giving

'''
patterns = [
((1, (1,)), (6, (1,))),
((1, (2,)), (6, (4,))),
((1, (5,)), (6, (4,))),
((1, (3,)), (6, (3, 3)))]

# We then count how often these appear in our database
# first we must import the database.
st, d = import_dat('./output/dowj_5y_close.dat')

'''
Then we check how often each one is found in a list of length 1500

for pattern in patterns:
    print(pattern)
    print(len(finder(pattern,d)))

This gives:


> for pattern in patterns:
>    print(pattern)
>    print(len(finder(pattern,d)))

((1, (1,)), (6, (1,)))
26
((1, (2,)), (6, (4,)))
65
((1, (5,)), (6, (4,)))
43
((1, (3,)), (6, (3, 3)))
107

which in a dataset of 1500 means 250 is maximally
covered (ergo ~15%) which is surprising compared to 
earlier results

We graph these results and then will compare them to 
another result (see workbook 6) where purely travelers versus UNH 
is mined and then plotted (thus disregarding the DOWJ)
'''

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

# %%
#We now do the usual for making a graph
d_og = d

ct = st.copy()

#this gives 16% coverage of line 1 
# and 23% of line 6`
ct = add(((1, (1,)), (6, (1,))),ct,d)
ct = add(((1, (2,)), (6, (4,))),ct,d)
ct = add(((1, (5,)), (6, (4,))),ct,d)
ct = add(((1, (3,)), (6, (3,3))),ct,d)



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

# ! you need to set this to the row your pattern pertains to
reference_column_database = 1
d2 = [[val_d[x] if x in val_d else 'None' for x in row]for row in d]
df2 = pd.read_excel('./output/dowj_5y_close.xlsx')
df2['Date'] = pd.to_datetime(df2['Date'])
df2['ToolTipDates'] = df2.Date.map(lambda x: x.strftime("%d %b %y"))
df2['UNHclose'] = list(pd.read_csv('./Stocks/UNH.csv').iloc[-1500:,:]['Close'])
df2['TRVclose'] = list(pd.read_csv('./Stocks/TRV.csv').iloc[-1500:,:]['Close'])
df2['patterns'] = d2[reference_column_database]
df2['patterns2'] = d2[6]


config = { 
          #Red
          ((1, (1,)), (6, (1,))):'crimson', 
          #Orange
          ((1, (2,)), (6, (4,))):'purple', 
          #Cyan blue
          ((1, (5,)), (6, (4,))):'lawngreen',
          #Red
          ((1, (3,)), (6, (3,3))):'deepskyblue',
 'None':'#f1f1f1'}

df2['colors'] = [config[x] for x in d2[reference_column_database]]
df2['colors2'] = [config[x] for x in d2[6]]



unh = xyc(df2,'Date','UNHclose','colors')
trv = xyc(df2,'Date','TRVclose','colors2')
df2['labTRV']= df2['Close-TRV_-LB']
df2['labUNH']= df2['Close-UNH_-LB']
df2['patstr']= [ str(x) for x in df2['patterns']]
source2 = ColumnDataSource(df2)



output_file('UnitedHealth_Travellers.html')




p = figure(x_axis_type='datetime' ,plot_width=1440, plot_height=600,
            title="United Health and Travellers Closing Price")


p.circle(x='Date', y='TRVclose',name='trv', alpha=0,
         source=source2,size=3)


p.circle(x='Date', y='UNHclose',name='unh', alpha=0,
         source=source2,size=3,color='colors')


p.multi_line(name='bill',
             xs=unh[0],
             ys=unh[1],
             color=unh[2],
             line_width=3)

p.multi_line(name='steve',
             xs=trv[0], 
             ys=trv[1],
             color=trv[2],
             line_width=3)


p.add_tools(HoverTool(names=['unh'],
                      mode = "vline",
                      line_policy='nearest',
                      point_policy='snap_to_data',
                                tooltips=[

                                ]))

p.add_tools(HoverTool(names=['trv'],
                      mode = "vline",
                      line_policy='nearest',
                      point_policy='snap_to_data',
                                tooltips=[
                                ('Date : ','@ToolTipDates'),

                                
                                ('Close United Health : ','@UNHclose'),
                                ('Close Travelers : ','@TRVclose'),

                                ('Label United Health : ','@labUNH'),
                                ('Label Travelers : ','@labTRV'),

                                ('Pattern : ','@patstr')



                                ]))


p.toolbar.logo = None


show(p)
