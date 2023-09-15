import pandas as pd

def custom_profile(df: pd.DataFrame, columns: list, position: str = None,
                   age_min: int = 16, age_max: int = 45, minutes: int = 0) -> pd.DataFrame:
    
    df = df.loc[(df['Pos'] == position) & (df['Age'] >= age_min) & (df['Age'] <= age_max) & (df['Minutes'] >= minutes)][columns].copy()
    for col in df.columns:
      if col in ['Player', 'Age', 'Pos', 'Squad']:
        pass
      elif col in ('Turnover%', 'onxGA'):
        df[col] = (df[col] * -1).rank(pct=True).round(2) * 100
      else:
        df[col] = df[col].rank(pct=True).round(2) * 100

    df['Rating'] = df.iloc[:, 4:-1].mean(axis=1).round()
    return df
