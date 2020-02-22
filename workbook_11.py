#%%
import pandas as pd
from input_gen import row_diff, kmean_columns, export_to_pyccoli, filter_columns

from pyccoli import pyccoli

# %%
#An example of how to use PYCCOLI for your own time series
# in this case we are looking at bitcoin data from 2016 till 2020
def make_the_file():
    data = pd.read_csv('./Stocks/bitcoin2016_hourly.csv')
    date = pd.to_datetime(data['<DATE>'],format= '%Y%m%d')
    del data['<DATE>']
    tijd = data['<TIME>']
    del data['<TIME>']
    data = row_diff(data)
    inf =  max(data['<VOL>'])
    data['<VOL>'] = [0 if x == inf else x for x in data['<VOL>'] ]
    data = kmean_columns(data,10)
    data['<DATE>'] = date
    data['<TIME>'] = tijd
    #%%


    data.to_excel('bitcoin2016_hourly.xlsx')

    export_to_pyccoli(filter_columns(data,'LB'), 'bitcoin2016_hourly')


# %%
def run_pyccoli():
    pyccoli('bitcoin2016_hourly')

#then do 
#make_the_file
#run_pyccoli
if __name__ == "__main__":
    #make_the_file()
    run_pyccoli()


#%%

# %%
