#%%
# Python imports 
import math
from operator import mul
from functools import reduce
# User imports
from cover import cover

#%%

def mdl_calc(codetable,dataset,singleton_table):
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
    mdl = 0
    for row in pattern:
        for element in row[1]:
        #print(singleton_table[row])
            amount = singleton_table[((row[0],(element,)),)] [0]
        mdl += x_st(amount,sum_singleton)
    return mdl

#%%
def x_st(number,lengthCodeTable):
  return -1*log2(number/lengthCodeTable)

def log2(number):
  if number==0:
      return 0
  else:
      return math.log2(number)

def lu (top,bottom):
  if top<1 and bottom<1:
      return 0
  else:
      return log2(nCr(top,bottom))

def ln(number):
  result = 0
  while number >= 1 :
          number = log2(number)
          result += number
  return result + log2(2.865064)


def nCr(n : int, r : int) -> int:
  r = min(r, n-r)
  numer = reduce(mul, range(n, n-r, -1), 1)
  denom = reduce(mul, range(1, r+1), 1)
  return numer // denom

