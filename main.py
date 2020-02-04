#%%
import pickle
import multiprocessing as mp
from import_data import import_dat
from product import product
from add_rem import add, rem
from mdl import mdl_calc



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


    
def ditto_plus(cand_,st,ct,d,mdl,cpu=0):
    if cpu ==0:
        cpu = None
    cand = cand_.copy()
    counter = 0
    used = []
    
    while True:
        found = False

        args = ((x,st,ct,d,mdl) for x in cand)

        with mp.Pool(cpu) as pool:
            for i, pattern in enumerate(pool.imap(plus_,args)):
                if pattern:
                    used.append(pattern)
                    counter += i
                    print( f'{round(100*(counter/len(cand_)),2)}%' ,end='\r')
                    ct = add(pattern,ct,d)
                    mdl = mdl_calc(ct,d,st)
                    cand = cand[i+1:]
                    #print(f'Current MDL: {mdl}')
                    found = True
                    break
        if not found:
            print(f'After adding codes:\t\t{mdl}')
            break
    return ct, used


    
def ditto_min(st,ct,d,cpu=0):
    if cpu == 0:
        cpu = None
    mdl = mdl_calc(ct,d,st)
    #print(mdl)
    p_ct = []
    for k,v in ct.items():
        if v[1]>1:
            p_ct.append(k)
    tt = len(p_ct)
    counter = 0
    while True:
        found = False
        args = ((x,st,ct,d,mdl) for x in p_ct)
        with mp.Pool(cpu) as pool:
            for i, pattern in enumerate(pool.imap(min_,args)):
                if pattern:
                    counter += i 
                    print(f'{round(100*(counter/tt),2)}%',end='\r')
                    ct = rem(pattern,ct)
                    mdl = mdl_calc(ct,d,st)
                    p_ct = p_ct[i+1:]
                    #print(f'Current MDL: {mdl}')
                    found = True
                    break
        if not found:
            print(f'After pruning codes:\t\t{mdl}')
            break
    return ct

if __name__ == "__main__":
    output_generation = False
    filename = 'AAPL_5y_comp'
    st, d = import_dat(f'./{filename}.dat')
    
    
    cand = product(st,st)
    ct = st.copy()
    mdl = mdl_calc(ct,d,st)
    print(f'Original MDL:\t\t\t{mdl}')
    gen = 0
    if output_generation:
        while True:
            gen += 1
            ct, used = ditto_plus(cand,st,ct,d,mdl,16)
            
            if mdl_calc(ct,d,st)<mdl:
                mdl = mdl_calc(ct,d,st)
                with open(f'./plus_{filename}_{gen}.txt','w') as o:
                    for key,value in ct.items():
                        print(f'{key} \t {value}',file=o)
            else:
                print('Finished')
                break
            
            
            ct = ditto_min(st,ct,d,16)
            
            
            if mdl_calc(ct,d,st)<mdl:
                mdl = mdl_calc(ct,d,st)
                with open(f'./min_{filename}_{gen}.txt','w') as o:
                    for key,value in ct.items():
                        print(f'{key} \t {value}',file=o)
            else:
                print('Finished')
                break
            
            cand = product(ct,used)
    else:
        while True:
            gen += 1
            ct, used = ditto_plus(cand,st,ct,d,mdl,16)
            
            mdl = mdl_calc(ct,d,st)
            
            ct = ditto_min(st,ct,d,16)
            
            
            if not mdl_calc(ct,d,st)<mdl:
                with open(f'./output/{filename}.txt','w') as o:
                    for key,value in ct.items():
                        print(f'{key} \t {value}',file=o)
                with open(f'./output/{filename}.dict','wb') as out_pickle:
                    pickle.dump(ct,out_pickle,protocol=pickle.HIGHEST_PROTOCOL)
                
                print('Finished')
                break
            
            mdl = mdl_calc(ct,d,st)
            
            cand = product(ct,used)
        
    

                    
        
    
    
    
# %%


# %%
