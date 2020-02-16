
"""

We run UNH vs mcdonalds to see if there is a difference between 
running them inside or outside of the DOWJ, previous work
between UNH and mcd showed that this was  the case
how will the results between UNH MCD fare up

"""

"""First we make the input data (see: example2 func within input_gen)
"""
from input_gen import example3
# We need to put this in a function to allow python multiprocessing
# to work.

def make_files():
    """
        Make all the files that we'll need for PYCCOLI
    """

    example3()

#Now that we have the files we can run PYCCOLI

from pyccoli import pyccoli
def run_pyccoli():
    pyccoli('UNH_MCD_5y_close')

#Uncomment to run pyccoli
'''
if __name__ == "__main__":
    make_files()
    run_pyccoli()
'''
'''
The answer to the question is no as the top patterns found are
different, there is overla but the priorities of both scopes seem
different that is the moust found patther within UNH and MCD
3 and 3 is not found within the dowjones, this is presumably 
because again just like in the case of workbook 4 versus 5 it
is used by other patterns when taking the dowjones as a whole
it would thus be intereseting in future research to let the patterns
overlap.


'''


#%%
from output_gen import load_dictionary, painter, compare_dictionaries
# We check what patterns overlap
ddict1_tmp = list(load_dictionary('./output/UNHMCD/UNH_MCD_5y_close.dict'))
ddict2 = load_dictionary('./output/dowj_5y_close.dict')
#we need to make the columns equal
ddict1 =[]
for x in ddict1_tmp:
    qq= []
    for row,pattern in x:
        qq.append(tuple([row+1,pattern]))
    ddict1.append(tuple(qq))


    
patterns_in_common = compare_dictionaries(ddict1,ddict2)

"""Output

[((1, (4,)),),
 ((1, (2,)),),
 ((2, (3,)),),
 ((1, (4,)), (2, (4,))),
 ((2, (1,)),),
 ((1, (5,)),),
 ((1, (3,)),),
 ((2, (2,)),),
 ((2, (5,)),),
 ((2, (4,)),),
 ((1, (1,)),)]
"""

'''
The fascinating part is that they only have one pattern in common 
United Health goes to 4 and then McDonalds also going to for 

For completeness sake we construct a graph with the four top patterns

'''


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

ddict = load_dictionary('./output/UNHMCD/UNH_MCD_5y_close.dict')

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


#%%
st, d = import_dat('./output/UNHMCD/UNH_MCD_5y_close.dat')

d_og = d

ct = st.copy()

#this gives 30% coverage of line 0 and 1
ct = add(list(ct_df.index)[0],ct,d)
ct = add(list(ct_df.index)[1],ct,d)
ct = add(list(ct_df.index)[2],ct,d)


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

df2 = pd.read_excel('./output/UNHMCD/UNH_MCD_5y_close.xlsx')
df2['Date'] = pd.to_datetime(df2['Date'])
df2['ToolTipDates'] = df2.Date.map(lambda x: x.strftime("%d %b %y"))
df2['MCDclose'] = list(pd.read_csv('./Stocks/MCD.csv').iloc[-1500:,:]['Close'])
df2['UNHclose'] = list(pd.read_csv('./Stocks/UNH.csv').iloc[-1500:,:]['Close'])
df2['patterns'] = [str(x) for x in d2[0]]



#%%
config = { 
          #Red
          list(ct_df.index)[0]:'lawngreen', 
          #Orange
          #Cyan blue
          list(ct_df.index)[1]:'deepskyblue',
          #Red
          list(ct_df.index)[2]:'crimson',
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



output_file('MCD_UNH.html')


p = figure(x_axis_type='datetime' ,plot_width=1440, plot_height=600,
            title="United Health, McDonalds (3 patterns)")


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
