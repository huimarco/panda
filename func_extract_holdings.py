import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

def load_model():
    system_prompt = """
    You are a financial advisor given a string of text from brokerage statements. Please interpret it to identify individual positions in each account.
    If you cannot identify a specific attribute, fill it with 'NA'.

    Example input:
    '7 of 28\nINVESTMENT REPORT \nJuly 1 – July 31, 2015\u2009\u2002\u2002\nHoldings (continued)\u2002\nDescription\nQuantity\nPrice \nPer Unit\nEnding \nMarket Value\nTotal \nCost Basis\nUnrealized \nGain/Loss\nEst. Annual \nIncome (EAI)\nEst. Yield \n(EY)\n25.00\n525.31\n$13,132.75 \n$9,350.12 \nc\n$3,782.63 \n$304.68 \n2.32%\nCommon Stocks \nAPPLE INC (AAPL) \nAMERCO COM (UHAL)\n30.00\n203.15A\n 6,094.50 \n 4,149.75 \nc\n 1,944.75 \n—\nTotal Common Stock (24% of account holdings)\n $5,517.25 \n$-1,011.12 \n$6,528.37 \n$304.68 \nAccount 111-111111 \nJohn W. Doe - Individual TOD\n*** SAMPLE STATEMENT ***\nFor informational purposes only\n$304.68 \n'

    Example output (follow the format exactly and do not collect extra metrics):
    {
        "statement_date":2015-07-31,
        "accounts":[
            {
                "account_number":"111-111111",
                "holdings": [
                    {
                    "description": "APPLE INC",
                    "symbol": "AAPL",
                    "quantity": 25.00,
                    "market_value": 13132.75,
                    "total_cost_basis": 9350.12
                    },
                    {
                    "description": "AMERCO COM",
                    "symbol": "UHAL",
                    "quantity": 30.00,
                    "market_value": 6094.50,
                    "total_cost_basis": 4149.75
                    }
                ]
            }
        ]
    }
    """

    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=api_key)

    # see https://ai.google.dev/api/python/google/generativeai/GenerativeModel
    generation_config = {
    'response_mime_type': 'application/json',
    }

    model = genai.GenerativeModel(
    model_name='gemini-1.5-pro', #"gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=system_prompt
    )

    return model

def extract_holdings(model, text):
    response = model.generate_content(text)
    return json.loads(response.text)