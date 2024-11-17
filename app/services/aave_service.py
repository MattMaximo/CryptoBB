# %%

from typing import Dict
import pandas as pd
import requests

class AaveService:
    def __init__(self):
        # Initialize any necessary attributes here
        pass


    def get_lending_pool_history(
        self,
        pool: str,
        start_date: int = 0,
        interval_hours: int = 24
    ) -> pd.DataFrame:
        url = f"https://aave-api-v2.aave.com/data/rates-history?reserveId={pool}&from={start_date}&resolutionInHours={interval_hours}"
        response = requests.get(url)
        print(url)
        data = response.json()
        
        df = pd.DataFrame(data)

        # Create datetime column with explicit format
        df['datetime'] = pd.to_datetime(
            df['x'].apply(lambda x: f"{x['year']}-{x['month']:02d}-{x['date']:02d} {x['hours']:02d}:00:00"), 
            format="%Y-%m-%d %H:%M:%S",  # Specifying format directly
            errors='coerce'
        )

        # Drop any rows where 'datetime' is NaT due to parsing issues
        df = df.dropna(subset=['datetime']).drop(columns='x')
        df.rename(columns={'datetime': 'date'}, inplace=True)

        return df



# %%