#%%
import pickle
from pattern_finder import finder
'''
Work in progress
'''
#Test
def load_dictionary(file):
    with open(file, 'rb') as pickled_dict:
        return pickle.load(pickled_dict)
    
def write_dict(d, file):   
    with open(f'{file}.txt','w') as out:
        for k,v in d.items():
            print(f'{k}\t\t\t{v}', file=out)
    
def painter(pattern,dataset,sign=-1):
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

        