"""
    Contain all code regarding to importing data for PYCCOLI 
"""
#%%
#Imports

from collections import Counter


#%%
#Functions
def import_dat(file: str):
    """Import a .dat file and return a singleton table and the dataset
    
    Arguments:
        file {[string]} -- [location of .dat file]
    """
    dataset = []
    with open(file,'r') as dat_file:
        for line in dat_file:
            dataset.append(tuple(int(x) for x in line.split()))
    dataset = tuple(dataset)
    
    singleton_table = Counter()
    for i,row in enumerate(dataset):
        for element in row:
            singleton_table[ ((i, (element,)), ) ] += 1
            
            if element < 1:
                raise ValueError('No value below 1 allowed')
    
    for key in singleton_table:
        #(support,total_length_pattern,timespan_of_pattern )
        singleton_table[key] = (singleton_table[key],1,1)
    return singleton_table, dataset
            
