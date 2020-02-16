#%%
import pandas as pd
from input_gen import row_diff, kmean_columns, export_to_pyccoli, filter_columns

from pyccoli import pyccoli

# %%
#An example of how to use PYCCOLI for your own time series
# in this case we are looking at bitcoin data from 2016 till 2020
def make_the_file():
    data = pd.read_csv('./Stocks/1Bitcoin4y.csv')
    date = pd.to_datetime(data['<DATE>'],format= '%Y%m%d')
    del data['<TIME>']
    data = row_diff(data)
    data = kmean_columns(data,5)
    data['<DATE>'] = date
    del data['<DATE>_-LB']
    data.to_excel('bitcoin2016.xlsx')

    export_to_pyccoli(filter_columns(data,'LB'), 'bitcoin2016')

# %%
def run_pyccoli():
    pyccoli('bitcoin2016')

#then do 
#make_the_file
#run_pyccoli
if __name__ == "__main__":
    run_pyccoli()