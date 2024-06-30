import pandas as pd 

def json_to_dfs(json_data):
    statement_date = json_data['statement_date']
    accounts = json_data['accounts']
    
    dataframes = {}
    
    for account in accounts:
        account_number = account['account_number']
        holdings = account['holdings']
        
        # Create a DataFrame for this account
        df = pd.DataFrame(holdings)
        df['statement_date'] = statement_date
        df['account_number'] = account_number
        
        # Store the DataFrame in the dictionary with the account number as the key
        dataframes[account_number] = df
    
    return dataframes