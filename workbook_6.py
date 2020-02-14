"""

We run UNH vs TRV to see if there is a difference between 
running them inside or outside of the DOWJ, previous work
between UNH and McDnalds showed that this was not the case
how will the results between UNH TRV fare up

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
ct_df = pd.DataFrame.from_dict(ct,
        orient='index',columns=['Support',
        'Length','Time'])



# %%
