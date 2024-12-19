import pandas as pd
from typing import Dict, Any
from app.core.session_manager import SessionManager

class VirtualsService:
    BASE_URL = "https://api.virtuals.io/api"
    
    def __init__(self):
        self.session_manager = SessionManager()
    
    async def get_agents_list(self) -> pd.DataFrame:
        """
        Fetch virtuals agents data asynchronously
        """
        url = f"{self.BASE_URL}/virtuals"
        params = {
            "filters[status][$in][0]": "AVAILABLE",
            "filters[status][$in][1]": "ACTIVATING",
            "filters[priority][$ne]": -1,
            "sort[0]": "totalValueLocked:desc",
            "sort[1]": "createdAt:desc",
            "populate[0]": "image",
            "pagination[page]": 1,
            "pagination[pageSize]": 200
        }
        
        session = await self.session_manager.get_session()
        async with session.get(url, params=params) as response:
            data = await response.json()
                
        df = pd.DataFrame(data['data'])
        df = df.fillna("")  # Fill NaN values before converting to dict
        
        return df