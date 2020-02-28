#%%
from output_gen import create_codetables
import numpy as np


data = './output/AAPL_5y_comp.dat'
codetable = './output/AAPL_5y_comp.dict'


apple_original, apple_covered = create_codetables(data,codetable)



data = './output/dowj_5y_close.dat'
codetable = './output/dowj_5y_close.dict'


dowj_original, dowj_covered = create_codetables(data,codetable)


data = './output/workbook8/bitcoin2016.dat'
codetable = './output/workbook8/bitcoin2016.dict'


bitcoin_original, bitcoin_covered = create_codetables(data,codetable)



data = './output/workbook9/PEP_KO_5y_close.dat'
codetable = './output/workbook9/PEP_KO_5y_close.dict'


pepko_original, pepko_covered = create_codetables(data,codetable)

data = './output/UNHMCD/UNH_MCD_5y_close.dat'
codetable = './output/UNHMCD/UNH_MCD_5y_close.dict'


UNHMCD_original, UNHMCD_covered = create_codetables(data,codetable)


data = './output/UNHTRV/UNH_TRV_5y_close.dat'
codetable = './output/UNHTRV/UNH_TRV_5y_close.dict'


UNHTRV_original, UNHTRV_covered = create_codetables(data,codetable)

for i, table in enumerate([apple_covered,bitcoin_covered,dowj_covered,pepko_covered,UNHTRV_covered,UNHMCD_covered]):
    table = table.loc[table['length']!=1]
    print(i)
    print(round(np.mean(table['support'])), end=' ')
    print(round(np.std(table['support'])), end=' ')
    print(round(np.median(table['support'])))
    
    print(round(np.mean(table['length'])), end=' ')
    print(round(np.std(table['length'])), end=' ')
    print(round(np.median(table['length'])))
    
    
    print(round(np.mean(table['time'])), end=' ')
    print(round(np.std(table['time'])), end=' ')
    print(round(np.median(table['time'])))