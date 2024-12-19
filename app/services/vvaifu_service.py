import pandas as pd
from typing import List, Dict
from app.core.session_manager import SessionManager
import asyncio

class VVaifuService:
    """Service for interacting with the VVaifu API to fetch NFT character data."""
    
    BASE_URL = "https://api.vvaifu.fun/api/solana/search"
    
    def __init__(self):
        self.session_manager = SessionManager()
    
    async def fetch_page(self, page: int, limit: int = 100) -> List[Dict]:
        """
        Fetch a single page of character data from the API.
        
        Args:
            page (int): Page number to fetch
            limit (int, optional): Number of items per page. Defaults to 100.
            
        Returns:
            List[Dict]: List of character data dictionaries
        """
        params = {
            "page": page,
            "limit": limit,
            "sort": "marketCap",
            "tags": "",
            "keywords": ""
        }
        
        session = await self.session_manager.get_session()
        async with session.get(self.BASE_URL, params=params) as response:
            data = await response.json()
            return data['characters']
    
    async def fetch_all_data(self, total_pages: int = 10) -> pd.DataFrame:
        """
        Fetch multiple pages concurrently and combine into a DataFrame.
        
        Args:
            total_pages (int, optional): Number of pages to fetch. Defaults to 10.
            
        Returns:
            pd.DataFrame: DataFrame containing all character data
        """
        tasks = [self.fetch_page(page) for page in range(1, total_pages + 1)]
        results = await asyncio.gather(*tasks)
        
        # Flatten the list of character lists
        all_characters = [char for page in results for char in page]
        
        return pd.DataFrame(all_characters)


# %%
