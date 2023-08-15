import pandas as pd


df_historical_data = pd.read_csv('FIFA_Worldcup_Historical_Data.csv')
df_fixture = pd.read_csv('FIFA_2022_WC_data.csv')

#cleaning_2022data
df_fixture['Home']=df_fixture['Home'].str.strip()
df_fixture['Away']=df_fixture['Away'].str.strip()

#cleaning_historic_data_with_walkover
delete_index = df_historical_data[df_historical_data['Home'].str.contains('Sweden') & df_historical_data['Away'].str.contains('Austria')].index
df_historical_data.drop(index = delete_index,inplace=True)

#Modifying score columns with not only digits
df_historical_data['Score']=df_historical_data['Score'].str.replace('[^\d-]','-',regex = True)

#cleaning historical data
df_historical_data['Home']=df_historical_data['Home'].str.strip()
df_historical_data['Away']=df_historical_data['Away'].str.strip()
df_historical_data['Score']=df_historical_data['Score'].str.strip('-')

#splitting the score into home and away goals and dropping score column
df_historical_data[['Home_Goals','Away_Goals']] = df_historical_data['Score'].str.split('-',expand = True)
df_historical_data.drop('Score',axis =1,inplace=True)

#Renaming Columns and changing datatypes
df_historical_data.rename(columns={'Home':'Home_Team','Away':'Away_Team','year':'Year'},inplace = True)
df_historical_data = df_historical_data.astype({'Home_Goals':int,'Away_Goals':int,'Year':int})

#creating Totalgoals
df_historical_data['Total_Goals'] = df_historical_data['Home_Goals']+df_historical_data['Away_Goals']


#Exporting the clean data

df_historical_data.to_csv('Cleaned_FIFA_Worldcup_Historical_Data.csv',index=False)
df_fixture.to_csv('Cleaned_FIFA_2022_WC_data.csv',index = False)