#%%
# Python imports 
import math
from operator import mul
from functools import reduce
# User imports
from cover import cover

#%%

def mdl_calc(codetable,dataset,singleton_table):
    """given codetable and dataset, return an MDL
    
    Arguments:
        codetable {dict} -- input codetable
        dataset {tuple} -- tuple of tuples containng data
        singleton_table {dict} -- dictionary containing singleton info
    
    Returns:
        [float] -- Mdl length as a number
    """
    c_ct, c_d = cover(codetable,dataset)
    #(support,total_length_pattern,timespan_of_pattern )
    sum_cov_ct = sum( v[0] for v in c_ct.values() )
    sum_st     = sum( v[0] for v in singleton_table.values() )
    
    # Ln(|D|)
    mdl = ln(1)
    # Ln(|A|)
    mdl += ln(len(c_d))
    # Sigma {s[equence] in D}: Ln(|s|)
    mdl += sum( ln(len(sequence)) for sequence in c_d )
    #  L(C_p|CT)
    mdl += sum(( v[0] * x_st(v[0], sum_cov_ct) ) for v in c_ct.values())
    # Sigma {s[equence] in D}: 
    #   Ln(Omega_s) +  lu(|D^s|,|Omega_s|)
    mdl += sum( ln(len(set(row))) + lu(len(row),len(set(row))) for row in dataset)
    # Ln(|P|+1)
    amount_p = sum( 1    for v in c_ct.values() if v[1] > 1)
    mdl += ln(amount_p + 1)
    # Ln(usage(P)+1)
    usage_p  = sum( v[0] for v in c_ct.values() if v[1] > 1)
    mdl += ln(usage_p + 1)
    # lu(usage(P),|P|)
    mdl += lu(usage_p,amount_p)
    #   Sigma {p[attern] in CT}: L(p given CT)
    mdl += sum( ln(v[2]) + 
                sum(log2(x) for x in measure_columns(k)) +
                element_in__p(k,sum_st,singleton_table) 
                for k,v in c_ct.items() if v[1] > 1 )

  
    
    return mdl

#%%
def measure_columns(pattern):
    """measure depth of array
    
    [1,2,3]
    [4,5,6,7,8]
    [6,7]
    
    would return [3,3,2,1,1]
    
    this is required to properly calculate mdl size
    
    Arguments:
        pattern {tuple} -- pattern for which columns are measured
    
    Returns:
        list -- list containing lengths
    """
    col_len = []
    lengths = []
    lengths = [len(row[1]) for row in pattern]
    while True:
        if len(lengths)==0:
            break

        col_len.append(len(lengths))
        lengths = [x-1 for x in lengths]
        lengths = [x for x in lengths if x>0]

    return col_len
        
#%%
    
def element_in__p(pattern,sum_singleton,singleton_table):
    """return the mdl sum of the elements in a pattern
    
    Arguments:
        pattern {tuple} -- pattern to be summed
        sum_singleton {int} -- amount of total cover of singletons
        singleton_table {dict} -- dictionary containing all singletons
    
    Returns:
        float -- mdl amount
    """
    mdl = 0
    for row in pattern:
        for element in row[1]:
        #print(singleton_table[row])
            amount = singleton_table[((row[0],(element,)),)] [0]
        mdl += x_st(amount,sum_singleton)
    return mdl

#%%
def x_st(number,lengthCodeTable):
    """does length(x|ST) or length(x|CT)
    
    Arguments:
        number {int} -- support of given pattern
        lengthCodeTable {int} -- support of all patterns
    """                 
    return -1*log2(number/lengthCodeTable)

def log2(number):
    """Returns log2 of a given number the correct way
    
    
    Arguments:
        number {int or float} -- number to be log'd
    """
    if number==0:
        return 0
    else:
        return math.log2(number)

def lu (top,bottom):
    """Gives the log2 of an nCr
    
    Arguments:
        top {int} -- top part of nCr
        bottom {int} -- bottom part of nCr
    """
    if top<1 and bottom<1:
        return 0
    else:
        return log2(nCr(top,bottom))

def ln(number):
    """Returns the length of complexity of a given number 
    
    (see SQS or DITTO paper for more details)
    but in short it log2's a number untill it goes 
    negative and then add the required constant to it
    
    Arguments:
        number {[int]} -- Number to be coded
    """
    result = 0
    while number >= 1 :
            number = log2(number)
            result += number
    return result + log2(2.865064)


def nCr(n : int, r : int) -> int:
    """nCr function for python
    
    nCr is the amount of combinations
    https://en.wikipedia.org/wiki/Combination
    
    Arguments:
        n {int} -- total amount of elements
        r {int} -- size of combinations
    
    Returns:
        int -- amount of combinations
    """
    r = min(r, n-r)
    numer = reduce(mul, range(n, n-r, -1), 1)
    denom = reduce(mul, range(1, r+1), 1)
    return numer // denom

