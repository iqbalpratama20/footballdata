import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def scraping(url: str, id: str, comp: str, columns: list) -> pd.DataFrame:
    """ Scrape dataframe from given url for non big 5 Leagues

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
    df.replace('', np.nan, inplace=True)
    df.fillna('0', inplace=True)
    return df

def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """ Clean dataframe for big 5 leagues

    Parameters
    ----------
    df  : pd.DataFrame
        Source dataframe from given url
    
    Returns
    -------
    cleaned Dataframe with missing values also filled
    """

    df = df.droplevel(level=0, axis=1)
    df.drop(df[df['Rk'] == 'Rk'].index, inplace=True)
    df['Comp'] = df['Comp'].apply(lambda x: ' '.join(x.split(' ')[1:]))
    df['Rk'] = df['Rk'].astype('int64')
    df.fillna('0', inplace=True)
    return df

def get_standard_stats(url: str, comp: str = None) -> pd.DataFrame:
    columns = ['Player', 'Nation','Pos','Squad','Age','Born','MP','Starts','Min','90s','Gls','Ast','G+A','G-PK','PK','PKatt',
           'CrdY','CrdR','xG','npxG','xAG','npxG+xAG','PrgC','PrgP','PrgR','Gls/90','Ast/90',
           'G+A/90','G-PK/90','G+A-PK/90','xG/90','xAG/90','xG+xAG/90','npxG/90','npxG+xAG/90','Matches']
    
    if comp:
        df = scraping(url, "stats_standard", comp, columns)
    else:
        df = clean_df(pd.read_html(url)[0])

    columns = ['Rk', 'Player', 'Nation','Pos','Squad','Comp', 'Age','Born','MP','Starts','Min','90s','Gls','Ast',
               'G+A','G-PK','PK','PKatt', 'CrdY','CrdR','xG','npxG','xAG','npxG+xAG','PrgC','PrgP','PrgR','Gls/90','Ast/90',
               'G+A/90','G-PK/90','G+A-PK/90','xG/90','xAG/90','xG+xAG/90','npxG/90','npxG+xAG/90','Matches']
    if comp:
        return df[columns]
    df.columns = columns
    return df
    

def get_shooting(url: str, comp: str = None) -> pd.DataFrame:
    columns = ['Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born', '90s',
       'Gls', 'Sh', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'Dist',
       'FK', 'PK', 'PKatt', 'xG', 'npxG', 'npxG/Sh', 'G-xG', 'np:G-xG', 'Matches']
    
    if comp:
        df = scraping(url, "stats_shooting", comp, columns)
    else:
        df = clean_df(pd.read_html(url)[0])
    
    columns = ['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Comp', 'Age', 'Born', '90s',
       'Gls', 'Sh', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'Dist',
       'FK', 'PK', 'PKatt', 'xG', 'npxG', 'npxG/Sh', 'G-xG', 'np:G-xG', 'Matches']
    
    if comp:
        return df[columns]
    df.columns = columns
    return df

def get_passing(url: str, comp: str = None) -> pd.DataFrame:
    columns = ['Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born', '90s',
       'Completed Passes Total', 'Attempted Passes Total', 'Completed Passes Total%', 
       'Total Passing Distance', 'Progressive Passing Distance', 'Completed Short Passes', 
       'Attempted Short Passes', 'Completed Short Passes%', 'Completed Medium Passes', 'Attempted Medium Passes', 
       'Completed Medium Passes%', 'Completed Long Passes', 'Attempted Long Passes', 'Completed Long Passes%', 
       'Ast', 'xAG', 'xA', 'A-xAG', 'Key Passes', 'Passes Into Final 3rd', 'Passes Into Pen Area', 
       'Crossing Into Pen Area', 'Progressive Passes', 'Matches']
    
    if comp:
        df = scraping(url, "stats_passing", comp, columns)
    else:
        df = clean_df(pd.read_html(url)[0])
    
    columns = ['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Comp', 'Age', 'Born', '90s',
       'Completed Passes Total', 'Attempted Passes Total', 'Completed Passes Total%', 
       'Total Passing Distance', 'Progressive Passing Distance', 'Completed Short Passes', 
       'Attempted Short Passes', 'Completed Short Passes%', 'Completed Medium Passes', 'Attempted Medium Passes', 
       'Completed Medium Passes%', 'Completed Long Passes', 'Attempted Long Passes', 'Completed Long Passes%', 
       'Ast', 'xAG', 'xA', 'A-xAG', 'Key Passes', 'Passes Into Final 3rd', 'Passes Into Pen Area', 
       'Crossing Into Pen Area', 'Progressive Passes', 'Matches']
    
    if comp:
        return df[columns]
    df.columns = columns
    return df

def get_pass_type(url: str, comp: str = None) -> pd.DataFrame:
    columns = ['Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born', '90s',
       'Att', 'Live', 'Dead', 'FK', 'TB', 'Sw', 'Crs', 'TI', 'CK', 'In', 'Out',
       'Str', 'Cmp', 'Off', 'Blocks', 'Matches']
    
    if comp:
        df = scraping(url, "stats_passing_types", comp, columns)
    else:
        df = clean_df(pd.read_html(url)[0])
    
    columns = ['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Comp', 'Age', 'Born', '90s',
       'Att', 'Live', 'Dead', 'FK', 'TB', 'Sw', 'Crs', 'TI', 'CK', 'In', 'Out',
       'Str', 'Cmp', 'Off', 'Blocks', 'Matches']
    
    if comp:
        return df[columns]
    df.columns = columns
    return df

def get_gsc(url: str, comp: str = None) -> pd.DataFrame:
    columns = ['Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born', '90s',
               'SCA', 'SCA90', 'SCAPassLive', 'SCAPassDead', 'SCATakeOns',
               'SCAShot', 'SCAFouled', 'SCADefAct', 'GCA', 'GCA90', 'GCAPassLive',
               'GCAPassDead', 'GCATakeOns', 'GCAShot', 'GCAFouled', 'GCADefAct', 'Matches']
    
    if comp:
        df = scraping(url, "stats_gca", comp, columns)
    else:
        df = clean_df(pd.read_html(url)[0])

    columns = ['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Comp', 'Age', 'Born', '90s',
               'SCA', 'SCA90', 'SCAPassLive', 'SCAPassDead', 'SCATakeOns',
               'SCAShot', 'SCAFouled', 'SCADefAct', 'GCA', 'GCA90', 'GCAPassLive',
               'GCAPassDead', 'GCATakeOns', 'GCAShot', 'GCAFouled', 'GCADefAct', 'Matches']

    if comp:
        return df[columns]
    df.columns = columns
    return df

def get_defensive_action(url: str, comp: str = None) -> pd.DataFrame:
    columns = ['Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born', '90s',
               'Tackles', 'Tackles Won', 'Def 3rd Tackles', 'Mid 3rd Tackles',
               'Att 3rd Tackles', 'Dribblers Tackled', 'Dribbles Challenged',
               'Dribbles Challenged%', 'Challenges Lost', 'Blocks', 'Shots Blocked', 
               'Pass Blocked', 'Interceptions', 'Interceptions+Tackles', 'Clearances', 'Errors', 'Matches']

    if comp:
        df = scraping(url, "stats_defense", comp, columns)
    else:
        df = clean_df(pd.read_html(url)[0])

    columns = ['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Comp', 'Age', 'Born', '90s',
               'Tackles', 'Tackles Won', 'Def 3rd Tackles', 'Mid 3rd Tackles',
               'Att 3rd Tackles', 'Dribblers Tackled', 'Dribbles Challenged',
               'Dribbles Challenged%', 'Challenges Lost', 'Blocks', 'Shots Blocked', 
               'Pass Blocked', 'Interceptions', 'Interceptions+Tackles', 'Clearances', 'Errors', 'Matches']
 
    if comp:
        return df[columns]
    df.columns = columns
    return df

def get_possession(url: str, comp: str = None) -> pd.DataFrame:
    columns = ['Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born', '90s',
               'Touches', 'Def Pen Touches', 'Def 3rd Touches', 'Mid 3rd Touches',
               'Att 3rd Touches', 'Att Pen Touches', 'Live Touches', 'TakeOns Attempted',
               'Successful TakeOns', 'Successful TakeOns%', 'TakeOns Tackled', 'TakeOns Tackled %', 
               'Carries', 'Total Carries Distance', 'Progressive Carries Distance', 'Progressive Carries',
               'Carries to Final Third', 'Carries to Pen Area', 'Miscontrols', 'Dispossessed', 
               'Passes Received', 'Progressive Passes Received', 'Matches']
    
    if comp:
        df = scraping(url, "stats_possession", comp, columns)
    else:
        df = clean_df(pd.read_html(url)[0])

    columns = ['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Comp', 'Age', 'Born', '90s',
               'Touches', 'Def Pen Touches', 'Def 3rd Touches', 'Mid 3rd Touches',
               'Att 3rd Touches', 'Att Pen Touches', 'Live Touches', 'TakeOns Attempted',
               'Successful TakeOns', 'Successful TakeOns%', 'TakeOns Tackled', 'TakeOns Tackled %', 
               'Carries', 'Total Carries Distance', 'Progressive Carries Distance', 'Progressive Carries',
               'Carries to Final Third', 'Carries to Pen Area', 'Miscontrols', 'Dispossessed', 
               'Passes Received', 'Progressive Passes Received', 'Matches']

    if comp:
        return df[columns]
    df.columns = columns
    return df

def get_playing_time(url: str, comp: str = None) -> pd.DataFrame:
    columns = ['Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born',
               'Matches Played', 'Minutes', 'Minutes per Match', 'Minutes%', '90s',
               'Starts', 'Minutes per Start', 'Complete Match', 'Subs', 'Minutes per Subs',
               'Unused Subs', 'PPM', 'onG', 'onGA', 'G+/-', 'G+/-90', 'On-Off', 'onxG', 'onxGA',
               'xG+/-', 'xG+/-90', 'xGOn-Off', 'Matches']
    
    if comp:
        df = scraping(url, "stats_playing_time", comp, columns)
    else:
        df = clean_df(pd.read_html(url)[0])

    columns = ['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Comp', 'Age', 'Born',
               'Matches Played', 'Minutes', 'Minutes per Match', 'Minutes%', '90s',
               'Starts', 'Minutes per Start', 'Complete Match', 'Subs', 'Minutes per Subs',
               'Unused Subs', 'PPM', 'onG', 'onGA', 'G+/-', 'G+/-90', 'On-Off', 'onxG', 'onxGA',
               'xG+/-', 'xG+/-90', 'xGOn-Off', 'Matches']
    
    if comp:
        return df[columns]
    df.columns = columns
    return df

def get_misc(url: str, comp: str = None) -> pd.DataFrame:
    columns = ['Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born', '90s',
               'Yellow Card', 'Red Card', '2nd Yellow', 'Fouls', 'Fouled',
               'Offsides', 'Crosses', 'Interceptions', 'Tackles Won', 'Pen Won',
               'Pen Conceded', 'Own Goals', 'Recoveries', 'Aerial Won', 'Aerial Lost', 
               'Aerial Won%', 'Matches']
    
    if comp:
        df = scraping(url, "stats_misc", comp, columns)
    else:
        df = clean_df(pd.read_html(url)[0])

    columns = ['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Comp', 'Age', 'Born', '90s',
               'Yellow Card', 'Red Card', '2nd Yellow', 'Fouls', 'Fouled',
               'Offsides', 'Crosses', 'Interceptions', 'Tackles Won', 'Pen Won',
               'Pen Conceded', 'Own Goals', 'Recoveries', 'Aerial Won', 'Aerial Lost', 
               'Aerial Won%', 'Matches']
    
    if comp:
        return df[columns]
    df.columns = columns
    return df

def combine_df(standard: pd.DataFrame, shooting: pd.DataFrame, passing: pd.DataFrame,
               pass_types: pd.DataFrame, gsc: pd.DataFrame, defense: pd.DataFrame,
               possession: pd.DataFrame, playing_time: pd.DataFrame, misc: pd.DataFrame, season: str) -> pd.DataFrame:
    
    playing_time.drop(playing_time.loc[playing_time['Matches Played'] == '0'].index, inplace=True)
    playing_time['Rk']= playing_time.reset_index().index + 1

    df = pd.merge(standard, shooting, on='Rk', suffixes=('', '_remove')).merge(passing, on='Rk', suffixes=('', '_remove')).merge(pass_types, on='Rk', suffixes=('', '_remove')).merge(gsc, on='Rk', suffixes=('', '_remove')).merge(defense, on='Rk', suffixes=('', '_remove')).merge(possession, on='Rk', suffixes=('', '_remove')).merge(misc, on='Rk', suffixes=('', '_remove')).merge(playing_time, on='Rk', suffixes=('', '_remove'))

    df.drop([i for i in df.columns if 'remove' in i or i == 'Matches'],
               axis=1, inplace=True)

    if season == '2023-2024':
        df['Age'] = df['Age'].apply(lambda x: x.split('-')[0])
        
    for col in df.columns:
      if col in ['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Comp']:
        pass
      elif col in ['Age', 'Born', 'Matches Played', 'Starts', 'Minutes', 'Minutes per Match', 'Minutes per Start']:
        df[col] = df[col].apply(lambda x: x.replace(',', ''))
        df[col] = df[col].astype('int64')
      else:
        df[col] = df[col].apply(lambda x: x.replace(',', ''))
        df[col] = df[col].astype('float64')

    df['Turnover'] = (df['Attempted Passes Total'] - df['Completed Passes Total']) + df['Dispossessed'] + df['TakeOns Tackled'] + df['Miscontrols']
    df['Turnover%'] = round((df['Turnover'] / df['Touches']) * 100, 2)
    df['Turnover/90'] = round(df['Turnover'] / df['90s'], 2)
    df['Season'] = season
    return df

def get_big5_combined(season: str) -> pd.DataFrame:
    standard = get_standard_stats(f'https://fbref.com/en/comps/Big5/{season}/stats/players/{season}-Big-5-European-Leagues-Stats')
    shooting = get_shooting(f'https://fbref.com/en/comps/Big5/{season}/shooting/players/{season}-Big-5-European-Leagues-Stats')
    passing = get_passing(f'https://fbref.com/en/comps/Big5/{season}/passing/players/{season}-Big-5-European-Leagues-Stats')
    pass_types = get_pass_type(f'https://fbref.com/en/comps/Big5/{season}/passing_types/players/{season}-Big-5-European-Leagues-Stats')
    gsc = get_gsc(f'https://fbref.com/en/comps/Big5/{season}/gca/players/{season}-Big-5-European-Leagues-Stats')
    defense = get_defensive_action(f'https://fbref.com/en/comps/Big5/{season}/defense/players/{season}-Big-5-European-Leagues-Stats')
    possession = get_possession(f'https://fbref.com/en/comps/Big5/{season}/possession/players/{season}-Big-5-European-Leagues-Stats')
    playing_time = get_playing_time(f'https://fbref.com/en/comps/Big5/{season}/playingtime/players/{season}-Big-5-European-Leagues-Stats')
    misc = get_misc(f'https://fbref.com/en/comps/Big5/{season}/misc/players/{season}-Big-5-European-Leagues-Stats')

    playing_time.drop(playing_time.loc[playing_time['Matches Played'] == '0'].index, inplace=True)
    playing_time['Rk']= playing_time.reset_index().index + 1

    df = pd.merge(standard, shooting, on='Rk', suffixes=('', '_remove')).merge(passing, on='Rk', suffixes=('', '_remove')).merge(pass_types, on='Rk', suffixes=('', '_remove')).merge(gsc, on='Rk', suffixes=('', '_remove')).merge(defense, on='Rk', suffixes=('', '_remove')).merge(possession, on='Rk', suffixes=('', '_remove')).merge(misc, on='Rk', suffixes=('', '_remove')).merge(playing_time, on='Rk', suffixes=('', '_remove'))
    
    df.drop([i for i in df.columns if 'remove' in i or i == 'Matches'],
               axis=1, inplace=True)

    if season == '2023-2024':
        df['Age'] = df['Age'].apply(lambda x: x.split('-')[0])
        
    for col in df.columns:
      if col in ['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Comp']:
        pass
      elif col in ['Age', 'Born', 'Matches Played', 'Starts', 'Minutes', 'Minutes per Match', 'Minutes per Start']:
        df[col] = df[col].astype('int64')
      else:
        df[col] = df[col].astype('float64')

    df['Turnover'] = (df['Attempted Passes Total'] - df['Completed Passes Total']) + df['Dispossessed'] + df['TakeOns Tackled'] + df['Miscontrols']
    df['Turnover%'] = round((df['Turnover'] / df['Touches']) * 100, 2)
    df['Turnover/90'] = round(df['Turnover'] / df['90s'], 2)
    df['Season'] = season
    return df