def finder(pattern,dataset):
    """Return all the index locations of the given pattern
    
    Arguments:
        pattern {tuple} -- Pattern (multi- or uni=variate)
        dataset {[tuple]} -- Dataset to be searched
    
    Returns:
        list -- Array containing all index locations
    """
    if not isinstance(dataset,list):
        d= [[x for x in row] for row in dataset]
    else:
        d=dataset    #find all index points that the patterns have in common
    found_indexes = []
    time_length = 0
    
    for row_n, pattern in pattern:
        #print(row_n)
        #print(pattern)
        if len(pattern)>time_length:
            time_length = len(pattern)
        
        found_indexes.append({i for i in range(len(d[row_n])) if 
                       d[row_n][i:i+len(pattern)]==list(pattern)})
        
    #print(found_indexes)
    found_indexes = set.intersection(*found_indexes)
    #remove overlapping patterns
    
    results = []
    for x in found_indexes:
        if not x-time_length+1 in results:
            results.append(x)
    
    return results
    


# %%
def painter(pattern,dataset,sign=-1):
    """Painter functions that removes found patterns from dataset
    
    Painter function covers first element of pattern with sign
    and then covers all remaining pattern spots with zero's as
    zero's are ignored by PYCOLLI they in essence are removed
    without having to modify the list length in place which would
    mess with the indexes found by the finder functions
    
    Arguments:
        pattern {tuple} -- see finder
        dataset {tuple} -- see finder
    
    Keyword Arguments:
        sign {int} -- sign with which to decorate first instance
         (default: {-1})
    
    Returns:
        [tuple] -- returns modified dataset and amount of points changed
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
                d[row[0]][point:point+len(row[1])] = [sign]+[0]*(len(row[1])-1)
            else:
                d[row[0]][point:point+len(row[1])] = [0]*len(row[1])
    return d, len(index_points)
#%%
