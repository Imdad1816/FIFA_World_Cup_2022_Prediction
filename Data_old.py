from bs4 import BeautifulSoup
import requests
import pandas as pd

years = [1930,1934,1938,1950,1958,1962,1966,1970,1974,1978,1982,1986,1990,1994,1998,2002,2006,2010,2014,2018]
def get_matches(year):
    web = f'https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'
    response = requests.get(web)
    content = response.text
    soup = BeautifulSoup(content,'lxml')
    matches = soup.find_all('div',class_='footballbox' )

    Home = []
    Score=[]
    Away =[]

    for match in matches:
        Home.append(match.find('th',class_='fhome').get_text())
        Score.append(match.find('th',class_='fscore').get_text())
        Away.append(match.find('th',class_='faway').get_text())

    dict_football = {'Home':Home,'Score':Score,'Away':Away}
    dataframe_football = pd.DataFrame(dict_football)
    dataframe_football['year'] = year
    return (dataframe_football)

#historical_data
FIFA_Matches = [get_matches(year) for year in years]
dataframe_football = pd.concat(FIFA_Matches,ignore_index=True)
dataframe_football.to_csv('FIFA_Worldcup_Historical_Data.csv',index = False)

#for 2022 WC
def get_match(year):
    web = f'https://web.archive.org/web/20221115040351/https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'
    response = requests.get(web)
    content = response.text
    soup = BeautifulSoup(content,'lxml')
    matches = soup.find_all('div',class_='footballbox' )

    Home = []
    Score=[]
    Away =[]

    for match in matches:
        Home.append(match.find('th',class_='fhome').get_text())
        Score.append(match.find('th',class_='fscore').get_text())
        Away.append(match.find('th',class_='faway').get_text())

    dict_football = {'Home':Home,'Score':Score,'Away':Away}
    dataframe_football = pd.DataFrame(dict_football)
    dataframe_football['year'] = year
    return (dataframe_football)

df_2022fixture = get_match(2022)
df_2022fixture.to_csv('FIFA_2022_WC_data.csv',index = False) 