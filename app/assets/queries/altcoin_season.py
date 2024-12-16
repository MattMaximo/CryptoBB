altcoin_season_query = """
    WITH latest_date AS (
        SELECT MAX(date) AS max_date 
        FROM COMMON.DAILY_MARKET_DATA
    ),
    first_date_data AS (
        SELECT
            coingecko_id,
            MIN(date) AS first_date
        FROM COMMON.DAILY_MARKET_DATA
        GROUP BY coingecko_id
    ),
    top_50_tokens AS (
        SELECT DISTINCT
            coingecko_id
        FROM COMMON.DAILY_MARKET_DATA d
        JOIN latest_date l ON 1=1
        WHERE d.date > '2017-01-01'
        QUALIFY RANK() OVER (
            PARTITION BY d.date 
            ORDER BY d.market_cap DESC
        ) <= 50
    ),
    base_data AS (
        SELECT
            d.date,
            d.coingecko_id,
            d.price,
            RANK() OVER (
                PARTITION BY d.date 
                ORDER BY d.market_cap DESC
            ) AS daily_rank,
            f.first_date
        FROM COMMON.DAILY_MARKET_DATA d
        JOIN latest_date l ON 1=1
        JOIN first_date_data f ON d.coingecko_id = f.coingecko_id
        JOIN top_50_tokens t ON d.coingecko_id = t.coingecko_id
        WHERE d.date > '2017-01-01'
        AND DATEDIFF(day, f.first_date, l.max_date) >= 90
        AND d.coingecko_id NOT IN (
            'tether', 'staked-ether', 'wrapped-bitcoin', 'weth', 'wrapped-eeth', 'dai',
            'binance-peg-weth', 'coinbase-wrapped-btc', 'rocket-pool-eth', 'first-digital-usd', 'usd-coin',
            'compound-0x', 'compound-basic-attention-token', 'compound-chainlink-token',
            'compound-ether', 'compound-maker', 'compound-meta', 'compound-sushi',
            'compound-uniswap', 'compound-usd-coin', 'compound-wrapped-btc',
            'compound-yearn-finance', 'aave-aave', 'aave-bal', 'aave-bat', 'aave-bat-v1',
            'aave-busd', 'aave-busd-v1', 'aave-crv', 'aave-dai', 'aave-dai-v1', 'aave-enj',
            'aave-enj-v1', 'aave-eth-v1', 'aave-gusd', 'aave-interest-bearing-steth',
            'aave-knc', 'aave-knc-v1', 'aave-link', 'aave-link-v1', 'aave-mana',
            'aave-mana-v1', 'aave-mkr', 'aave-mkr-v1', 'aave-polygon-aave',
            'aave-polygon-dai', 'aave-polygon-usdc', 'aave-polygon-usdt',
            'aave-polygon-wbtc', 'aave-polygon-weth', 'aave-polygon-wmatic', 'aave-rai',
            'aave-ren', 'aave-ren-v1', 'aave-snx', 'aave-snx-v1', 'aave-stkgho',
            'aave-susd', 'aave-susd-v1', 'aave-tusd', 'aave-tusd-v1', 'aave-uni',
            'aave-usdc', 'aave-usdc-v1', 'aave-usdt', 'aave-usdt-v1', 'aave-v3-1inch',
            'aave-v3-aave', 'aave-v3-ageur', 'aave-v3-arb', 'aave-v3-bal', 'aave-v3-btc-b',
            'aave-v3-cbeth', 'aave-v3-crv', 'aave-v3-dai', 'aave-v3-dpi', 'aave-v3-ens',
            'aave-v3-eure', 'aave-v3-eurs', 'aave-v3-frax', 'aave-v3-ghst', 'aave-v3-gno',
            'aave-v3-knc', 'aave-v3-ldo', 'aave-v3-link', 'aave-v3-lusd', 'aave-v3-mai',
            'aave-v3-maticx', 'aave-v3-metis', 'aave-v3-mkr', 'aave-v3-op', 'aave-v3-reth',
            'aave-v3-rpl', 'aave-v3-savax', 'aave-v3-sdai', 'aave-v3-snx', 'aave-v3-stg',
            'aave-v3-stmatic', 'aave-v3-susd', 'aave-v3-sushi', 'aave-v3-uni',
            'aave-v3-usdbc', 'aave-v3-usdc', 'aave-v3-usdc-e', 'aave-v3-usdt',
            'aave-v3-wavax', 'aave-v3-wbtc', 'aave-v3-weth', 'aave-v3-wmatic',
            'aave-v3-wsteth', 'aave-wbtc', 'aave-wbtc-v1', 'aave-weth', 'aave-xsushi',
            'aave-yfi', 'aave-yvault', 'aave-zrx', 'aave-zrx-v1', 'wrapped-steth', 'ethena-usde'
        )
    ),
    returns_data AS (
        SELECT 
            b.*,
            h.price AS price_90d_ago,
            (b.price / NULLIF(h.price, 0) - 1) * 100 AS returns_90d
        FROM base_data b
        LEFT JOIN COMMON.DAILY_MARKET_DATA h 
            ON h.coingecko_id = b.coingecko_id 
            AND h.date = DATEADD(day, -90, b.date)
        WHERE b.daily_rank <= 50
    )
    SELECT 
        r.date,
        AVG(CASE WHEN r.returns_90d > btc.returns_90d THEN 100.0 ELSE 0 END) AS alt_season
    FROM returns_data r
    JOIN returns_data btc 
        ON btc.date = r.date 
        AND btc.daily_rank = 1
    GROUP BY r.date
    ORDER BY r.date DESC;
    """
