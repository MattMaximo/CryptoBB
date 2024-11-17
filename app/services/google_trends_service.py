# %%

from pytrends.request import TrendReq
import pandas as pd

class GoogleTrendsService:
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)

    def get_historical_search_trends(self, keywords) -> pd.DataFrame:
        """
        Fetch historical Google search trends for one or more keywords.

        Args:
            keywords (str or list): A single keyword as a string or a list of keywords.

        Returns:
            pd.DataFrame: DataFrame with 'date' as index and columns for each keyword's trend data.
        """
        # Ensure keywords is a list
        if isinstance(keywords, str):
            keywords = [keywords]

        # Build the payload for the search terms
        self.pytrends.build_payload(keywords, cat=0, timeframe='today 5-y', geo='', gprop='')

        # Get historical interest data
        trend_data = self.pytrends.interest_over_time()

        # Drop the 'isPartial' column if it exists
        if 'isPartial' in trend_data.columns:
            trend_data = trend_data.drop(columns=['isPartial'])

        # Reset index to make 'date' a column
        trend_data.reset_index(inplace=True)

        return trend_data

    def get_current_region_search_trends(self, keywords) -> pd.DataFrame:
        """
        Fetch current search trends by region for the specified keywords.

        Args:
            keywords (str or list): A single keyword as a string or a list of keywords.

        Returns:
            pd.DataFrame: DataFrame with search trends by region.
        """
        self.pytrends.build_payload(kw_list=keywords)
        df = self.pytrends.interest_by_region()
        # Drop values where interest is 0
        df = df[df["value"] != 0]
        return df

# Example usage:
# google_trends_service = GoogleTrendsService()
# df_historical = google_trends_service.get_historical_search_trends(["Ethereum", "Bitcoin"])
# df_current = google_trends_service.get_current_region_search_trends("Ethereum")

# %%
