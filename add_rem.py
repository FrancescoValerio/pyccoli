# User Import
from pattern_finder import finder

def rem(pattern,codetable):
    
    ct = codetable.copy()
    
    del ct[pattern]
    
    return ct

def add(pattern,codetable,dataset):
    
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
    