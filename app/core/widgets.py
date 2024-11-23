WIDGETS = {

    "crypto_dominance": {
        "name": "Crypto Market Dominance",
        "description": "Market dominance of major cryptocurrencies",
        "category": "crypto",
        #"subCategory": "crypto",
        "defaultViz": "chart",
        "endpoint": "dominance",
        "gridData": {"w": 20, "h": 9},
        "source": "CoinGecko",
        "params": [
            {
                "paramName": "coin_id",
                "value": "bitcoin",
                "label": "Coin",
                "type": "text",
                "description": "CoinGecko ID of the cryptocurrency",
            }
        ],
        "data": {"chart": {"type": "line"}},
    },
    "volume_marketcap_ratio": {
        "name": "Volume/Market Cap Ratio",
        "description": "Total Trading Volume / Total Market Cap",
        "category": "crypto",
        #"subCategory": "crypto",
        "defaultViz": "chart",
        "endpoint": "vm_ratio",
        "gridData": {"w": 20, "h": 9},
        "source": "CoinGecko",
        "params": [
            {
                "paramName": "coin_id",
                "value": "bitcoin",
                "label": "Coin",
                "type": "text",
                "description": "CoinGecko ID of the cryptocurrency",
            }
        ],
        "data": {"chart": {"type": "line"}},
    },
    "coingecko_coin_list": {
        "name": "Coingecko Coins List",
        "description": "List of all coins available on CoinGecko including ID, Name, Ticker, and available chains.",
        "category": "crypto",
        "endpoint": "coingecko_coin_list",
        "gridData": {"w": 20, "h": 9},
        "source": "CoinGecko",
        "data": {
            "table": {  
                "showAll": True,
                "columnsDefs": [
                    {
                        "headerName": "Name",
                        "field": "name",
                        "chartDataType": "category",
                    },
                    {
                        "headerName": "Ticker",
                        "field": "symbol",
                        "chartDataType": "category",
                    },
                    {
                        "headerName": "Chains",
                        "field": "platforms",
                        "chartDataType": "category",
                    },
                    {
                        "headerName": "ID",
                        "field": "id",
                        "chartDataType": "category",
                    },
                ],
            }
        },
    },
    
    "long_term_holders_net_change": {
        "name": "Long Term Holders Net Position Change",
        "description": "Net position change of long term holders",
        "category": "crypto",
        "defaultViz": "chart",
        "endpoint": "lth_net_change",
        "gridData": {"w": 20, "h": 9},
        "source": "Glassnode",
        "params": [
            {
                "paramName": "asset",
                "value": "btc",
                "label": "Coin",
                "type": "text",
                "description": "Glassnode ID of the cryptocurrency",
            },  
            {
                "paramName": "show_price",
                "value": "False",
                "label": "Show Price",
                "type": "text",
                "description": "Overlay price on chart",
                "options": [
                    {
                        "value": "True",
                        "label": "True"
                    },
                    {
                        "value": "False",
                        "label": "False"
                    },
        ]
      }
        ],
        "data": {"chart": {"type": "line"}},
    },

    "long_term_holders_supply": {
        "name": "Long Term Holders Supply",
        "description": "Supply of long term holders",
        "category": "crypto",
        "defaultViz": "chart",
        "endpoint": "lth_supply",
        "gridData": {"w": 20, "h": 9},
        "source": "Glassnode",
        "params": [
            {
                "paramName": "asset",
                "value": "btc",
                "label": "Coin",
                "type": "text",
                "description": "Glassnode ID of the cryptocurrency",
            },
            {
                "paramName": "show_price",
                "value": "False",
                "label": "Show Price",
                "type": "text",
                "description": "Overlay price on chart",
                "options": [
                    {
                        "value": "True",
                        "label": "True"
                    },
                    {
                        "value": "False",
                        "label": "False"
                    },
        ]
      }
        ],
        "data": {"chart": {"type": "line"}},
    },

    "google_trends": {
        "name": "Google Trends",
        "description": "Historical and current search trends for a given keyword",
        "category": "sentiment",
        #"subCategory": "crypto",
        "defaultViz": "chart",
        "endpoint": "historical_google_trends",
        "gridData": {"w": 20, "h": 9},
        "source": "Google",
        "params": [
            {
                "paramName": "search_term",
                "value": "coinbase",
                "label": "Search Term",
                "type": "text",
                "description": "Term you want to return Google trends for",
            }
        ],
        "data": {"chart": {"type": "line"}},
    },

    "token_correlation": {
        "name": "Token Correlation",
        "description": "Historical correlation between two search tokens",
        "category": "crypto",
        #"subCategory": "crypto",
        "defaultViz": "chart",
        "endpoint": "correlation",
        "gridData": {"w": 20, "h": 9},
        "source": "Google",
        "params": [
            {
                "paramName": "coin_id1",
                "value": "bitcoin",
                "label": "Coin 1",
                "type": "text",
                "description": "CoinGecko ID of the first cryptocurrency",
            },
            {
                "paramName": "coin_id2",
                "value": "ethereum",
                "label": "Coin 2",
                "type": "text",
                "description": "CoinGecko ID of the second cryptocurrency",
            }
        ],
        "data": {"chart": {"type": "line"}},
    },

 "velo_futures_products": {
        "name": "Velo Futures Products",
        "description": "List of all futures products available on Velo.",
        "category": "crypto",
        #"subCategory": "crypto",
        "endpoint": "velo_futures_products",
        "gridData": {"w": 20, "h": 9},
        "source": "VeloData",
        "data": {
            "table": {  
                "showAll": True,
                "columnsDefs": [
                    {
                        "headerName": "Exchange",
                        "field": "exchange",
                        "chartDataType": "category",
                    },
                    {
                        "headerName": "Ticker",
                        "field": "coin",
                        "chartDataType": "category",
                    },
                    {
                        "headerName": "Pair",
                        "field": "product",
                        "chartDataType": "category",
                    },
                    {
                        "headerName": "Start Date",
                        "field": "begin",
                        "chartDataType": "category",
                    },
                ],
            }
        },
    },

 "velo_spot_products": {
        "name": "Velo Spot Products",
        "description": "List of all spot products available on Velo.",
        "category": "crypto",
        #"subCategory": "crypto",
        "endpoint": "velo_spot_products",
        "gridData": {"w": 20, "h": 9},
        "source": "VeloData",
        "data": {
            "table": {  
                "showAll": True,
                "columnsDefs": [
                    {
                        "headerName": "Exchange",
                        "field": "exchange",
                        "chartDataType": "category",
                    },
                    {
                        "headerName": "Ticker",
                        "field": "coin",
                        "chartDataType": "category",
                    },
                    {
                        "headerName": "Pair",
                        "field": "product",
                        "chartDataType": "category",
                    },
                    {
                        "headerName": "Start Date",
                        "field": "begin",
                        "chartDataType": "category",
                    },
                ],
            }
        },
    },
 "velo_options_products": {
        "name": "Velo Options Products",
        "description": "List of all options products available on Velo.",
        "category": "crypto",
        #"subCategory": "crypto",
        "endpoint": "velo_options_products",
        "gridData": {"w": 20, "h": 9},
        "source": "VeloData",
        "data": {
            "table": {  
                "showAll": True,
                "columnsDefs": [
                    {
                        "headerName": "Exchange",
                        "field": "exchange",
                        "chartDataType": "category",
                    },
                    {
                        "headerName": "Ticker",
                        "field": "coin",
                        "chartDataType": "category",
                    },
                    {
                        "headerName": "Pair",
                        "field": "product",
                        "chartDataType": "category",
                    },
                    {
                        "headerName": "Start Date",
                        "field": "begin",
                        "chartDataType": "category",
                    },
                ],
            }
        },
    },
    "oi_weighted_funding_rates": {
        "name": "Open Interest Weighted Funding Rates",
        "description": "Historical Open Interest Weighted Funding Rates.",
        "category": "crypto",
        "defaultViz": "chart",
        "endpoint": "oi_weighted_funding_rates",
        "gridData": {"w": 20, "h": 9},
        "source": "VeloData",
        "params": [
            {
                "paramName": "coin",
                "value": "BTC",
                "label": "Coin",
                "type": "text",
                "description": "Coin to get funding rates for",
            },
            {
                "paramName": "resolution",
                "value": "1d",
                "label": "Resolution",
                "type": "text",
                "description": "Resolution of the data",
            },
            {
                "paramName": "begin",
                "value": "2024-01-01",
                "label": "Start Date",
                "type": "text",
                "description": "Start date of the data (YYYY-MM-DD). Leave blank for full history.",
            }
        ],
        "data": {"chart": {"type": "line"}},
    },
    
    "exchange_funding_rates": {
        "name": "Funding Rates by Exchange",
        "description": "Historical Funding Rates by Exchange.",
        "category": "crypto",
        "defaultViz": "chart",
        "endpoint": "exchange_funding_rates",
        "gridData": {"w": 20, "h": 9},
        "source": "VeloData",
        "params": [
            {
                "paramName": "coin",
                "value": "BTC",
                "label": "Coin",
                "type": "text",
                "description": "Coin to get funding rates for",
            },
            {
                "paramName": "resolution",
                "value": "1d",
                "label": "Resolution",
                "type": "text",
                "description": "Resolution of the data",
            },
            {
                "paramName": "begin",
                "value": "2024-01-01",
                "label": "Start Date",
                "type": "text",
                "description": "Start date of the data (YYYY-MM-DD). Leave blank for full history.",
            }
        ],
        "data": {"chart": {"type": "line"}},
    },
    "long_liquidations": {
        "name": "Long Liquidations",
        "description": "Historical Long Liquidations.",
        "category": "crypto",
        "defaultViz": "chart",
        "endpoint": "long_liquidations",
        "gridData": {"w": 20, "h": 9},
        "source": "VeloData",
        "params": [
            {
                "paramName": "coin",
                "value": "BTC",
                "label": "Coin",
                "type": "text",
                "description": "Coin to get funding rates for",
            },
            {
                "paramName": "resolution",
                "value": "1d",
                "label": "Resolution",
                "type": "text",
                "description": "Resolution of the data",
            },
            {
                "paramName": "begin",
                "value": "2024-01-01",
                "label": "Start Date",
                "type": "text",
                "description": "Start date of the data (YYYY-MM-DD). Leave blank for full history.",
            }
        ],
        "data": {"chart": {"type": "line"}},
    },
    "short_liquidations": {
        "name": "Short Liquidations",
        "description": "Historical Short Liquidations.",
        "category": "crypto",
        "defaultViz": "chart",
        "endpoint": "short_liquidations",
        "gridData": {"w": 20, "h": 9},
        "source": "VeloData",
        "params": [
            {
                "paramName": "coin",
                "value": "BTC",
                "label": "Coin",
                "type": "text",
                "description": "Coin to get funding rates for",
            },
            {
                "paramName": "resolution",
                "value": "1d",
                "label": "Resolution",
                "type": "text",
                "description": "Resolution of the data",
            },
            {
                "paramName": "begin",
                "value": "2024-01-01",
                "label": "Start Date",
                "type": "text",
                "description": "Start date of the data (YYYY-MM-DD). Leave blank for full history.",
            }
        ],
        "data": {"chart": {"type": "line"}},
    },
    "net_liquidations": {
        "name": "Net Liquidations",
        "description": "Historical Net Liquidations.",
        "category": "crypto",
        "defaultViz": "chart",
        "endpoint": "net_liquidations",
        "gridData": {"w": 20, "h": 9},
        "source": "VeloData",
        "params": [
            {
                "paramName": "coin",
                "value": "BTC",
                "label": "Coin",
                "type": "text",
                "description": "Coin to get funding rates for",
            },
            {
                "paramName": "resolution",
                "value": "1d",
                "label": "Resolution",
                "type": "text",
                "description": "Resolution of the data",
            },
            {
                "paramName": "begin",
                "value": "2024-01-01",
                "label": "Start Date",
                "type": "text",
                "description": "Start date of the data (YYYY-MM-DD). Leave blank for full history.",
            }
        ],
        "data": {"chart": {"type": "line"}},
    },
    "open_interest": {
        "name": "Open Interest",
        "description": "Historical Open Interest.",
        "category": "crypto",
        "defaultViz": "chart",
        "endpoint": "open_interest",
        "gridData": {"w": 20, "h": 9},
        "source": "VeloData",
        "params": [
            {
                "paramName": "coin",
                "value": "BTC",
                "label": "Coin",
                "type": "text",
                "description": "Coin to get funding rates for",
            },
            {
                "paramName": "resolution",
                "value": "1d",
                "label": "Resolution",
                "type": "text",
                "description": "Resolution of the data",
            },
            {
                "paramName": "begin",
                "value": "2024-01-01",
                "label": "Start Date",
                "type": "text",
                "description": "Start date of the data (YYYY-MM-DD). Leave blank for full history.",
            }
        ],
        "data": {"chart": {"type": "line"}},
    },

    "aave_lending_rate": {
        "name": "Aave Lending Rate",
        "description": "Historical Daily Aave Lending Rates. Default is USDC on Aave.",
        "category": "crypto",
        "defaultViz": "chart",
        "endpoint": "aave_lending_rate",
        "gridData": {"w": 20, "h": 9},
        "source": "Aave",
        "params": [
            {
                "paramName": "pool",
                "value": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb480x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e1",
                "label": "Pool",
                "type": "text",
                "description": "Aave Pool to get lending rates for",
            },

        ],
        "data": {"chart": {"type": "line"}},
    },


    "aave_borrow_rate": {
        "name": "Aave Borrow Rate",
        "description": "Historical Daily Aave Borrow Rates. Default is USDC on Aave.",
        "category": "crypto",
        "defaultViz": "chart",
        "endpoint": "aave_borrow_rate",
        "gridData": {"w": 20, "h": 9},
        "source": "Aave",
        "params": [
            {
                "paramName": "pool",
                "value": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb480x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e1",
                "label": "Pool",
                "type": "text",
                "description": "Aave Pool to get borrow rates for",
            },

        ],
        "data": {"chart": {"type": "line"}},
    },

    "aave_utilization_rate": {
        "name": "Aave Utilization Rate",
        "description": "Historical Daily Aave Utilization Rates. Default is USDC on Aave.",
        "category": "crypto",
        "defaultViz": "chart",
        "endpoint": "aave_utilization_rate",
        "gridData": {"w": 20, "h": 9},
        "source": "Aave",
        "params": [
            {
                "paramName": "pool",
                "value": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb480x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e1",
                "label": "Pool",
                "type": "text",
                "description": "Aave Pool to get utilization rates for",
            },
        ],
        "data": {"chart": {"type": "line"}},
    },      


 "aave_pools": {
        "name": "Aave Pools",
        "description": "List of all Aave Lending Pools.",
        "category": "crypto",
        #"subCategory": "crypto",
        "endpoint": "aave_pools",
        "gridData": {"w": 20, "h": 9},
        "source": "Aave",
        "data": {
            "table": {  
                "showAll": True,
                "columnsDefs": [
                    {
                        "headerName": "Pool Address",
                        "field": "pool_address",
                        "chartDataType": "category",
                    },
                    {
                        "headerName": "Pool Name",
                        "field": "pool_name",
                        "chartDataType": "category",
                    },
                    {
                        "headerName": "Chain",
                        "field": "chain",
                        "chartDataType": "category",
                    },
                    {
                        "headerName": "Version",
                        "field": "version",
                        "chartDataType": "category",
                    },
                    {
                        "headerName": "Link",
                        "field": "link",
                        "chartDataType": "category",
                    },
                ],
            }
        },
    },

    "coingecko_price": {
        "name": "Coingecko Price",
        "description": "Historical and current price for a given coin",
        "category": "crypto",
        #"subCategory": "crypto",
        "defaultViz": "chart",
        "endpoint": "coingecko_price",
        "gridData": {"w": 20, "h": 9},
        "source": "CoinGecko",
        "params": [
            {
                "paramName": "coin_id",
                "value": "bitcoin",
                "label": "Coin",
                "type": "text",
                "description": "CoinGecko ID of the cryptocurrency",
            }
        ],
        "data": {"chart": {"type": "line"}},
    },

    "coinbase_app_store_rank": {
        "name": "Coinbase App Store Rank",
        "description": "Historical and current rank of Coinbase in the App Store",
        "category": "sentiment",
        #"subCategory": "crypto",
        "defaultViz": "chart",
        "endpoint": "coinbase_app_store_rank",
        "gridData": {"w": 20, "h": 9},
        "source": "Telegram",
        "data": {"chart": {"type": "line"}},
    },

    "coinbase_wallet_app_store_rank": {
        "name": "Coinbase Wallet App Store Rank",
        "description": "Historical and current rank of Coinbase Wallet in the App Store",
        "category": "sentiment",
        #"subCategory": "crypto",
        "defaultViz": "chart",
        "endpoint": "coinbase_wallet_app_store_rank",
        "gridData": {"w": 20, "h": 9},
        "source": "Telegram",
        "data": {"chart": {"type": "line"}},
    },

    "phantom_wallet_app_store_rank": {
        "name": "Phantom Wallet App Store Rank",
        "description": "Historical and current rank of Phantom Wallet in the App Store",
        "category": "sentiment",
        #"subCategory": "crypto",
        "defaultViz": "chart",
        "endpoint": "phantom_wallet_app_store_rank",
        "gridData": {"w": 20, "h": 9},
        "source": "Telegram",
        "data": {"chart": {"type": "line"}},
    },


    "glassnode_price": {
        "name": "Glassnode Price",
        "description": "Historical and current price for a given coin",
        "category": "crypto",
        #"subCategory": "crypto",
        "defaultViz": "chart",
        "endpoint": "glassnode_price",
        "gridData": {"w": 20, "h": 9},
        "source": "Glassnode",
        "params": [
            {
                "paramName": "asset",
                "value": "btc",
                "label": "Coin",
                "type": "text",
                "description": "Glassnode ID of the cryptocurrency",
            }
        ],
        "data": {"chart": {"type": "line"}},
    },
    "microstrategy_premium": {
        "name": "Microstrategy Premium",
        "description": "Historical and current premium for Microstrategy",
        "category": "crypto",
        "defaultViz": "chart",
        "endpoint": "microstrategy_premium",
        "gridData": {"w": 20, "h": 9},
        "source": "MSTR Tracker",
        "data": {"chart": {"type": "line"}},
    },
    "microstrategy_info": {
        "name": "Microstrategy Info",
        "description": "Historical info for Microstrategy's Bitcoin holdings, including balance, cost basis, and share metrics",
        "category": "crypto",
        "defaultViz": "table",
        "endpoint": "microstrategy_info", 
        "gridData": {"w": 20, "h": 9},
        "source": "MSTR Tracker",
        "data": {
            "table": {
                "showAll": True,
                "columnsDefs": [
                    {
                        "headerName": "Date",
                        "field": "date",
                        "chartDataType": "category"
                    },
                    {
                        "headerName": "BTC Held",
                        "field": "btc_balance",
                        "chartDataType": "category"
                    },
                    {
                        "headerName": "Bal Change",
                        "field": "change", 
                        "chartDataType": "category"
                    },
                    {
                        "headerName": "BTC per Share",
                        "field": "btc_per_share",
                        "chartDataType": "category"
                    },
                    {
                        "headerName": "Cost Basis",
                        "field": "cost_basis",
                        "chartDataType": "category"
                    },
                    {
                        "headerName": "MSTR/BTC",
                        "field": "mstr_btc",
                        "chartDataType": "category"
                    },
                    {
                        "headerName": "MSTR Price",
                        "field": "mstr",
                        "chartDataType": "category"
                    },
                    {
                        "headerName": "BTC Price",
                        "field": "btc",
                        "chartDataType": "category"
                    },
                    {
                        "headerName": "Outstanding Shares",
                        "field": "total_outstanding_shares",
                        "chartDataType": "category"
                    }
                ]
            }
        }
    },
    "exchange_price_deltas": {
        "name": "Exchange Price Deltas",
        "description": "This is the percent difference between the vwap price of BTC on each exchange and the average price of BTC across those exchanges.",
        "category": "crypto",
        "defaultViz": "chart",
        "endpoint": "exchange_price_deltas",
        "gridData": {"w": 20, "h": 9},
        "source": "CCData",
        "data": {"chart": {"type": "line"}},
    },
    "ai_agents_market_data": {
        "name": "AI Agents Market Data",
        "description": "Market data for AI Agents",
        "category": "crypto",
        "defaultViz": "table",
        "endpoint": "ai_agents_market_data", 
        "gridData": {"w": 20, "h": 9},
        "source": "Geckoterminal",
        "data": {
            "table": {
                "showAll": True,
                "columnsDefs": [
                    {
                        "headerName": "Price USD",
                        "field": "price_usd",
                        "chartDataType": "category"
                    },
                    {
                        "headerName": "Volume USD",
                        "field": "volume_usd",
                        "chartDataType": "category"
                    },
                    {
                        "headerName": "Market Cap USD",
                        "field": "market_cap_usd",
                        "chartDataType": "category"
                    },
                    {
                        "headerName": "FDV USD",
                        "field": "fdv_usd",
                        "chartDataType": "category"
                    },
                    {
                        "headerName": "Total Supply",
                        "field": "total_supply",
                        "chartDataType": "category"
                    },
                    {
                        "headerName": "Total Reserve USD",
                        "field": "total_reserve_in_usd",
                        "chartDataType": "category"
                    }
                ]
            }
        }
    }, 
}

