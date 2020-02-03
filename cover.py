"""
Covers the dataset using a codetable and returns a covered 
    dataset and codetable.

"""
#%%
# Imports
from collections import OrderedDict, Counter

# User imports
from pattern_finder import painter

# %%
def cover(codetable,dataset):    
    
    # Create separate dictionary for the patterns
    patterns = {}
    d = dataset
    
    # Add all patterns from the codetable to the pattern dictionary
    for key, value in codetable.items():
        if value[1]>1:
            patterns[key]=value
    
    # Order the patterns dictionary
    c_ord_patterns = cov_order(patterns)
    
    # Initialize a counter dictionary
    c = Counter()
    
    # For patterns in order, go over the dataset
    for x in c_ord_patterns:
        # 'Paint' the dataset with 0's where covered and return p amount
        d,num = painter(x,d)
        # Use pattern amount for value, and pattern for key, for dict
        c[x] = num
        
    # Once all patterns have covered the dataset
    # Go over the covered dataset element by element and count
    #  how often an element appears
    for i, row in enumerate(d):
        for element in row:
            if element > 0:
                c[((i,(element,)),)] += 1
    
    # Iterate over every pattern in the original code table
    for x in codetable:
        # If it doesn't exist in the covered codetable, add it
        if not x in c:
            #(support,total_length_pattern,timespan_of_pattern )

            c[x] = (0,codetable[x][1],codetable[x][2])
        #Otherwise just add the length and timespan of the patterns
        else:
            #(support,total_length_pattern,timespan_of_pattern )

            c[x] = (c[x] ,codetable[x][1],codetable[x][2])
    
    # Remove all the zero's from the covered dataset
    d = [[element for element in row if not element == 0] for row in d]
    
    # output codetable and d cannot be re-used as they're dependent 
    # supports and not independent supports
    covered_codetable = c
    covered_dataset = d
    return covered_codetable,covered_dataset

def cov_order(codetable):
    """
    Take a codetable and return it in order, time,length,support [desc]
    
    
    Arguments:
        codetable {[dict]} -- codetable to be ordered
    """
    #first length in time, then pattern lengt, then support
    # This is different from DITTO as 
    return{k: v for k, v in sorted(codetable.items(), 
        key=lambda item:(item[1][2],item[1][1], item[1][0]),
        reverse = True) }

    