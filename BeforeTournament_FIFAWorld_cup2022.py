import pandas as pd
from string import ascii_uppercase as alphabet
import pickle
dict_table = {}
all_tables = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup')
for letter,i in zip(alphabet,range(9,65,7)):
    df = all_tables[i]
    df.rename(columns = {'Teamvte':'Team'},inplace =  True)
    df.pop('Qualification')
    df.iloc[:,2:]=0
    dict_table[f'Group {letter}']=df

print(dict_table)
with open('dict_table','wb') as output:
    pickle.dump(dict_table,output)