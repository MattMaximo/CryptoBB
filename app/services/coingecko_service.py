from typing import Dict
import pandas as pd
import requests
from app.core.settings import get_settings

settings = get_settings()

class CoinGeckoService: 
    def __init__(self):
        self.api_key = settings.COINGECKO_API_KEY
        self.headers = {"accept": "application/json", "x-cg-pro-api-key": self.api_key}

    def fetch_data(self, url: str) -> Dict:
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def get_coin_details(self, coin_id: str) -> Dict:
        url = f"https://pro-api.coingecko.com/api/v3/coins/{coin_id}"
        return self.fetch_data(url)
    
    def get_coin_list(self, include_platform: str = "true", status: str = "active") -> pd.DataFrame:
        """Fetches active coins list from CoinGecko API."""
        url = f"https://pro-api.coingecko.com/api/v3/coins/list?include_platform={include_platform}&status={status}"
        data = self.fetch_data(url)

        if include_platform:
            # Convert list of dictionaries to DataFrame from the list of chains the token is on
            df = pd.DataFrame(data)
            df["platforms"] = df["platforms"].apply(
                lambda d: ", ".join(d.keys()) if isinstance(d, dict) else ""
            )

        return df

    def get_total_marketcap(self) -> pd.DataFrame:
        url = "https://pro-api.coingecko.com/api/v3/global/market_cap_chart?days=max"
        data = self.fetch_data(url).get("market_cap_chart", {})

        market_cap_data = pd.DataFrame(
            data["market_cap"], columns=["date", "total_market_cap"]
        )
        market_cap_data["date"] = pd.to_datetime(market_cap_data["date"], unit="ms")

        return market_cap_data

    def get_market_data(self, coin_id: str) -> pd.DataFrame:
        url = f"https://pro-api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=max&interval=daily"
        data = self.fetch_data(url)

        prices = pd.DataFrame(data["prices"], columns=["date", f"{coin_id}_price"])
        market_cap = pd.DataFrame(
            data["market_caps"], columns=["date", f"{coin_id}_market_cap"]
        )
        volume = pd.DataFrame(
            data["total_volumes"], columns=["date", f"{coin_id}_volume"]
        )

        df = prices.merge(market_cap, on="date").merge(volume, on="date")
        df["date"] = pd.to_datetime(df["date"], unit="ms")
        df = df[df["date"].dt.time == pd.to_datetime("00:00:00").time()]

        return df

    def get_dominance(self, coin_id: str) -> pd.DataFrame:
        total_market_cap = self.get_total_marketcap()
        coin_data = self.get_market_data(coin_id)
        coin_data = coin_data[["date", f"{coin_id}_market_cap"]]

        dominance_data = total_market_cap.merge(coin_data, on="date", how="inner")
        dominance_data["dominance"] = (
            dominance_data[f"{coin_id}_market_cap"]
            / dominance_data["total_market_cap"]
        )
        return dominance_data[["date", "dominance"]]

    def get_vm_ratio(self, coin_id: str) -> pd.DataFrame:
        market_data = self.get_market_data(coin_id)
        market_data["vm_ratio"] = market_data[f"{coin_id}_volume"] / market_data[f"{coin_id}_market_cap"]
        return market_data[["date", "vm_ratio"]]

    def get_correlation(self, coin_id1: str, coin_id2: str, days: int = 30) -> pd.DataFrame:
        # Fetch market data for each coin
        market_data1 = self.get_market_data(coin_id1)
        market_data2 = self.get_market_data(coin_id2)

        # Select date and price columns
        market_data1 = market_data1[["date", f"{coin_id1}_price"]]
        market_data2 = market_data2[["date", f"{coin_id2}_price"]]

        # Merge data on date
        merged_data = market_data1.merge(market_data2, on="date", how="inner")

        # Calculate rolling correlation
        merged_data["correlation"] = merged_data[f"{coin_id1}_price"].rolling(window=days).corr(merged_data[f"{coin_id2}_price"])

        # Return only date and correlation columns
        return merged_data[["date", "correlation"]]