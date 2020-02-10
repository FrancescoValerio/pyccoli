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

import_stock_list = []
for x in ('UNH','MCD'):
    import_stock_list.append(import_csv_to_df(f'./Stocks/{x}.csv'))
stock_list = join_dataframes(*import_stock_list)
stock_list = remove_NaN_rows(stock_list)
stock_list = stock_list.iloc[-1500:,:]

stock_list = filter_columns(stock_list,'Close')
stock_list_backup = stock_list.copy()
stock_list =row_diff(stock_list)
stock_list['UNH-kmean'] = d[0][1:]
stock_list['MCD-kmean'] = d[1][1:]
stock_list['og_UNH-kmean'] = d_og[1][1:]
stock_list['og_MCD-kmean'] = d_og[2][1:]
stock_list['og_Close-UNH'] = stock_list_backup['Close-UNH']
stock_list['og_Close-MCD'] = stock_list_backup['Close-MCD']





# %%

#Now we build the first plot
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
stock_list['Color'] = [colordict[x] if x in colordict 
                       else '#000000' for x in stock_list['MCD-kmean']]

fig, ax = plt.subplots(figsize=(120, 10),dpi=120)

for color, start, end in gen_repeating(stock_list['Color']):
    if start > 0: # make sure lines connect
        start -= 1
    idx = stock_list.index[start:end+1]
    stock_list.loc[idx, 'og_Close-UNH'].plot(
        ax=ax, color=color, label='United Health')
    stock_list.loc[idx, 'og_Close-MCD'].plot(
        ax=ax, color=color, label='McDonalds')

#plt.show()
plt.savefig('books_read3.png')
'''

Now we make a nicer plot
'''

#%%

from bokeh.plotting import figure, output_file, show

output_file("patch.html")

p = figure(plot_width=1200, plot_height=400)


p.multi_line([[1,2,3],[4,5,6]],
             [[1,2,3],[4,5,6]],
             color=["firebrick",'blue'], alpha=[0.8], line_width=4)

show(p)

# %%

colordict ={
    -800: 1,
    -400: 2,
    -200: 3,
    -100: 4,
}
stock_list['Color2'] = [colordict2[x] if x in colordict 
                       else 0 for x in stock_list['MCD-kmean']]

import plotly.express as px
d = {'col1': list(range(5)), 'col2': list(range(5)),'type':[0,1,1,2,2]}
df = pd.DataFrame(data=d)
fig = px.line(df, x='col1', y='col2',color='type')
fig.show()

# %%
