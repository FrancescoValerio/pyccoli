#%%
import pickle
from pattern_finder import finder
'''
Some functions to help with output generations
'''
def load_dictionary(file):
    """Loads a dictionary file 
    
    This helps when you want to look into a codetable within
    a jupyter environment
    
    Arguments:
        file {string} -- filelocation
    
    Returns:
        dict -- the codetable
    """
    with open(file, 'rb') as pickled_dict:
        return pickle.load(pickled_dict)
    
def write_dict(d, file): 
    """Write a dictionary file to a text file
    
    This can be used with load_dictionary() to load and 
    print a dictionary to a text file for manual review
    
    Arguments:
        d {[dict]} -- dictionary file to be used as output
        file {str} -- desired location of output
    """
    with open(f'{file}.txt','w') as out:
        for k,v in d.items():
            print(f'{k}\t\t\t{v}', file=out)
    
def painter(pattern,dataset,sign=-1):
    """Custom painter function 
    
    This painter function allows patterns to be drawn as unique
    signs and thus be distinguishable from one another, the sign
    must be given otherwise it defaults to negative 1
    remember that 0's are ignored by PYCOLLI and thus should never
    be used within dataset manipulations
    
    Arguments:
        pattern {tuple} -- patterns to be discovered in dataset
        dataset {tuple or list} -- dataset to be modified
    
    Keyword Arguments:
        sign {int} -- sign with which to paint dataset (default: {-1})
    
    Returns:
        dataset -- modified dataset
    """
    if not isinstance(dataset,list):
        d= [[x for x in row] for row in dataset]
    else:
        d=dataset
    index_points = finder(pattern,dataset)
    for point in index_points:
        first = True
        for row in pattern:
            if first:
                first = False
                d[row[0]][point:point+len(row[1])] = [sign]*len(row[1])
            else:
                d[row[0]][point:point+len(row[1])] = [sign]*len(row[1])
    return d
#%%
def compare_dictionaries(d1,d2):
    """Return the patterns two dictionaries have in common
    
    Arguments:
        d1 {dict} -- First dictionary
        d2 {dict} -- Second dictionary
    
    Returns:
        list -- Intersection of both dictionaries
    """
    d1=set(list(d1))
    d2=set(list(d2))
    return list(d1.intersection(d2))
    