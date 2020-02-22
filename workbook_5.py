#%%


"""

We run UNH vs TRV to see if there is a difference between 
running them inside or outside of the DOWJ, there does seem to be a 
difference

"""

"""First we make the input data (see: example2 func within input_gen)
"""
from input_gen import example2
# We need to put this in a function to allow python multiprocessing
# to work.

def make_files():
    """
        Make all the files that we'll need for PYCCOLI
    """

    example2()

#Now that we have the files we can run PYCCOLI

from pyccoli import pyccoli
def run_pyccoli():
    pyccoli('UNH_TRV_5y_close')

#Uncomment to run pyccoli
'''
if __name__ == "__main__":
    make_files()
    run_pyccoli()
    pass
'''
# We can then move all the output files into a map (./output/UNHTRV)
# (Remaining of code is written as script thus comment it
# out if you want to run pyccoli as scripts and multi-
# processing do no play nice together)

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

ddict = load_dictionary('./output/UNHTRV/UNH_TRV_5y_close.dict')

# Filter out the singletons 
ct = { k:v for k,v in ddict.items() if (v[1]>1 )}
# Make dataframe (the hard way because pandas is being weird)
# AKA how i stopped worrying about pandas and just managed my
# dataframes by hand
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


'''
This gives

index	                Support Length Length_in_time		
((0, (3,)), (1, (3,)))	275	2	1
((0, (4,)), (1, (4,)))	176	2	1
((0, (3,)), (1, (4,)))	162	2	1
((0, (2,)), (1, (2,)))	107	2	1
((0, (3,)), (1, (2,)))	105	2	1
((0, (4,)), (1, (5,)))	43	2	1
((0, (5,)), (1, (4,)))	43	2	1
((0, (4,)), (1, (2,)))	39	2	1
((0, (1,)), (1, (2,)))	31	2	1
((0, (1,)), (1, (1,)))	26	2	1
((0, (5,)), (1, (5,)))	25	2	1
((0, (2, 3)), (1, (4,)))	21	3	2
((0, (2, 4)), (1, (4,)))	20	3	2
((0, (2, 4)), (1, (4, 4)))	7	4	2
((0, (5,)), (1, (2, 4)))	4	3	2

where 0 is UNH and 1 is TRV
The patterns we picked in 5 were
where 1 is UNH and 6 is TRV
((1, (1,)), (6, (1,))),
((1, (2,)), (6, (4,))),
((1, (5,)), (6, (4,))),
((1, (3,)), (6, (3, 3)))

This is very strange as ((0, (3,)), (1, (3,)))	
with its 275 support has been wiped from the table
That is, until looking into the dicitonary
it has probably been replaced by
((1, (3,)), (16, (3,)))
or ((1, (3,)), (15, (3,))) or one of the other 6
patterns that in total use UNH with movement 3
over 800 times, it is then no wonder that there 
is little space left to allow UNH to 
come together with traveller as more important
(i.e. longer) patterns eat up the space that is 
needed to distinguish UNH. This however shows
that there is more than one route to rome and
that not all routes are created equally, order
does most certainly matter

To make comparison fair we take only four patterns

thus
((0, (3,)), (1, (3,)))
((0, (4,)), (1, (4,)))
((0, (3,)), (1, (4,)))
((0, (2,)), (1, (2,)))

These patterns all have an immediate and simple trend
They move almost identically (with one slight exception)

We now visualize the results like we always do
'''
#%%
st, d = import_dat('./output/UNHTRV/UNH_TRV_5y_close.dat')

d_og = d

ct = st.copy()

#this gives 48% coverage of line 0 and 1
ct = add(((0, (3,)), (1, (3,))),ct,d)
ct = add(((0, (4,)), (1, (4,))),ct,d)
ct = add(((0, (3,)), (1, (4,))),ct,d)
ct = add(((0, (2,)), (1, (2,))),ct,d)


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

df2 = pd.read_excel('./output/UNHTRV/UNH_TRV_5y_close.xlsx')
df2['Date'] = pd.to_datetime(df2['Date'])
df2['ToolTipDates'] = df2.Date.map(lambda x: x.strftime("%d %b %y"))
df2['TRVclose'] = list(pd.read_csv('./Stocks/TRV.csv').iloc[-1500:,:]['Close'])
df2['UNHclose'] = list(pd.read_csv('./Stocks/UNH.csv').iloc[-1500:,:]['Close'])
df2['patterns'] = [str(x) for x in d2[0]]



#%%
config = { 
          #Red
          ((0, (3,)), (1, (3,))):'crimson', 
          #Orange
          ((0, (4,)), (1, (4,))):'purple', 
          #Cyan blue
          ((0, (3,)), (1, (4,))):'lawngreen',
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



trv = xyc(df2,'Date','TRVclose','colors')
unh = xyc(df2,'Date','UNHclose','colors')
df2['labTRV']= df2['Close-TRV_-LB']
df2['labUNH']= df2['Close-UNH_-LB']
df2['patstr']= [ str(x) for x in df2['patterns']]


source2 = ColumnDataSource(df2)



output_file('TRV_UNH.html')


p = figure(x_axis_type='datetime' ,plot_width=1440, plot_height=600,
            title="United Health and Travellers Closing Price")


p.circle(x='Date', y='UNHclose',name='unh', alpha=0,
         source=source2,size=3)


p.circle(x='Date', y='TRVclose',name='trv', alpha=0,
         source=source2,size=3)


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
                                ('Close Travellers : ','@TRVclose'),

                                ('Label United Health : ','@labUNH'),
                                ('Label Travellers : ','@labTRV'),

                                ('Pattern : ','@patstr')



                                ]))

p.toolbar.logo = None


show(p)

# %%
