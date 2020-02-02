#%%

from import_data import import_dat
from product import product
from add_rem import add
from mdl import mdl_calc

def main():
    pass
    
if __name__ == "__main__":

    st, d = import_dat('./dowjones_long_complete.dat')
    ct = st
    cand = product(st,st)
    mdl = mdl_calc(ct,d,st)
    print(mdl)
    for i,x in enumerate(cand):
        print(mdl_calc(add(x,ct,d),d,st))
        if i==5:
            break

    # %%
