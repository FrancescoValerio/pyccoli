#%%

'''
#? Code used to generate this output was:



dow =[]

for x in index_list('dowj'):
    
    if x in ('V','GS','DOW'):
        continue
    
    dow.append(import_csv_to_df(f'./Stocks/{x}.csv'))
dow.append(import_csv_to_df(f'./Stocks/1ndex_DOW.csv'))
dow = join_dataframes(*dow)

#dow = import_csv_to_df('./AAPL.csv').iloc[-1500:]
dow = filter_columns(dow,'Close')
dow = remove_NaN_rows(dow)
a = row_diff(dow)
a = a.iloc[-1500:,:]
a = kmean_columns(a,5)
#a = filter_columns(a,'LB')

export_to_pyccoli(filter_columns(a,'LB'),'dowj_5y_close')
a.to_excel('dowj_5y_close.xlsx')


'''

'''
#! Analysis of 1500 days of Dow Jones data

Data has been drawn from the 10th of September 2013
until august 23 2019.
'''
#%%
import numpy as np
import pandas as pd
from output_gen import load_dictionary

d = load_dictionary('./output/AAPL_5y_comp.dict')
ct = { k:v for k,v in d.items() if v[1]>1}
ct_df = pd.DataFrame.from_dict(ct,
        orient='index',columns=['Support',
        'Length','Time'])


ct_df.sort_values('Support')[::-1][:10]

'''

Within the top 5 stocks interestingly enough the
firs two stocks are Mcdonalds and United 
Health Group. They only appear together in the top 10
Making up spot number 1, 2,6, 10.

Taking those 4 together, you can link 2/3 of every 
trading day based on the movement of Mcdonalds 
versus United Health Group. Why?

Google provides no free lunch, so time to 
investigate. For our missing third variable.

First option. They are part of same index so they
move together.

No, they move different directions within spot
1, 2 and 6 only within 10 are they both going 
both the same direction and even in that case
it is down and not up. You could make an argument
that some institutional investor is going so
long on the DOWJ index that it pulls them both
up, but that they short it the DOW so hard that
it pulls it down is very very unlikely.
The risk would simply be far too large.

Second option. Mcdonalds buys their insurance
ar UNH. Nope, McDonalds gets their insurance
from Blue Cross Blue Shield Association members
who are competitors from UNH.

Perhaps both measures relate to american health 
numbers?

We plot the data we have for more insight
'''
#%%
from import_data import import_dat
from add_rem import add
from cover import cov_order
from output_gen import painter

st, d = import_dat('./output/dowj_5y_close.dat')
d_og = d

ct = st.copy()
lijst = list(ct_df.sort_values('Support')[::-1][:10].index)
ct = add(lijst[0],ct,d)
ct = add(lijst[1],ct,d)
ct = add(lijst[5],ct,d)
ct = add(lijst[9],ct,d)

patterns = {}
for key, value in ct.items():
    if value[1]>1:
        patterns[key]=value

ordered_p = cov_order(patterns)

sign = -100
for x in ordered_p:
    # 'Paint' the dataset with 0's where covered and return p amount
    d = painter(x,d,sign)
    sign *= 2
    
d= d[1:3]
'''
The first and second row of the dataset have now been 
marked and extracted, the patterns explain 1024 of the 
1499 points, thus more than two thirds.

Just the first pattern alone explains almost 1/3 of the data
so what is this pattern and when does it occur

To get an idea as to what it does to our time series we append
it to the excel file used
'''
#%%
#We make sure that the data is correct

from input_gen import import_csv_to_df, join_dataframes
from input_gen import filter_columns, remove_NaN_rows
from input_gen import row_diff


imported_excel = pd.read_excel('./output/dowj_5y_close.xlsx',
                               index_col=0).iloc[1:,1:3]

import_stocklist = []
for x in ('UNH','MCD'):
    import_stocklist.append(import_csv_to_df(f'./Stocks/{x}.csv'))
stocklist = join_dataframes(*import_stocklist)
stocklist = remove_NaN_rows(stocklist)
stocklist = stocklist.iloc[-1500:,:]

stocklist = filter_columns(stocklist,'Close')
stocklist_backup = stocklist.copy()
stocklist =row_diff(stocklist)
stocklist['UNH-kmean'] = d[0][1:]
stocklist['MCD-kmean'] = d[1][1:]
stocklist['og_UNH-kmean'] = d_og[1][1:]
stocklist['og_MCD-kmean'] = d_og[2][1:]
stocklist['og_Close-UNH'] = stocklist_backup['Close-UNH']
stocklist['og_Close-MCD'] = stocklist_backup['Close-MCD']


#%%
    

colordict ={
    #blue
    -800: '#00FFFF',
    #these need to be brighter
    #orange
    -400: '#ffc87c',
    #Green
    -200: '#2ca02c',
    #red
    -100: '#ef2728',
}


stocklist['Color'] = [colordict[x] if x in colordict 
                       else '#d9d9d9' for x in stocklist['MCD-kmean']]


#Now we build the first plot
'''
import matplotlib.pyplot as plt


def gen_repeating(s):
    """Generator: groups repeated elements in an iterable
    E.g.
        'abbccc' -> [('a', 0, 0), ('b', 1, 2), ('c', 3, 5)]
                    [(<string>,start,end),...,(<string>,start,end)]
    """
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        yield (s[i], i, j-1)
        i = j
        

colordict ={
    -800: '#7FFF00',
    -400: '#FF0000',
    -200: '#15F4EE',
    -100: '#e7FF00',
}
stocklist['Color'] = [colordict[x] if x in colordict 
                       else '#000000' for x in stocklist['MCD-kmean']]

fig, ax = plt.subplots(figsize=(120, 10),dpi=120)

for color, start, end in gen_repeating(stocklist['Color']):
    if start > 0: # make sure lines connect
        start -= 1
    idx = stocklist.index[start:end+1]
    stocklist.loc[idx, 'og_Close-UNH'].plot(
        ax=ax, color=color, label='United Health')
    stocklist.loc[idx, 'og_Close-MCD'].plot(
        ax=ax, color=color, label='McDonalds')

#plt.show()
plt.savefig('books_read3.png')
'''
'''

Now we make a nicer plot
'''

'''

Bokeh 1

def make_array(df,column_name):
    x = []
    y = []
    color = []
    
    first = True
    
    for index,row in df.iterrows():
        if first:
            x_mem = []
            y_mem = []
            first = False
            c = row['Color']
            color.append(c)
            x_mem.append(index)
            y_mem.append(row[column_name])
        else:
            if row['Color'] == c:
                x_mem.append(index)
                y_mem.append(row[column_name])
            else:
                x_mem.append(index)
                y_mem.append(row[column_name])
                x.append(x_mem)
                y.append(y_mem)
                x_mem = []
                y_mem = []
                c = row['Color']
                color.append(c)
                x_mem.append(index)
                y_mem.append(row[column_name])
    x.append(x_mem)
    y.append(y_mem)
    return x,y, color    

                    
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.sampledata.autompg import autompg



source = ColumnDataSource(autompg)
   
output_file('dab.html')

x,y_unh, color = make_array(stocklist,'og_Close-UNH')
x,y_mcd, color = make_array(stocklist,'og_Close-MCD')

p = figure(width=1200, height=800, x_axis_type="datetime") 
p.multi_line(xs=x+x,
                ys=y_mcd+y_unh,
                line_color=color+color,
                line_width=3)


p.add_tools(HoverTool(tooltips=[('Value:','$y'),
                                ('Date:','$x')]))
show(p)    
'''

'''
Bokeh 2
'''
'''
df = stocklist.reset_index()
df['Date2'] = pd.to_datetime(df['Date'])
df['ClassMCD'] = df['og_MCD-kmean']
df['ClassUNH'] = df['og_UNH-kmean']

df['ToolTipDates'] = df.Date.map(lambda x: x.strftime("%y %b %d")) # Saves work with the tooltip later

from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource, CustomJSHover
from bokeh.palettes import Spectral6
from bokeh.transform import linear_cmap


source = ColumnDataSource(df)
output_file('dab.html')

p = figure(x_axis_type='datetime' ,plot_width=1440, plot_height=800, title="Patterns between Mcdonalds and United Health")

p.line(x='Date', y='og_Close-MCD', source=source,color='grey',line_width=3,line_alpha=0.5)
p.circle(x='Date', y='og_Close-MCD',name='circle', source=source,color='Color',size=5)

p.line(x='Date', y='og_Close-UNH', source=source,color='grey',line_width=3,line_alpha=0.5)
p.circle(x='Date', y='og_Close-UNH',name='circle2', source=source,color='Color',size=5)


p.add_tools(HoverTool(names=['circle'],tooltips=[('Close :','$y'),
                                ('Date :','@ToolTipDates'),
                                ('Class :','@ClassMCD'),                                
                                
                                ]))

p.add_tools(HoverTool(names=['circle2'],tooltips=[('Close :','$y'),
                                ('Date :','@ToolTipDates'),
                                ('Class :','@ClassUNH')
                                
                                ]))


show(p)    
'''

'''
Bokeh3
'''
'''

from bokeh.models import ColumnDataSource, Plot, LinearAxis, Grid
from bokeh.models.glyphs import MultiLine
from bokeh.io import curdoc, show

df = stocklist.reset_index()
df['Date2'] = pd.to_datetime(df['Date'])
df['ClassMCD'] = df['og_MCD-kmean']
df['ClassUNH'] = df['og_UNH-kmean']

df['ToolTipDates'] = df.Date.map(lambda x: x.strftime("%y %b %d")) # Saves work with the tooltip later


source = ColumnDataSource(df)
output_file('d.html')
p = figure(x_axis_type='datetime' ,plot_width=1440, plot_height=800,
            title="Patterns between Mcdonalds and United Health")

p.multi_line(xs=[[1,2,3],[1,2,3],[3,4,5,6]],
              ys=[[1,2,3],[4,5,6],[3,4,5,6]],
              line_color=['red','blue','yellow'], line_width=2)
show(p)

'''


def make_array(df,kleur,column,klas,verschil):
    first=True
    x=[]
    y=[]
    color = []
    clss = []
    diff = []
    for i in range(len(df.index)):
        
        row = df.iloc[i,:]

        
        if first:
            first = False
            xMem = []
            yMem = []
            clsMem =[]
            difMem =[]
            xMem.append(row['Date'])
            yMem.append(row[column])
            clsMem.append(row[klas])
            difMem.append(row[verschil])
            color.append(row[kleur])
        
        if not row[kleur] == color[-1]:
            x.append(xMem)
            y.append(yMem)
            clss.append(clsMem)
            diff.append(difMem)
            
            xMem=[df.iloc[i-1,:]['Date']]
            yMem=[df.iloc[i-1,:][column]]
            clsMem=[df.iloc[i-1,:][klas]]
            difMem=[df.iloc[i-1,:][verschil]]
                   
            
            xMem.append(row['Date'])
            yMem.append(row[column])
            clsMem.append(row[klas])
            difMem.append(row[verschil])
            color.append(row[kleur])
        
        else:
            xMem.append(row['Date'])
            yMem.append(row[column])
            clsMem.append(row[klas])
            difMem.append(row[verschil])
            
    x.append(xMem)
    y.append(yMem)
    clss.append(clsMem)
    diff.append(difMem)
    return x,y,color,clss,diff
        

from bokeh.models import HoverTool

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, LinearAxis, Grid
from bokeh.models.glyphs import MultiLine
from bokeh.io import curdoc, show
from bokeh.plotting import figure, show, output_file

df = stocklist.reset_index()
df['Date2'] = pd.to_datetime(df['Date'])
df['ClassMCD'] = df['og_MCD-kmean']
df['ClassUNH'] = df['og_UNH-kmean']
df['pUNH'] = [x*100 for x in df['Close-UNH']]
df['pMCD'] = [x*100 for x in df['Close-MCD']]

HoverTool(mode='vline')

df['ToolTipDates'] = df.Date.map(lambda x: x.strftime("%d %b %y")) # Saves work with the tooltip later

mcd = make_array(df,'og_Close-MCD','og_MCD-kmean','Close-MCD')
unh = make_array(df,'og_Close-UNH','og_UNH-kmean','Close-UNH')
source2 = ColumnDataSource(df)

source = ColumnDataSource(dict(xsMcd=mcd[0],ysMcd=mcd[1],
                               xsUnh=unh[0],ysUnh=unh[1],
                               cMcd=mcd[2],cUnh=unh[2],
                               classM=mcd[3],classU=unh[3],
                               diffM=mcd[4],diffU=unh[4]))
output_file('mcdonalds_unitedhealth.html')
p = figure(x_axis_type='datetime' ,plot_width=1440, plot_height=800,
            title="Patterns between Mcdonalds and United Health")

p.multi_line(xs='xsMcd',
              ys='ysMcd',
              line_join='round',
              legend='cMcd',
              line_color='cMcd', line_width=4,name='mcd',source=source)

p.multi_line(xs='xsUnh',
              ys='ysUnh',
              line_join='round',
              line_color='cUnh', line_width=4,name='unh',source=source)

p.circle(x='Date', y='og_Close-MCD',name='mcdonalds', alpha=0,
          source=source2,color='Color',size=4)
p.circle(x='Date', y='og_Close-UNH',name='circle2', alpha=0,
         source=source2,color='Color',size=4)


p.add_tools(HoverTool(names=['mcdonalds'],
                               
                                point_policy = "snap_to_data",
                                mode = 'vline',
                                tooltips=[
                                ('Stock : ','McDonalds'),
                                ('Close :','$y'),
                                ('Date :','@ToolTipDates'),
                                ('Class :','@ClassUNH'),
                                ('Difference :','@pMCD %'),                                
                                
                                ]))

p.add_tools(HoverTool(names=['circle2'],
                      point_policy = "snap_to_data",
                      mode='vline',
                      tooltips=[
                                
                                ('Stock : ','UnitedHealth'),
                                ('Close :','$y'),
                                ('Date :','@ToolTipDates'),
                                ('Class :','@ClassUNH'),
                                ('Difference :','@pUNH %')
                                
                                
                                ]))
#p.add_tools(HoverTool(names=['mcd'],tooltips=[('Value:','$y')]))



#p.add_tools(HoverTool(names=['unh'],tooltips=[('Value:','$y')]))


show(p)




# %%
