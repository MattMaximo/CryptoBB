import snowflake.connector
import pandas as pd
from app.core.settings import Settings
import asyncio

settings = Settings()

class ArtemisService:
    def __init__(self):
        self.user = settings.SNOWFLAKE_USER
        self.password = settings.SNOWFLAKE_PASSWORD
        self.account = settings.SNOWFLAKE_ACCOUNT
        self.warehouse = settings.SNOWFLAKE_WAREHOUSE
        self.database = settings.SNOWFLAKE_DATABASE
        self.role = settings.SNOWFLAKE_ROLE
        self.api_key = settings.ARTEMIS_API_KEY

        
    def get_connection(self):
        return snowflake.connector.connect(
            user=self.user,
            password=self.password,
            account=self.account,
            warehouse=self.warehouse,
            database=self.database,
            role=self.role
        )

    async def execute_query(self, query: str) -> pd.DataFrame:
        """Execute a Snowflake query asynchronously"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute_async(query)
            query_id = cursor.sfqid
            
            while conn.get_query_status(query_id) == 'running':
                await asyncio.sleep(1)
            
            cursor.get_results_from_sfqid(query_id)
            result_set = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            
            return pd.DataFrame(result_set, columns=column_names)
            
        finally:
            cursor.close()
            conn.close()
