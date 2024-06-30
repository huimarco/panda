import pandas as pd 

def json_to_df(json):
    holdings = json['holdings']
    df = pd.DataFrame(holdings)
    return df