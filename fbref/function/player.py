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

def get_stats(url: str, category: str, comp: str = None) -> pd.DataFrame:
    """ Get individul stats from given fbref url. 

    Parameters
    ----------
    url  : str
        URL to be scrapped
    category    : str
        Stats category to be scrapped. Possible values are standard, shooting, passing, passing_type,
        gca, defense, possession, playing_time and misc
    comp    : str
        The name of the competition, leave to default value if scrapping big 5 leagues 
    
    Returns
    -------
    Scrapped individual stats DataFrame for given category
    """

    cat_dict = {'standard': "stats_standard", 'shooting': "stats_shooting", 'passing': "stats_passing",
                'passing_type': "stats_passing_types", 'gca': "stats_gca", 'defense': "stats_defense",
                'possession': "stats_possession", 'playing_time': "stats_playing_time", 'misc': "stats_misc"}
    
    if category == 'standard':
        columns = ['Player', 'Nation','Position','Squad','Age','Born','Match Played','Starts','Minutes','90s',
                   'Goals','Assists','G+A','Non Penalty Goals','Penalty Goals','Penalty Attempted', 'Yellow Cards',
                   'Red Cards','xG','npxG','xAG','npxG+xAG','Progressive Carries','Progressive Passes', 
                   'Progressive Passes Received','Goals/90','Assists/90', 'G+A/90','Non Penalty Goals/90',
                   'Non Penalty G+A/90','xG/90','xAG/90','xG+xAG/90','npxG/90','npxG+xAG/90','Matches']
        
    elif category == 'shooting':
        columns = ['Player', 'Nation', 'Position', 'Squad', 'Age', 'Born', '90s', 'Goals', 'Shots', 
                   'Shots on Target', 'Shots on Target %', 'Shots/90', 'Shots on Target/90', 'Goals/Shot', 
                   'Goals/Shot on Target', 'Average Shot Distance', 'Free Kicks', 'Penalty Goals', 'Penalty Attempted', 
                   'xG', 'npxG', 'npxG/Shot', 'Goals - xG', 'Non Penalty Goals - npxG', 'Matches']
        
    elif category == 'passing':
        columns = ['Player', 'Nation', 'Position', 'Squad', 'Age', 'Born', '90s','Completed Passes Total', 
                   'Attempted Passes Total', 'Completed Passes Total%', 'Total Passing Distance', 
                   'Progressive Passing Distance', 'Completed Short Passes', 'Attempted Short Passes', 
                   'Completed Short Passes%', 'Completed Medium Passes', 'Attempted Medium Passes', 
                   'Completed Medium Passes%', 'Completed Long Passes', 'Attempted Long Passes', 'Completed Long Passes%', 
                   'Assists', 'xAG', 'xA', 'A-xAG', 'Key Passes', 'Passes Into Final 3rd', 'Passes Into Pen Area', 
                   'Crossing Into Pen Area', 'Progressive Passes', 'Matches']
        
    elif category == 'passing_type':
        columns = ['Player', 'Nation', 'Position', 'Squad', 'Age', 'Born', '90s', 'Attempted Passes Total', 
                   'Live Ball Passes', 'Dead Ball Passes', 'Free Kicks Passes', 'Through Balls', 'Switches', 
                   'Crosses', 'Throw Ins', 'Corner Kicks', 'Inswinging Corner', 'Outswinging Corner', 
                   'Straight Corner', 'Completed Passes Total', 'Passes Offside', 'Passes Blocked', 'Matches']
        
    elif category == 'gca':
        columns = ['Player', 'Nation', 'Position', 'Squad', 'Age', 'Born', '90s', 'SCA', 'SCA90', 'SCAPassLive', 
                   'SCAPassDead', 'SCATakeOns', 'SCAShot', 'SCAFouled', 'SCADefAct', 'GCA', 'GCA90', 'GCAPassLive', 
                   'GCAPassDead', 'GCATakeOns', 'GCAShot', 'GCAFouled', 'GCADefAct', 'Matches']
        
    elif category == 'defense':
        columns = ['Player', 'Nation', 'Position', 'Squad', 'Age', 'Born', '90s','Tackles', 'Tackles Won', 
                   'Def 3rd Tackles', 'Mid 3rd Tackles', 'Att 3rd Tackles', 'Dribblers Tackled', 'Dribbles Challenged', 
                   'Dribbles Challenged%', 'Challenges Lost', 'Blocks', 'Shots Blocked', 'Pass Blocked', 'Interceptions', 
                   'Interceptions+Tackles', 'Clearances', 'Errors', 'Matches']
        
    elif category == 'possession':
        columns = ['Player', 'Nation', 'Position', 'Squad', 'Age', 'Born', '90s', 'Touches', 'Def Pen Touches', 
                   'Def 3rd Touches', 'Mid 3rd Touches', 'Att 3rd Touches', 'Att Pen Touches', 'Live Touches', 
                   'TakeOns Attempted', 'Successful TakeOns', 'Successful TakeOns%', 'TakeOns Tackled', 
                   'TakeOns Tackled %', 'Carries', 'Total Carries Distance', 'Progressive Carries Distance', 
                   'Progressive Carries', 'Carries to Final Third', 'Carries to Pen Area', 'Miscontrols', 'Dispossessed', 
                   'Passes Received', 'Progressive Passes Received', 'Matches']
        
    elif category == 'playing_time':
        columns = ['Player', 'Nation', 'Position', 'Squad', 'Age', 'Born', 'Matches Played', 'Minutes', 
                   'Minutes per Match', 'Minutes%', '90s', 'Starts', 'Minutes per Start', 'Complete Match', 
                   'Subs', 'Minutes per Subs', 'Unused Subs', 'PPM', 'onG', 'onGA', 'G+/-', 'G+/-90', 'On-Off', 
                   'onxG', 'onxGA', 'xG+/-', 'xG+/-90', 'xGOn-Off', 'Matches']
        
    elif category == 'misc':
        columns = ['Player', 'Nation', 'Position', 'Squad', 'Age', 'Born', '90s', 'Yellow Cards', 'Red Cards', 
                   '2nd Yellow', 'Fouls', 'Fouled', 'Offsides', 'Crosses', 'Interceptions', 'Tackles Won', 'Pen Won', 
                   'Pen Conceded', 'Own Goals', 'Recoveries', 'Aerial Won', 'Aerial Lost', 'Aerial Won%', 'Matches']
    else:
        return None
    
    if comp:
        df = scraping(url, cat_dict[category], comp, columns)
        columns.insert(0, 'Rk')
        columns.insert(5, 'Comp')
        return df[columns]
    else:
        df = clean_df(pd.read_html(url)[0])
        columns.insert(0, 'Rk')
        columns.insert(5, 'Comp')
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

    df = cast_column(season=season, df=df, big5=False)
    return df

def get_big5_combined(season: str) -> pd.DataFrame:
    standard = get_stats(f'https://fbref.com/en/comps/Big5/{season}/stats/players/{season}-Big-5-European-Leagues-Stats', category='standard')
    shooting = get_stats(f'https://fbref.com/en/comps/Big5/{season}/shooting/players/{season}-Big-5-European-Leagues-Stats', category='shooting')
    passing = get_stats(f'https://fbref.com/en/comps/Big5/{season}/passing/players/{season}-Big-5-European-Leagues-Stats', category='passing')
    pass_types = get_stats(f'https://fbref.com/en/comps/Big5/{season}/passing_types/players/{season}-Big-5-European-Leagues-Stats', category='passing_type')
    gca = get_stats(f'https://fbref.com/en/comps/Big5/{season}/gca/players/{season}-Big-5-European-Leagues-Stats', category='gca')
    defense = get_stats(f'https://fbref.com/en/comps/Big5/{season}/defense/players/{season}-Big-5-European-Leagues-Stats', category='defense')
    possession = get_stats(f'https://fbref.com/en/comps/Big5/{season}/possession/players/{season}-Big-5-European-Leagues-Stats', category='possession')
    playing_time = get_stats(f'https://fbref.com/en/comps/Big5/{season}/playingtime/players/{season}-Big-5-European-Leagues-Stats', category='playing_time')
    misc = get_stats(f'https://fbref.com/en/comps/Big5/{season}/misc/players/{season}-Big-5-European-Leagues-Stats', category='misc')

    playing_time.drop(playing_time.loc[playing_time['Matches Played'] == '0'].index, inplace=True)
    playing_time['Rk']= playing_time.reset_index().index + 1

    df = pd.merge(standard, shooting, on='Rk', suffixes=('', '_remove')).merge(passing, on='Rk', suffixes=('', '_remove')).merge(pass_types, on='Rk', suffixes=('', '_remove')).merge(gca, on='Rk', suffixes=('', '_remove')).merge(defense, on='Rk', suffixes=('', '_remove')).merge(possession, on='Rk', suffixes=('', '_remove')).merge(misc, on='Rk', suffixes=('', '_remove')).merge(playing_time, on='Rk', suffixes=('', '_remove'))
    
    df.drop([i for i in df.columns if 'remove' in i or i == 'Matches'],
               axis=1, inplace=True)

    df = cast_column(season=season, df=df)

    return df

def cast_column(season: str, df: pd.DataFrame, big5: bool = True) -> pd.DataFrame:
    
    if season == '2023-2024':
            df['Age'] = df['Age'].apply(lambda x: x.split('-')[0])

    if big5:
        for col in df.columns:
            if col in ['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Comp']:
                pass
            elif col in ['Age', 'Born', 'Matches Played', 'Starts', 'Minutes', 'Minutes per Match', 'Minutes per Start']:
                df[col] = df[col].astype('int64')
            else:
                df[col] = df[col].astype('float64')
    else:
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

def get_per_90(df: pd.DataFrame) -> pd.DataFrame:
    """ Converting eligible columns into per 90 basis

    Parameters
    ----------
    df  : pd.DataFrame
        Source DataFrame to be converted
    
    Returns
    New DataFrame with eligible columns converted into per 90 basis  
    """
    
    # Making a deep copy so the function will not affect to original DataFrame
    df = df.copy(deep=True)

    for col in df.columns:
        # Excluding the following columns for conversion
        if col in ['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Comp', 'Age', 
                   'Born', 'Match Played', 'Starts', 'Minutes', 'Season']:
            pass
        # Excluding columns which already in per 90 basis
        elif '90' in col:
            pass
        # Converting the remaining columns with 2 points rounding
        else:
            df[col] = round(df[col] / df['90s'], 2)
    
    return df
