

def finder(pattern,dataset):
    d = [[element for element in row] for row in dataset]
    #find all index points that the patterns have in common
    found_indexes = []
    time_length = 0
    
    for row_n, pattern in pattern:
        #print(row_n)
        #print(pattern)
        if len(pattern)>time_length:
            time_length = len(pattern)
        
        found_indexes.append({i for i in range(len(d[row_n])) if 
                       d[row_n][i:i+len(pattern)]==list(pattern)})
        
    #print(found_indexes)
    found_indexes = set.intersection(*found_indexes)
    #remove overlapping patterns
    
    results = []
    for x in found_indexes:
        if not x-time_length+1 in results:
            results.append(x)
    
    return results
    


# %%
def painter(pattern,dataset,sign=-1):
    d= [[x for x in row] for row in dataset]
    index_points = finder(pattern,dataset)
    for point in index_points:
        first = True
        for row in pattern:
            if first:
                first = False
                d[row[0]][point:point+len(row[1])] = [sign]+[0]*(len(row[1])-1)
            else:
                d[row[0]][point:point+len(row[1])] = [0]*len(row[1])
    return d, len(index_points)
#%%
