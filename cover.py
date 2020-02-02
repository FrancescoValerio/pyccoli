##Return to this later first we need to find and thus count our patterns
#%%
# Imports
from collections import OrderedDict, Counter

# User imports
from pattern_finder import painter

# %%
def cover(codetable,dataset):    
    patterns = {}
    d = dataset
    for key, value in codetable.items():
        if value[1]>1:
            patterns[key]=value
    
    c_ord_patterns = cov_order(patterns)
    c = Counter()
    
    for x in c_ord_patterns:
        d,num = painter(x,d)
        c[x] = num
        
    for i, row in enumerate(d):
        for element in row:
            if element > 0:
                c[((i,(element,)),)] += 1
                
    for x in codetable:
        if not x in c:
            #(support,total_length_pattern,timespan_of_pattern )

            c[x] = (0,codetable[x][1],codetable[x][2])
        else:
            #(support,total_length_pattern,timespan_of_pattern )

            c[x] = (c[x] ,codetable[x][1],codetable[x][2])
    
    d = [[element for element in row if not element == 0] for row in d]
    
    # output codetable and d cannot be re-used as they're dependent 
    # supports and not independent supports
    covered_codetable = c
    covered_dataset = d
    return covered_codetable,covered_dataset

def cov_order(codetable):
    #first length in time, then pattern lengt, then support
    return{k: v for k, v in sorted(codetable.items(), 
        key=lambda item:(item[1][2],item[1][1], item[1][0]),
        reverse = True) }

    