#%%
from input_gen import example4
# We need to put this in a function to allow python multiprocessing
# to work.

def make_files():
    """
        Make all the files that we'll need for PYCCOLI
    """

    example4()

#Now that we have the files we can run PYCCOLI

from pyccoli import pyccoli
def run_pyccoli():
    pyccoli('PEP_KO_5y_close')

#Uncomment to run pyccoli
'''
if __name__ == "__main__":
    make_files()
    run_pyccoli()
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
ct = load_dictionary('./output/workbook9/PEP_KO_5y_close.dict')
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


st, d = import_dat('./output/workbook9/PEP_KO_5y_close.dat')

d_og = d

ct = st.copy()

#this gives  33% coverage of line 0 and 1
ct = add(list(ct_df.index)[0],ct,d)
ct = add(list(ct_df.index)[2],ct,d)
ct = add(list(ct_df.index)[4],ct,d)
ct = add(list(ct_df.index)[5],ct,d)


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


df2 = pd.read_excel('./output/workbook9/PEP_KO_5y_close.xlsx')
df2['Date'] = pd.to_datetime(df2['Date'])
df2['ToolTipDates'] = df2.Date.map(lambda x: x.strftime("%d %b %y"))
df2['PEPclose'] = list(pd.read_csv('./Stocks/PEP.csv').iloc[-1500:,:]['Close'])
df2['KOclose'] = list(pd.read_csv('./Stocks/KO.csv').iloc[-1500:,:]['Close'])
df2['patterns'] = [str(x) for x in d2[0]]


config = { 
          #Red
          list(ct_df.index)[0]:'crimson', 
          #Orange
          list(ct_df.index)[2]:'gold', 
          #Cyan blue
          list(ct_df.index)[4]:'lawngreen',
          #Red
          list(ct_df.index)[5]:'deepskyblue',
 'None':'#f1f1f1'}
df2['colors'] = [config[x] for x in d2[1]]



ko = xyc(df2,'Date','KOclose','colors')
pep = xyc(df2,'Date','PEPclose','colors')
df2['labPEP']= df2['Close-PEP_-LB']
df2['labKO']= df2['Close-KO_-LB']
df2['patstr']= [ str(x) for x in df2['patterns']]


source2 = ColumnDataSource(df2)



output_file('PEP_KO.html')


p = figure(x_axis_type='datetime' ,plot_width=1440, plot_height=600,
            title="Coca-Cola, PepsiCo (3 patterns)")

p.circle(x='Date', y='PEPclose',name='pep', alpha=0,
         source=source2,size=3)


p.circle(x='Date', y='KOclose',name='ko', alpha=0,
         source=source2,size=3)


p.multi_line(name='bill',
             xs=ko[0],
             ys=ko[1],
             color=ko[2],
             line_width=3)

p.multi_line(name='steve',
             xs=pep[0], 
             ys=pep[1],
             color=pep[2],
             line_width=3)


p.add_tools(HoverTool(names=['pep'],
                      mode = "vline",
                      line_policy='nearest',
                      point_policy='snap_to_data',
                                tooltips=[

                                ]))

p.add_tools(HoverTool(names=['ko'],
                      mode = "vline",
                      line_policy='nearest',
                      point_policy='snap_to_data',
                                tooltips=[
                                ('Date : ','@ToolTipDates'),

                                
                                ('Close Pepsi : ','@PEPclose'),
                                ('Close Coca-Cola : ','@KOclose'),

                                ('Label Pepsi : ','@labPEP'),
                                ('Label Coca-Cola : ','@labKO'),

                                ('Pattern : ','@patstr')



                                ]))

p.toolbar.logo = None

show(p)



# %%
