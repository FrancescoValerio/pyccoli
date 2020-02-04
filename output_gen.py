import pickle
'''
Work in progress
'''
def load_dictionary(file):
    with open(file, 'rb') as pickled_dict:
        return pickle.load(pickled_dict)
    
    
    with open(file,'r') as dat_file:
        for line in dat_file:
            dataset.append([int(x) for x in line.split()])
    
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
    return d, len(index_points)
#%%

        