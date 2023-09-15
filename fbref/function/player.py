import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

def scraping(url: str, id: str, comp: str, columns: list) -> pd.DataFrame:
    """ Scrape dataframe from given url

    Parameters
    ----------
    url : str
        This is the url from fbref page which we want to scrape
    id  : str
        The id html tag from the table we want to scrape (ex: standard_stats, shooting)
    comp    : str
        The name of the competition, this is used to create competition column in the DataFrame
    columns : list
        The list of columns for the DataFrame

    Returns
    -------
    a DataFrame from given url
    """
    
    page = requests.get(url)

    # workaround to get the table under comment tag
    comm = re.compile("<!--|-->")

    soup = BeautifulSoup(comm.sub("",page.text),'lxml')
    table = soup.find("table", {"id": id})

    data = {}
    rows = table.find('tbody').find_all('tr')
    for row in rows:
        temp = row.find_all('td')
        for i in range(len(temp)):
            if columns[i] in data:
                data[columns[i]].append(temp[i].text)
            else:
                data[columns[i]] = []
                data[columns[i]].append(temp[i].text)

    df = pd.DataFrame(data)
    df['Rk']= df.reset_index().index + 1
    df['Comp'] = comp
    return df

def get_standard_stats(url: str, comp: str) -> pd.DataFrame:
    columns = ['Player', 'Nation','Pos','Squad','Age','Born','MP','Starts','Min','90s','Gls','Ast','G+A','G-PK','PK','PKatt',
           'CrdY','CrdR','xG','npxG','xAG','npxG+xAG','PrgC','PrgP','PrgR','Gls/90','Ast/90',
           'G+A/90','G-PK/90','G+A-PK/90','xG/90','xAG/90','xG+xAG/90','npxG/90','npxG+xAG/90','Matches']
    
    df = scraping(url, "stats_standard", comp, columns)
    
    columns = ['Rk', 'Player', 'Nation','Pos','Squad','Comp', 'Age','Born','MP','Starts','Min','90s','Gls','Ast',
               'G+A','G-PK','PK','PKatt', 'CrdY','CrdR','xG','npxG','xAG','npxG+xAG','PrgC','PrgP','PrgR','Gls/90','Ast/90',
               'G+A/90','G-PK/90','G+A-PK/90','xG/90','xAG/90','xG+xAG/90','npxG/90','npxG+xAG/90','Matches']
    return df[columns]

def get_shooting(url: str, comp: str) -> pd.DataFrame:
    columns = ['Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born', '90s',
       'Gls', 'Sh', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'Dist',
       'FK', 'PK', 'PKatt', 'xG', 'npxG', 'npxG/Sh', 'G-xG', 'np:G-xG', 'Matches']
    
    df = scraping(url, "stats_shooting", comp, columns)
    
    columns = ['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Comp', 'Age', 'Born', '90s',
       'Gls', 'Sh', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'Dist',
       'FK', 'PK', 'PKatt', 'xG', 'npxG', 'npxG/Sh', 'G-xG', 'np:G-xG', 'Matches']
    return df[columns]

def get_passing(url: str, comp: str) -> pd.DataFrame:
    columns = ['Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born', '90s',
       'CmpTot', 'AttTot', 'CmpTot%', 'TotDist', 'PrgDist', 'CmpS', 'AttS', 'CmpS%', 'CmpM',
       'AttM', 'CmpM%', 'CmpL', 'AttL', 'CmpL%', 'Ast', 'xAG', 'xA', 'A-xAG', 'KP',
       '1/3', 'PPA', 'CrsPA', 'PrgP', 'Matches']
    
    df = scraping(url, "stats_passing", comp, columns)
    
    columns = ['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Comp', 'Age', 'Born', '90s',
       'CmpTot', 'AttTot', 'CmpTot%', 'TotDist', 'PrgDist', 'CmpS', 'AttS', 'CmpS%', 'CmpM',
       'AttM', 'CmpM%', 'CmpL', 'AttL', 'CmpL%', 'Ast', 'xAG', 'xA', 'A-xAG', 'KP',
       '1/3', 'PPA', 'CrsPA', 'PrgP']
    return df[columns]

def get_pass_type(url: str, comp: str) -> pd.DataFrame:
    columns = ['Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born', '90s',
       'Att', 'Live', 'Dead', 'FK', 'TB', 'Sw', 'Crs', 'TI', 'CK', 'In', 'Out',
       'Str', 'Cmp', 'Off', 'Blocks', 'Matches']
    
    df = scraping(url, "stats_passing_types", comp, columns)
    
    columns = ['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Comp', 'Age', 'Born', '90s',
       'Att', 'Live', 'Dead', 'FK', 'TB', 'Sw', 'Crs', 'TI', 'CK', 'In', 'Out',
       'Str', 'Cmp', 'Off', 'Blocks']
    return df[columns]

def get_gsc(url: str, comp: str) -> pd.DataFrame:
    columns = ['Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born', '90s',
               'SCA', 'SCA90', 'SCAPassLive', 'SCAPassDead', 'SCATakeOns',
               'SCAShot', 'SCAFouled', 'SCADefAct', 'GCA', 'GCA90', 'GCAPassLive',
               'GCAPassDead', 'GCATakeOns', 'GCAShot', 'GCAFouled', 'GCADefAct']
    
    df = scraping(url, "stats_gca", comp, columns)

    columns = ['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born', '90s',
               'SCA', 'SCA90', 'SCAPassLive', 'SCAPassDead', 'SCATakeOns',
               'SCAShot', 'SCAFouled', 'SCADefAct', 'GCA', 'GCA90', 'GCAPassLive',
               'GCAPassDead', 'GCATakeOns', 'GCAShot', 'GCAFouled', 'GCADefAct', 'Matches']

    return df[columns]

def get_defensive_action(url: str, comp: str) -> pd.DataFrame:
    return True

def get_possession(url: str, comp: str) -> pd.DataFrame:
    return True

def get_playing_time(url: str, comp: str) -> pd.DataFrame:
    return True

def get_misc(url: str, comp: str) -> pd.DataFrame:
    return True