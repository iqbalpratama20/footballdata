import pandas as pd

LEAGUES = {'Eredivisie': ['23', 'Eredivisie'],
           'Primeira Liga': ['32', 'Primerira-Liga'],
           'MLS': ['22', 'Major-League-Soccer'], 
           'Championship': ['10', 'Championship'],
           'Brasil': ['24', 'Serie-A'],
           'Liga MX': ['31', 'Liga-MX'],
           'Primera Division': ['21', 'Primera-Division'],
           'Belgian Pro Leage': ['37', 'Belgian-Pro-League'],
           'Segunda': ['17', 'Segunda-Division'],
           'Serie B': ['18', 'Serie-B'],
           'Bundesliga 2': ['33', '2-Bundesliga'],
           'Ligue 2': ['60', 'Ligue-2'],
           'Big 5': ['Big5', 'Big-5-European-League']}

def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    
    df = df.droplevel(level=0, axis=1)
    return df

def clean_big5_df(df: pd.DataFrame) -> pd.DataFrame:
    
    df = df.droplevel(level=0, axis=1)
    df.drop(['Rk', 'Comp'], axis=1, inplace=True)
    return df

def get_for_stats(league: str, season: str, category: str = None) -> pd.DataFrame:
    
    if league == 'Big 5':
        standard = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/stats/squads/{season}-{LEAGUES[league][1]}-Stats')[0]
        shooting = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/shooting/squads/{season}-{LEAGUES[league][1]}-Stats')[0]
        passing = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/passing/squads/{season}-{LEAGUES[league][1]}-Stats')[0]
        pass_type = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/passing_types/squads/{season}-{LEAGUES[league][1]}-Stats')[0]
        gca = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/gca/squads/{season}-{LEAGUES[league][1]}-Stats')[0]
        defense = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/defense/squads/{season}-{LEAGUES[league][1]}-Stats')[0]
        possession = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/possession/squads/{season}-{LEAGUES[league][1]}-Stats')[0]
        playing_time = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/playingtime/squads/{season}-{LEAGUES[league][1]}-Stats')[0]
        misc = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/misc/squads/{season}-{LEAGUES[league][1]}-Stats')[0]

        standard, shooting, passing, pass_type, gca, defense, possession, playing_time, misc = (df.pipe(clean_big5_df) for df in [standard, shooting, passing, pass_type, 
                                                                                                                            gca, defense, possession, playing_time, misc])
        
        
    else:
        standard = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/stats/{season}-{LEAGUES[league][1]}-Stats')[0]
        shooting = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/shooting/{season}-{LEAGUES[league][1]}-Stats')[0]
        passing = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/passing/{season}-{LEAGUES[league][1]}-Stats')[0]
        pass_type = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/passing_types/{season}-{LEAGUES[league][1]}-Stats')[0]
        gca = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/gca/{season}-{LEAGUES[league][1]}-Stats')[0]
        defense = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/defense/{season}-{LEAGUES[league][1]}-Stats')[0]
        possession = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/possession/{season}-{LEAGUES[league][1]}-Stats')[0]
        playing_time = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/playingtime/{season}-{LEAGUES[league][1]}-Stats')[0]
        misc = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/misc/{season}-{LEAGUES[league][1]}-Stats')[0]

        standard, shooting, passing, pass_type, gca, defense, possession, playing_time, misc = (df.pipe(clean_df) for df in [standard, shooting, passing, pass_type, 
                                                                                                                            gca, defense, possession, playing_time, misc])
        
    columns = ['Squad', '# Player', 'Age', 'Possession', 'Matches Played', 'Starts', 'Minutes', '90s', 'Goals',
               'Assists', 'G+A', 'Non Penalty Goals', 'Penalty Goals', 'Penalty Attempted', 'Yellow Cards',
               'Red Cards', 'xG', 'npxG', 'xAG', 'npxG+xAG', 'Progressive Carries', 'Progressive Passes', 
               'Goals/90', 'Assists/90', 'G+A/90', 'Non Penalty Goals/90', 'Non Penalty G+A/90', 'xG/90',
               'xAG/90', 'xG+xAG/90', 'npxG/90', 'npxG+xAG/90']
    standard.columns = columns

    columns = ['Squad', '# Player', '90s', 'Goals', 'Shots', 'Shots on Target', 'Shots on Target %', 'Shots/90',
               'Shots on Target/90', 'Goals/Shot', 'Goals/Shot on Target', 'Average Shot Distance', 'Free Kicks',
               'Penalty Goals', 'Penalty Attempted', 'xG', 'npxG', 'npxG/Shot', 'Goals - xG', 'Non Penalty Goals - npxG']               
    shooting.columns = columns

    columns = ['Squad', '# Player', '90s', 'Completed Passes Total', 'Attempted Passes Total', 'Completed Passes Total%', 
               'Total Passing Distance', 'Progressive Passing Distance', 'Completed Short Passes', 'Attempted Short Passes', 
               'Completed Short Passes%', 'Completed Medium Passes', 'Attempted Medium Passes', 'Completed Medium Passes%', 
               'Completed Long Passes', 'Attempted Long Passes', 'Completed Long Passes%', 'Assists', 'xAG', 'xA', 'A-xAG', 
               'Key Passes', 'Passes Into Final 3rd', 'Passes Into Pen Area', 'Crossing Into Pen Area', 'Progressive Passes']
    passing.columns = columns

    columns = ['Squad', '# Player', '90s', 'Attempted Passes Total', 'Live Ball Passes', 'Dead Ball Passes', 'Free Kicks Passes',
               'Through Balls', 'Switches', 'Crosses', 'Throw Ins', 'Corner Kicks', 'Inswinging Corner', 'Outswinging Corner',
               'Straight Corner', 'Completed Passes Total', 'Passes Offside', 'Passes Blocked']
    pass_type.columns = columns

    columns = ['Squad', '# Player', '90s', 'SCA', 'SCA90', 'SCAPassLive', 'SCAPassDead', 'SCATakeOns',
               'SCAShot', 'SCAFouled', 'SCADefAct', 'GCA', 'GCA90', 'GCAPassLive', 'GCAPassDead', 
               'GCATakeOns', 'GCAShot', 'GCAFouled', 'GCADefAct']
    gca.columns = columns

    columns = ['Squad', '# Player', '90s', 'Tackles', 'Tackles Won', 'Def 3rd Tackles', 'Mid 3rd Tackles',
               'Att 3rd Tackles', 'Dribblers Tackled', 'Dribbles Challenged', 'Dribbles Challenged%', 
               'Challenges Lost', 'Blocks', 'Shots Blocked', 'Pass Blocked', 'Interceptions', 'Interceptions+Tackles', 
               'Clearances', 'Errors']
    defense.columns = columns

    columns = ['Squad', '# Player', 'Possession', '90s', 'Touches', 'Def Pen Touches', 'Def 3rd Touches', 'Mid 3rd Touches',
               'Att 3rd Touches', 'Att Pen Touches', 'Live Touches', 'TakeOns Attempted', 'Successful TakeOns', 
               'Successful TakeOns%', 'TakeOns Tackled', 'TakeOns Tackled %', 'Carries', 'Total Carries Distance', 
               'Progressive Carries Distance', 'Progressive Carries', 'Carries to Final Third', 'Carries to Pen Area', 
               'Miscontrols', 'Dispossessed', 'Passes Received', 'Progressive Passes Received']
    possession.columns = columns

    columns = ['Squad', '# Player', 'Age', 'Matches Played', 'Minutes', 'Minutes per Match', 'Minutes%', '90s',
               'Starts', 'Minutes per Start', 'Complete Match', 'Subs', 'Minutes per Subs', 'Unused Subs', 'PPM', 
               'onG', 'onGA', 'Plus-Minus', 'Plus-Minus/90', 'onxG', 'onxGA', 'xG+/-', 'xG+/-90']
    playing_time.columns = columns

    columns = ['Squad', '# Player', '90s', 'Yellow Cards', 'Red Cards', '2nd Yellow', 'Fouls', 'Fouled',
               'Offsides', 'Crosses', 'Interceptions', 'Tackles Won', 'Pen Won', 'Pen Conceded', 'Own Goals', 
               'Recoveries', 'Aerial Won', 'Aerial Lost', 'Aerial Won%']
    misc.columns = columns

    if category == 'standard':
        return standard
    elif category == 'shooting':
        return shooting
    elif category == 'passing':
        return passing
    elif category == 'pass_type':
        return pass_type
    elif category == 'gca':
        return gca
    elif category == 'defense':
        return defense
    elif category == 'possession':
        return possession
    elif category == 'playing_time':
        return playing_time
    elif category == 'misc':
        return misc
    
    df = pd.merge(standard, shooting, on='Squad', suffixes=('', '_remove')) \
        .merge(passing, on='Squad', suffixes=('', '_remove')) \
        .merge(pass_type, on='Squad', suffixes=('', '_remove')) \
        .merge(gca, on='Squad', suffixes=('', '_remove')) \
        .merge(defense, on='Squad', suffixes=('', '_remove')) \
        .merge(possession, on='Squad', suffixes=('', '_remove')) \
        .merge(misc, on='Squad', suffixes=('', '_remove')) \
        .merge(playing_time, on='Squad', suffixes=('', '_remove'))
    
    df.drop([i for i in df.columns if 'remove' in i],
               axis=1, inplace=True)
    df.drop(['# Player', 'Matches Played', 'Minutes', 'Starts'], axis=1, inplace=True)

    new_columns = ['Squad ' + col if col != 'Squad' else col for col in df.columns ]
    df.columns = new_columns
    
    return df

def get_opponent_stats(league: str, season: str, category: str = None) -> pd.DataFrame:

    if league == 'Big 5':
        standard = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/stats/squads/{season}-{LEAGUES[league][1]}-Stats')[1]
        shooting = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/shooting/squads/{season}-{LEAGUES[league][1]}-Stats')[1]
        passing = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/passing/squads/{season}-{LEAGUES[league][1]}-Stats')[1]
        pass_type = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/passing_types/squads/{season}-{LEAGUES[league][1]}-Stats')[1]
        gca = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/gca/squads/{season}-{LEAGUES[league][1]}-Stats')[1]
        defense = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/defense/squads/{season}-{LEAGUES[league][1]}-Stats')[1]
        possession = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/possession/squads/{season}-{LEAGUES[league][1]}-Stats')[1]
        playing_time = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/playingtime/squads/{season}-{LEAGUES[league][1]}-Stats')[1]
        misc = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/misc/squads/{season}-{LEAGUES[league][1]}-Stats')[1]

        standard, shooting, passing, pass_type, gca, defense, possession, playing_time, misc = (df.pipe(clean_big5_df) for df in [standard, shooting, passing, pass_type, 
                                                                                                                            gca, defense, possession, playing_time, misc])
    
    else:
        standard = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/stats/{season}-{LEAGUES[league][1]}-Stats')[1]
        shooting = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/shooting/{season}-{LEAGUES[league][1]}-Stats')[1]
        passing = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/passing/{season}-{LEAGUES[league][1]}-Stats')[1]
        pass_type = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/passing_types/{season}-{LEAGUES[league][1]}-Stats')[1]
        gca = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/gca/{season}-{LEAGUES[league][1]}-Stats')[1]
        defense = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/defense/{season}-{LEAGUES[league][1]}-Stats')[1]
        possession = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/possession/{season}-{LEAGUES[league][1]}-Stats')[1]
        playing_time = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/playingtime/{season}-{LEAGUES[league][1]}-Stats')[1]
        misc = pd.read_html(f'https://fbref.com/en/comps/{LEAGUES[league][0]}/{season}/misc/{season}-{LEAGUES[league][1]}-Stats')[1]

        standard, shooting, passing, pass_type, gca, defense, possession, playing_time, misc = (df.pipe(clean_df) for df in [standard, shooting, passing, pass_type, 
                                                                                                                            gca, defense, possession, playing_time, misc])
        
    columns = ['Squad', '# Player', 'Age', 'Possession', 'Matches Played', 'Starts', 'Minutes', '90s', 'Goals',
               'Assists', 'G+A', 'Non Penalty Goals', 'Penalty Goals', 'Penalty Attempted', 'Yellow Cards',
               'Red Cards', 'xG', 'npxG', 'xAG', 'npxG+xAG', 'Progressive Carries', 'Progressive Passes', 
               'Goals/90', 'Assists/90', 'G+A/90', 'Non Penalty Goals/90', 'Non Penalty G+A/90', 'xG/90',
               'xAG/90', 'xG+xAG/90', 'npxG/90', 'npxG+xAG/90']
    standard.columns = columns

    columns = ['Squad', '# Player', '90s', 'Goals', 'Shots', 'Shots on Target', 'Shots on Target %', 'Shots/90',
               'Shots on Target/90', 'Goals/Shot', 'Goals/Shot on Target', 'Average Shot Distance', 'Free Kicks',
               'Penalty Goals', 'Penalty Attempted', 'xG', 'npxG', 'npxG/Shot', 'Goals - xG', 'Non Penalty Goals - npxG']               
    shooting.columns = columns

    columns = ['Squad', '# Player', '90s', 'Completed Passes Total', 'Attempted Passes Total', 'Completed Passes Total%', 
               'Total Passing Distance', 'Progressive Passing Distance', 'Completed Short Passes', 'Attempted Short Passes', 
               'Completed Short Passes%', 'Completed Medium Passes', 'Attempted Medium Passes', 'Completed Medium Passes%', 
               'Completed Long Passes', 'Attempted Long Passes', 'Completed Long Passes%', 'Assists', 'xAG', 'xA', 'A-xAG', 
               'Key Passes', 'Passes Into Final 3rd', 'Passes Into Pen Area', 'Crossing Into Pen Area', 'Progressive Passes']
    passing.columns = columns

    columns = ['Squad', '# Player', '90s', 'Attempted Passes Total', 'Live Ball Passes', 'Dead Ball Passes', 'Free Kicks Passes',
               'Through Balls', 'Switches', 'Crosses', 'Throw Ins', 'Corner Kicks', 'Inswinging Corner', 'Outswinging Corner',
               'Straight Corner', 'Completed Passes Total', 'Passes Offside', 'Passes Blocked']
    pass_type.columns = columns

    columns = ['Squad', '# Player', '90s', 'SCA', 'SCA90', 'SCAPassLive', 'SCAPassDead', 'SCATakeOns',
               'SCAShot', 'SCAFouled', 'SCADefAct', 'GCA', 'GCA90', 'GCAPassLive', 'GCAPassDead', 
               'GCATakeOns', 'GCAShot', 'GCAFouled', 'GCADefAct']
    gca.columns = columns

    columns = ['Squad', '# Player', '90s', 'Tackles', 'Tackles Won', 'Def 3rd Tackles', 'Mid 3rd Tackles',
               'Att 3rd Tackles', 'Dribblers Tackled', 'Dribbles Challenged', 'Dribbles Challenged%', 
               'Challenges Lost', 'Blocks', 'Shots Blocked', 'Pass Blocked', 'Interceptions', 'Interceptions+Tackles', 
               'Clearances', 'Errors']
    defense.columns = columns

    columns = ['Squad', '# Player', 'Possession', '90s', 'Touches', 'Def Pen Touches', 'Def 3rd Touches', 'Mid 3rd Touches',
               'Att 3rd Touches', 'Att Pen Touches', 'Live Touches', 'TakeOns Attempted', 'Successful TakeOns', 
               'Successful TakeOns%', 'TakeOns Tackled', 'TakeOns Tackled %', 'Carries', 'Total Carries Distance', 
               'Progressive Carries Distance', 'Progressive Carries', 'Carries to Final Third', 'Carries to Pen Area', 
               'Miscontrols', 'Dispossessed', 'Passes Received', 'Progressive Passes Received']
    possession.columns = columns

    columns = ['Squad', '# Player', 'Age', 'Matches Played', 'Minutes', 'Minutes per Match', 'Minutes%', '90s',
               'Starts', 'Minutes per Start', 'Complete Match', 'Subs', 'Minutes per Subs', 'Unused Subs', 'PPM', 
               'onG', 'onGA', 'Plus-Minus', 'Plus-Minus/90', 'onxG', 'onxGA', 'xG+/-', 'xG+/-90']
    playing_time.columns = columns

    columns = ['Squad', '# Player', '90s', 'Yellow Cards', 'Red Cards', '2nd Yellow', 'Fouls', 'Fouled',
               'Offsides', 'Crosses', 'Interceptions', 'Tackles Won', 'Pen Won', 'Pen Conceded', 'Own Goals', 
               'Recoveries', 'Aerial Won', 'Aerial Lost', 'Aerial Won%']
    misc.columns = columns

    if category == 'standard':
        return standard
    elif category == 'shooting':
        return shooting
    elif category == 'passing':
        return passing
    elif category == 'pass_type':
        return pass_type
    elif category == 'gca':
        return gca
    elif category == 'defense':
        return defense
    elif category == 'possession':
        return possession
    elif category == 'playing_time':
        return playing_time
    elif category == 'misc':
        return misc
    
    df = pd.merge(standard, shooting, on='Squad', suffixes=('', '_remove')) \
        .merge(passing, on='Squad', suffixes=('', '_remove')) \
        .merge(pass_type, on='Squad', suffixes=('', '_remove')) \
        .merge(gca, on='Squad', suffixes=('', '_remove')) \
        .merge(defense, on='Squad', suffixes=('', '_remove')) \
        .merge(possession, on='Squad', suffixes=('', '_remove')) \
        .merge(misc, on='Squad', suffixes=('', '_remove')) \
        .merge(playing_time, on='Squad', suffixes=('', '_remove'))
    
    df['Squad'] = df['Squad'].apply(lambda x: ' '.join(x.split(' ')[1:]))

    df.drop([i for i in df.columns if 'remove' in i],
               axis=1, inplace=True)
    df.drop(['# Player', 'Matches Played', 'Minutes', 'Starts'], axis=1, inplace=True)

    new_columns = ['Opponent ' + col if col != 'Squad' else col for col in df.columns]
    df.columns = new_columns
    
    return df