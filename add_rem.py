# User Import
from pattern_finder import finder

def rem(pattern,codetable):
    """Returns copy of codetable without the given pattern
    
    Arguments:
        pattern {tuple} -- Tuple of tuples representing pattern
        codetable {dict} -- Dictionary containing all patterns
    
    Returns:
        dict -- Copy of dictionary without given pattern
    """
    
    ct = codetable.copy()
    
    del ct[pattern]
    
    return ct

def add(pattern,codetable,dataset):
    """Returns copy of codetable with the given pattern adde
    
    Arguments:
        pattern {tuple} -- Tuple of tuples representing the pattern
        codetable {dict} -- Dictionary containing all patterns
        dataset {tuple} -- tuple of tuples containing the dataset
    
    Returns:
        dict -- Copy of dictionary with the given pattern added
    """
    
    ct = codetable.copy()
    len_p = 0
    time_p = 0
    
    for row in pattern:
        
        len_p += len(row[1])
        
        if len(row[1])>time_p:
            time_p = len(row[1])
            
    #(support,total_length_pattern,timespan_of_pattern )
    ct[pattern] =  (len(finder(pattern,dataset)),len_p,time_p)
    return ct
    