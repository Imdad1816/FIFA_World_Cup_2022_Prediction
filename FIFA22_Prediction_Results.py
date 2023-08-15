import pandas as pd
import pickle
from scipy.stats import poisson

#importing Data
dict_table = pickle.load(open('dict_table','rb'))
df_historical_data = pd.read_csv('Cleaned_FIFA_Worldcup_Historical_Data.csv')
df_fixture = pd.read_csv('Cleaned_FIFA_2022_WC_data.csv')

#calculation
df_Home = df_historical_data[['Home_Team','Home_Goals','Away_Goals']]
df_Away = df_historical_data[['Away_Team','Home_Goals','Away_Goals']]

#Renaming columns
df_Home=df_Home.rename(columns={'Home_Team':'Team','Home_Goals':'Goals_Scored','Away_Goals':'Goals_Conceded'})
df_Away=df_Away.rename(columns={'Away_Team':'Team','Home_Goals':'Goals_Conceded','Away_Goals':'Goals_Scored'})

#Team_Strength
df_Team_Strength = pd.concat([df_Home,df_Away],ignore_index=True).groupby('Team').mean()

#Function to predict points
def Predict_points(home,away):
    if home in df_Team_Strength.index and away in df_Team_Strength.index:
        #goals_scored*goals_conceded
        lmda_home = df_Team_Strength.at[home,'Goals_Scored']*df_Team_Strength.at[away,'Goals_Conceded']
        lmda_away = df_Team_Strength.at[away,'Goals_Scored']*df_Team_Strength.at[home,'Goals_Conceded']
        prob_home,prob_away,prob_draw=0,0,0
        for x in range(0,21): #number of goals scored by home team
            for y in range(0,21): #number of goals scored by away team
                p = poisson.pmf(x,lmda_home)*poisson.pmf(y,lmda_away)
                if(x==y):
                    prob_draw+=p
                elif x>y:
                    prob_home+=p
                else:
                    prob_away+=p
        points_home = 3*prob_home + prob_draw
        points_away = 3*prob_away + prob_draw
        return(points_home,points_away)
    else:
        return(0,0)

########Prediction of World_Cup########
#Splitting the data of fixtures
df_fixture_group=df_fixture[:48].copy()
df_fixture_knockout=df_fixture[48:56].copy()
df_fixture_quarter=df_fixture[56:60].copy()
df_fixture_semi=df_fixture[60:62].copy()
df_fixture_final=df_fixture[63:].copy()



####Group_stage####
for group in dict_table:
    teams_in_group = dict_table[group]['Team'].values
    df_fixture_group_6 = df_fixture_group[df_fixture_group['Home'].isin(teams_in_group)]
    for index , row in df_fixture_group_6.iterrows():
        home,away = row['Home'],row['Away']
        points_home,points_away = Predict_points(home,away)
        dict_table[group].loc[dict_table[group]['Team']==home,'Pts']+=points_home
        dict_table[group].loc[dict_table[group]['Team']==away,'Pts']+=points_away
    dict_table[group] = dict_table[group].sort_values('Pts',ascending=False).reset_index()
    dict_table[group] = dict_table[group][['Team','Pts']]
    dict_table[group] = dict_table[group].round(0)



#update knockout matches
for group in dict_table:
    group_winner = dict_table[group].loc[0,'Team']
    runners_up = dict_table[group].loc[1,'Team']

    df_fixture_knockout.replace({f'Winners {group}':group_winner,
                                 f'Runners-up {group}':runners_up},inplace=True)
    
df_fixture_knockout['Winner'] = '?'
#winner_function
def get_winner(df_fixture_updated):
    for index,row in df_fixture_updated.iterrows():
        home,away = row['Home'],row['Away']
        points_home,points_away = Predict_points(home,away)
        if(points_home>points_away):
            winner = home
        else:
            winner = away
        df_fixture_updated.loc[index,'Winner']=winner
    return df_fixture_updated

#update table function
def update_table(df_fixture_round_1,df_fixture_round_2):
    for (index, row) in df_fixture_round_1.iterrows():
        winner = df_fixture_round_1.loc[index,'Winner']
        match = df_fixture_round_1.loc[index,'Score']
        df_fixture_round_2.replace({f'Winners {match}':winner},inplace=True)
    df_fixture_round_2['Winner'] = '?'
    return df_fixture_round_2

####Round of 16 Knockout####
print("-------Round of 16-------")
df_fixture_knockout = get_winner(df_fixture_knockout)
print(df_fixture_knockout,"\n")

####Quarter Final Knockout####
print("-------Quarter Finals-------")
df_fixture_quarter = update_table(df_fixture_knockout,df_fixture_quarter)
df_fixture_quarter = get_winner(df_fixture_quarter)
print(df_fixture_quarter,"\n")

####Semi Final Knockout####
print("-------Semi Finals-------")
df_fixture_semi = update_table(df_fixture_quarter,df_fixture_semi)
df_fixture_semi = get_winner(df_fixture_semi)
print(df_fixture_semi,"\n")

####Final Knockout####
print("-------Final-------")
df_fixture_final = update_table(df_fixture_semi,df_fixture_final)
df_fixture_final = get_winner(df_fixture_final)
print(df_fixture_final,"\n\n\n")



print("**********Winner of 2022 FIFA World Cup :",df_fixture_final['Winner'].iloc[-1],"***********")


