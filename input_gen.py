#%%
########################################################################
# Imports
# Python
import getopt
import re 
import sys
# 3rd Party
import pandas as pd 
import sklearn.cluster


########################################################################
# Functions
def import_csv_to_df(file):
    """Import a csv file and return it as a pandas.Dataframe
    
    Arguments:
        file {string} -- File location
    
    Returns:
        df -- A dataframe of the file
    """

    try:
        iden = re.search(r'\w/(.+?).csv',file).group(1)
    except AttributeError:
        try:
            iden = re.search(r'/(.+?).csv',file).group(1)
        except AttributeError:
            print('Function only accepts forward slash')

    df = pd.read_csv(f'{file}',index_col=0,parse_dates=True ).iloc[::-1]
    
    #Adjusted close is not needed on this level of precision
    if 'Adj Close' in list(df):
        df = df.drop('Adj Close',axis=1)
    df.columns = [f'{name}-{iden}' for name in list(df)]

    return df.iloc[::-1]

def join_dataframes(*dataframes):
    """Join two dataframes by corresponding index values
    
    Returns:
        dataframe -- Joined dataframes
    """
    return pd.concat(list(dataframes),axis=1)

def remove_NaN_rows(dataframe):
    """Remove any rows containing NaN
    
    Arguments:
        dataframe {Dataframe} -- Input dataframe
    
    Returns:
        Dataframe -- Dataframe without rows containing NaN
    """
    return dataframe.dropna()

def filter_columns(dataframe, *filters):
    """Allow dataframe column if substring contains any filter word        
    
    Arguments:
        dataframe {Dataframe} -- Input dataframe
        *filters  {string}    -- Word that substring needs to match
    
    Returns:
        Dataframe -- Filtered dataframe
    """
    output =[]
    for f in filters:
        x = dataframe.filter(like=f)
        output.append(x)
    return join_dataframes(*output)

def row_diff(dataframe, option='%'):
    """Turn rows into (percentage) difference
    
    Arguments:
        dataframe {Dataframe} -- Input dataframe
    
    Keyword Arguments:
        option {string} -- Choice between % and absolute difference 
                            (default: {'%'})
    
    Returns:
        Dataframe -- Dataframe with changed values
    """
    if option == '%':
        return dataframe.pct_change().iloc[1:]
    elif option == 'abs':
        return dataframe.diff().iloc[1:]

def kmean_columns(dataframe,nm_clusters = 10):
    """
    Add a kmean clustered label for every column in table
    
    
    Returns:
        Dataframe -- Dataframe containing clustered columns
        

    """
    #Iterate through every column
    for head, column in dataframe.iteritems():
        #    DO NOT CHANGE MINIBATCH PARAMETERS
        #    OR YOU WILL NOT BE ABLE TO RECREATEE
        #    RESULTS
        kmean =  sklearn.cluster.MiniBatchKMeans(
            n_clusters=nm_clusters,random_state=12).fit(
                column.values.reshape(-1,1))

        # Assign out of order labels to the column
        bad_label = kmean.predict(column.values.reshape(-1,1))
        ##dataframe[f'{head}_-L-bad'] = bad_label

        # zip values and labels together and sort them from small to big
        lab_val = list(zip(column.values,bad_label))
        lab_val.sort()

        # go through each label and when not seen before add it to guide
        guide = {}
        counter = 0
        for x in lab_val:
            if not x[1] in guide:
                counter += 1
                guide[x[1]] = counter

        # guide contains the information now in the right order 
        # in the order guide[unordered_label] = ordered_label

        # replace all the unordered labels into ordered labels
        good_label = [guide[x] for x in bad_label]
        # 1 is now always the smallest with len(guide) being the biggest

        # add the ordered labels to the dataframe
        dataframe[f'{head}_-LB'] = good_label

    return dataframe

    ##gg = sklearn.cluster.MiniBatchKMeans(n_clusters=10).fit(qq.iloc[:,2].values.reshape(-1,1))
    ##gg.predict(qq.iloc[:,2].values.reshape(-1,1))
def export_to_pyccoli(dataframe,output_file):
    """Take a df and export it to ditto friendly input with documenation
    
    Arguments:
        dataframe {Dataframe} -- Dataframe to be outputted
        output_file {string} -- file location for output
    """
    data_file = open(f'{output_file}.dat','wt')
    text_file = open(f'{output_file}.txt','wt')
    print(f'This is automated documentation for file {output_file}'+
          '\n the following columns are represented within \n' +
          f'{output_file}.dat ',file = text_file)
    counter = 0
    for head, c in dataframe.iteritems():
        counter +=1
        col=str(list(c)).replace(',','').replace('[','').replace(']','')
        print(len(col.split()))
        print(col, file = data_file)
        print(f'{counter}. {head}',   file = text_file)
            
def index_list(index):
    if index in ('dow','DOW','Dow'):
        file = './Data/Components of the Dow Jones.csv'
    elif index in ('ndaq','nsdaq','ndq'):
        file = './Data/Components of the Nasdaq 100.csv'
    elif index in ('sp','sp500'):
        file = './Data/Components of the S&P 500.csv'
    else:
        file = index
    df = pd.read_csv(file,index_col=0, sep='\t')
    return [x.rstrip() for x in list(df.iloc[:,1])]
#aapl=import_csv_to_df('./Data/AAPL.csv')

#%%
dow =[]

#for x in index_list('sp'):
    
    #if x in ('V','GS','DOW'):
     #   continue
    
    #dow.append(import_csv_to_df(f'./Stocks/{x}.csv'))
    #dow.append(import_csv_to_df(f'./Stocks/1ndex_DOW.csv'))
#dow = join_dataframes(*dow)

dow = import_csv_to_df('./AAPL.csv').iloc[-1500:]
#a = filter_columns(dow,'Close')
a = remove_NaN_rows(dow)
#%%
a = row_diff(a)
a = kmean_columns(a,5)
#a = filter_columns(a,'LB')

export_to_pyccoli(filter_columns(a,'LB'),'AAPL_5y_comp')
a.to_excel('AAPL_5y_comp.xlsx')



# %%
