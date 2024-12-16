def get_category_market_cap_query(coin_ids):
    '''
    Convert list of coin ids to a string of comma separated values for the query to search for in the database
    
    Returns Date and the sum of a Category's Market Cap
    '''
    ids_string = ", ".join(f"'{id}'" for id in coin_ids)
    
    return f"""
    SELECT
        DATE,
        SUM(MARKET_CAP) AS MARKET_CAP
    FROM ART_SHARE.COMMON.DAILY_MARKET_DATA
    WHERE COINGECKO_ID IN ({ids_string})
    GROUP BY DATE
    ORDER BY MARKET_CAP;
    """