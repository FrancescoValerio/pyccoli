"""
    Contain all code regarding to candidate prodiction for PYCCOLI 
"""
#Imports
import multiprocessing as mp
import itertools
# %%
def product(codetable_a,codetable_b):
    """Make the cartesian product of two patterns
    
    Arguments:
        codetable_1 {any} -- first list of patterns
        codetable_2 {any} -- seconds list of patterns
    
    Returns:
        list -- List of all possible candidates
    """
    a = list(codetable_a)
    b = list(codetable_b)
    combinations = list(itertools.product(a,b))
    
    with mp.Pool() as pool:
        results = pool.map(pattern_combiner,combinations)
    

    return results
    

def pattern_combiner(x):
    """Helper function for product function, take 2 patterns and combine
    
    Arguments:
        x {[tuple]} -- tuple by itertools.product with both patterns
    
    Returns:
        [tuple] -- Combination of both patterns
    """
    
    comb_p = {}
    pattern1 = x[0]
    pattern2 = x[1]
    
    # Make base out of key value pair out of row number and pattern
    for row in pattern1:
        comb_p[row[0]] = [x for x in row[1]]
    
    # Add new pattern to base
    for row in pattern2:
        # If it already exists within base append 
        if row[0] in comb_p:
            comb_p[row[0]] = comb_p[row[0]] + [x for x in row[1]]
        # Else create key value pait
        else:
            comb_p[row[0]] = [x for x in row[1]]
    return tuple((key,tuple(value)) for key,value in comb_p.items())    
    

