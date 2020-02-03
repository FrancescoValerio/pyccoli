#%%
import multiprocessing as mp
from import_data import import_dat
from product import product
from add_rem import add, rem
from mdl import mdl_calc
from tqdm import tqdm


def plus_(args):
    x,st,ct,d,mdl = args
    if mdl_calc(add(x,ct,d),d,st) < mdl:
        return x
    
def min_(args):
    x,st,ct,d,mdl = args
    if mdl_calc(rem(x,ct),d,st) < mdl:
        return x   
     
def main():
    pass


    
def ditto_plus(cand_,st,ct,d,mdl):
    cand = cand_.copy()
    counter = 0
    used = []
    
    while True:
        found = False

        args = ((x,st,ct,d,mdl) for x in cand)

        with mp.Pool() as pool:
            for i, pattern in enumerate(pool.imap(plus_,args)):
                if pattern:
                    used.append(pattern)
                    counter += i
                    print(100*(counter/len(cand_)))
                    ct = add(pattern,ct,d)
                    mdl = mdl_calc(ct,d,st)
                    cand = cand[i+1:]
                    print(f'Current MDL: {mdl}')
                    found = True
                    break
        if not found:
            break
    return ct, used


    
def ditto_min(st,ct,d):
    mdl = mdl_calc(ct,d,st)
    print(mdl)
    p_ct = []
    for k,v in ct.items():
        if v[1]>1:
            p_ct.append(k)
    tt = len(p_ct)
    counter = 0
    while True:
        found = False
        args = ((x,st,ct,d,mdl) for x in p_ct)
        with mp.Pool() as pool:
            for i, pattern in enumerate(pool.imap(min_,args)):
                if pattern:
                    counter += i 
                    print(100*(counter/tt))
                    ct = rem(pattern,ct)
                    mdl = mdl_calc(ct,d,st)
                    p_ct = p_ct[i+1:]
                    print(f'Current MDL: {mdl}')
                    found = True
                    break
        if not found:
            break
    return ct

if __name__ == "__main__":

    st, d, cand = import_dat('./plant3.dat')
    ct = st.copy()
    mdl = mdl_calc(ct,d,st)
    print(f'Original MDL:{mdl}')
    while True:
        ct, used = ditto_plus(cand,st,ct,d,mdl)
        if mdl_calc(ct,d,st)<mdl:
            mdl = mdl_calc(ct,d,st)
        else:
            break
        ct = ditto_min(st,ct,d)
        if mdl_calc(ct,d,st)<mdl:
            mdl = mdl_calc(ct,d,st)
        else:
            break
        cand = product(ct,used)



                    
        
    
    
    
# %%


# %%
