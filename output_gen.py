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

def write_df(df, file): 
    """Write a Dataframe file to a text file
    
   
    Arguments:
        df {Dataframe} -- dataframe file to be used as output
        file {str} -- desired location of output
    """
    with open(f'{file}.txt','w') as out:
        print(df.to_string(max_colwidth=2000), file=out)
            
             
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
    
    
def xyc(df2,date,data,color):
    """Helper function for making graphs using Bokeh multi-line
    
    Arguments:
        df2 {np.array} -- dataframe to be used for graph
        date {string} -- Name of the column containing the date
        
        data {sting} -- Name of col of to be plotted data
        color {string} -- name of col with what color data should be
    
    Returns:
        tuple -- multiline compatible tuple
    """
    xs=[]
    ys=[]
    x=[df2.iloc[0,:][date]]
    y=[df2.iloc[0,:][data]]
    c=[df2.iloc[0,:][color]]

    for row in df2.iterrows():
        row = row[1]
        if not c[-1] == row[color]:
            xs.append(x)
            ys.append(y)
            
            c.append(row[color])

            x=[x[-1]]
            y=[y[-1]]

        y.append(row[data])
        x.append(row[date])


    xs.append(x)
    ys.append(y)
    return xs,ys,c

import pandas as pd
from import_data import import_dat
from collections import OrderedDict, Counter
from pattern_finder import painter
from cover import cov_order



#data = './output/AAPL_5y_comp.dat'
#codetable = './output/AAPL_5y_comp.dict'


def create_codetables(data,codetable):

    st, d = import_dat(data)
    codetable = load_dictionary(codetable)



    # Create separate dictionary for the patterns
    patterns = {}

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
            
    for x in codetable:
        # If it doesn't exist in the covered codetable, add it
        if not x in c:
            #(support,total_length_pattern,timespan_of_pattern )

            c[x] = (0,codetable[x][1],codetable[x][2])
        #Otherwise just add the length and timespan of the patterns
        else:
            #(support,total_length_pattern,timespan_of_pattern )

            c[x] = (c[x] ,codetable[x][1],codetable[x][2])

    # C is now our covered codetable and codetable is the original
    '''
    This can be tested by checking the difference between 
    codetable[((0,(2,)),)]
    and
    c[((0,(2,)),)]
    '''
    original_ct = pd.DataFrame.from_dict(codetable, orient='index'
                , columns=['support','length','time']).sort_values(
                    'support')[::-1]
    covered_ct = pd.DataFrame.from_dict(c, orient='index', columns=[
        'support','length','time']).sort_values('support')[::-1]
    return original_ct, covered_ct