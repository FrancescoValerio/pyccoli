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
        file {[string]} -- location of .dat file
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
            
#Unused code, bugs out on certain styles of dataset
def candidates(dataset):
    """Generate first generation of candidates
    
    The manual generation of candidates gives a smaller set of 
    candidates than the cartesian product of the singletons
    thus this method speeds up the first generation of pycolli
    significantly, however, it does require a database to be 
    rectangular, which pycolli doesn't require. As such it is
    not implemented.
    
    Arguments:
        dataset {[tuple]} -- dataset in the form of ((1,2,3,4),)
    
    Returns:
        [list] -- list of all candidates
    """
    cand = []
    for x in range(len(dataset[0])):
        for y in range(len(dataset)):
            # Every horizontal candidate
            if x > 0:
                cand.append(((y,(dataset[y][x-1],dataset[y][x])),))
            if y > 0:
                cand.append(((y-1,(dataset[y-1][x])),(y,(dataset[y][x]))))
    return list(set(cand))
                