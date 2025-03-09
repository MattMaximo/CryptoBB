TEMPLATES = [
  {
    "name": "CoinGecko",
    "img": "https://blog.cryptoflies.com/wp-content/uploads/2023/11/sale-2.png",
    "img_dark": "",
    "img_light": "",
    "description": "CoinGecko powered dashboard with price, volume/mktcap, market dominance; and a screener.",
    "allowCustomization": True,
    "tabs": {
      "overview": {
        "id": "overview",
        "name": "Overview",
        "layout": [
          {
            "i": "coingecko_price",
            "x": 0,
            "y": 2,
            "w": 20,
            "h": 12
          },
          {
            "i": "volume_marketcap_ratio",
            "x": 20,
            "y": 2,
            "w": 20,
            "h": 12
          },
          {
            "i": "crypto_dominance",
            "x": 0,
            "y": 14,
            "w": 40,
            "h": 10
          }
        ]
      },
      "screener": {
        "id": "screener",
        "name": "Screener",
        "layout": [
          {
            "i": "screener_watchlist",
            "x": 0,
            "y": 2,
            "w": 40,
            "h": 24,
            "state": {
              "chartView": {
                "enabled": False,
                "chartType": "line"
              }
            }
          }
        ]
      }
    },
    "groups": [
      {
        "name": "Group 1",
        "type": "endpointParam",
        "paramName": "coin_id",
        "defaultValue": "bitcoin",
        "widgetIds": [
          "coingecko_price",
          "volume_marketcap_ratio",
          "crypto_dominance"
        ]
      }
    ]
  },
  {
    "name": "VeloData",
    "img": "https://velodata.app/assets/twitter_preview.png",
    "img_dark": "",
    "img_light": "",
    "description": "Open Interest, Liquidations, Funding Rates, Annualized Basis, and more.",
    "allowCustomization": True,
    "tabs": {
      "liquidations": {
        "id": "liquidations",
        "name": "Liquidations",
        "layout": [
          {
            "i": "short_liquidations",
            "x": 0,
            "y": 2,
            "w": 20,
            "h": 12
          },
          {
            "i": "long_liquidations",
            "x": 20,
            "y": 2,
            "w": 20,
            "h": 12
          },
          {
            "i": "net_liquidations",
            "x": 0,
            "y": 14,
            "w": 40,
            "h": 12
          }
        ]
      },
      "funding-rates": {
        "id": "funding-rates",
        "name": "Funding Rates",
        "layout": [
          {
            "i": "oi_weighted_funding_rates",
            "x": 0,
            "y": 2,
            "w": 40,
            "h": 11
          },
          {
            "i": "exchange_funding_rates",
            "x": 0,
            "y": 13,
            "w": 40,
            "h": 11
          }
        ]
      },
      "ohlcv": {
        "id": "ohlcv",
        "name": "OHLCV",
        "layout": [
          {
            "i": "velo_ohlcv",
            "x": 0,
            "y": 2,
            "w": 40,
            "h": 21
          }
        ]
      },
      "open-interest": {
        "id": "open-interest",
        "name": "Open Interest",
        "layout": [
          {
            "i": "open_interest",
            "x": 0,
            "y": 2,
            "w": 40,
            "h": 15
          }
        ]
      },
      "annualized-basis": {
        "id": "annualized-basis",
        "name": "Annualized Basis",
        "layout": [
          {
            "i": "velo_basis",
            "x": 0,
            "y": 2,
            "w": 40,
            "h": 17
          }
        ]
      }
    },
    "groups": [
      {
        "name": "Group 1",
        "type": "param",
        "paramName": "coin",
        "defaultValue": "BTC",
        "widgetIds": [
          "short_liquidations",
          "long_liquidations",
          "net_liquidations",
          "open_interest",
          "velo_basis",
          "oi_weighted_funding_rates",
          "exchange_funding_rates"
        ]
      },
      {
        "name": "Group 2",
        "type": "endpointParam",
        "paramName": "resolution",
        "defaultValue": "1d",
        "widgetIds": [
          "short_liquidations",
          "long_liquidations",
          "net_liquidations",
          "open_interest",
          "velo_basis",
          "oi_weighted_funding_rates",
          "velo_ohlcv",
          "exchange_funding_rates"
        ]
      },
      {
        "name": "Group 3",
        "type": "param",
        "paramName": "begin",
        "defaultValue": "2024-01-01",
        "widgetIds": [
          "short_liquidations",
          "long_liquidations",
          "net_liquidations",
          "open_interest",
          "oi_weighted_funding_rates",
          "exchange_funding_rates"
        ]
      }
    ]
  },
  {
    "name": "Matt Backend",
    "img": "https://staticg.sportskeeda.com/editor/2023/05/ca5cb-16833681547269-1920.jpg?w=640",
    "img_dark": "https://staticg.sportskeeda.com/editor/2023/05/ca5cb-16833681547269-1920.jpg?w=640",
    "img_light": "https://staticg.sportskeeda.com/editor/2023/05/ca5cb-16833681547269-1920.jpg?w=640",
    "description": "Matt Maximo crypto interface",
    "allowCustomization": True,
    "tabs": {
      "liquidations": {
        "id": "liquidations",
        "name": "Liquidations",
        "layout": [
          {
            "i": "short_liquidations",
            "x": 0,
            "y": 2,
            "w": 20,
            "h": 12
          },
          {
            "i": "long_liquidations",
            "x": 20,
            "y": 2,
            "w": 20,
            "h": 12
          },
          {
            "i": "net_liquidations",
            "x": 0,
            "y": 14,
            "w": 40,
            "h": 12
          }
        ]
      },
      "funding-rates": {
        "id": "funding-rates",
        "name": "Funding Rates",
        "layout": [
          {
            "i": "oi_weighted_funding_rates",
            "x": 0,
            "y": 2,
            "w": 40,
            "h": 11
          },
          {
            "i": "exchange_funding_rates",
            "x": 0,
            "y": 13,
            "w": 40,
            "h": 11
          }
        ]
      },
      "open-interest": {
        "id": "open-interest",
        "name": "Open Interest",
        "layout": [
          {
            "i": "open_interest",
            "x": 0,
            "y": 2,
            "w": 40,
            "h": 15,
            "state": {
              "params": {
                "coin": "ETH"
              }
            }
          }
        ]
      },
      "annualized-basis": {
        "id": "annualized-basis",
        "name": "Annualized Basis",
        "layout": [
          {
            "i": "velo_basis",
            "x": 0,
            "y": 2,
            "w": 40,
            "h": 17,
            "state": {
              "params": {
                "coin": "ETH",
                "resolution": "1w"
              }
            }
          }
        ]
      },
      "long-term-holders": {
        "id": "long-term-holders",
        "name": "Long term holders",
        "layout": [
          {
            "i": "long_term_holders_supply",
            "x": 20,
            "y": 10,
            "w": 20,
            "h": 7
          },
          {
            "i": "lth_nupl",
            "x": 0,
            "y": 2,
            "w": 40,
            "h": 8
          },
          {
            "i": "long_term_holders_net_change",
            "x": 0,
            "y": 10,
            "w": 20,
            "h": 7
          },
          {
            "i": "mvrv_zscore",
            "x": 0,
            "y": 17,
            "w": 40,
            "h": 10
          }
        ]
      },
      "btc-matrix": {
        "id": "btc-matrix",
        "name": "BTC Matrix",
        "layout": [
          {
            "i": "btc_pct_matrix",
            "x": 0,
            "y": 2,
            "w": 40,
            "h": 14
          },
          {
            "i": "btc_reserve_matrix",
            "x": 0,
            "y": 16,
            "w": 40,
            "h": 15
          }
        ]
      },
      "mstr": {
        "id": "mstr",
        "name": "MSTR",
        "layout": [
          {
            "i": "microstrategy_info",
            "x": 0,
            "y": 13,
            "w": 40,
            "h": 13,
            "state": {
              "chartView": {
                "enabled": False,
                "chartType": "line"
              }
            }
          },
          {
            "i": "microstrategy_premium",
            "x": 0,
            "y": 2,
            "w": 40,
            "h": 11
          }
        ]
      },
      "exchanges": {
        "id": "exchanges",
        "name": "Exchanges",
        "layout": [
          {
            "i": "exchange_price_deltas",
            "x": 0,
            "y": 2,
            "w": 40,
            "h": 9
          },
          {
            "i": "spot_exchange_volume",
            "x": 0,
            "y": 11,
            "w": 40,
            "h": 13
          }
        ]
      },
      "ta": {
        "id": "ta",
        "name": "TA",
        "layout": [
          {
            "i": "ta_macd",
            "x": 0,
            "y": 2,
            "w": 20,
            "h": 9
          },
          {
            "i": "ta_rsi",
            "x": 20,
            "y": 2,
            "w": 20,
            "h": 9
          },
          {
            "i": "ta_fibonacci_retracement",
            "x": 0,
            "y": 11,
            "w": 12,
            "h": 12,
            "state": {
              "params": {
                "interval": "days"
              },
              "chartView": {
                "enabled": False,
                "chartType": "line"
              }
            }
          },
          {
            "i": "ta_stochastic",
            "x": 12,
            "y": 11,
            "w": 28,
            "h": 12,
            "state": {
              "params": {
                "interval": "days"
              }
            }
          }
        ]
      },
      "aave-pools": {
        "id": "aave-pools",
        "name": "AAVE pools",
        "layout": [
          {
            "i": "aave_utilization_rate",
            "x": 0,
            "y": 11,
            "w": 40,
            "h": 13
          },
          {
            "i": "aave_lending_rate",
            "x": 0,
            "y": 2,
            "w": 20,
            "h": 9
          },
          {
            "i": "aave_borrow_rate",
            "x": 20,
            "y": 2,
            "w": 20,
            "h": 9
          }
        ]
      }
    },
    "groups": [
      {
        "name": "Group 1",
        "type": "param",
        "paramName": "coin",
        "defaultValue": "ETH",
        "widgetIds": [
          "short_liquidations",
          "long_liquidations",
          "net_liquidations",
          "oi_weighted_funding_rates",
          "exchange_funding_rates",
          "open_interest",
          "velo_basis"
        ]
      },
      {
        "name": "Group 2",
        "type": "endpointParam",
        "paramName": "resolution",
        "defaultValue": "1w",
        "widgetIds": [
          "short_liquidations",
          "long_liquidations",
          "net_liquidations",
          "oi_weighted_funding_rates",
          "exchange_funding_rates",
          "open_interest",
          "velo_basis"
        ]
      },
      {
        "name": "Group 3",
        "type": "param",
        "paramName": "begin",
        "defaultValue": "2024-01-01",
        "widgetIds": [
          "short_liquidations",
          "long_liquidations",
          "net_liquidations",
          "oi_weighted_funding_rates",
          "exchange_funding_rates",
          "open_interest"
        ]
      },
      {
        "name": "Group 4",
        "type": "param",
        "paramName": "exchange",
        "defaultValue": "binance",
        "widgetIds": [
          "ta_macd",
          "ta_rsi",
          "ta_fibonacci_retracement",
          "ta_stochastic"
        ]
      },
      {
        "name": "Group 5",
        "type": "param",
        "paramName": "symbol",
        "defaultValue": "BTC-USDT",
        "widgetIds": [
          "ta_macd",
          "ta_rsi",
          "ta_fibonacci_retracement",
          "ta_stochastic"
        ]
      },
      {
        "name": "Group 6",
        "type": "param",
        "paramName": "interval",
        "defaultValue": "days",
        "widgetIds": [
          "ta_macd",
          "ta_rsi",
          "ta_fibonacci_retracement",
          "ta_stochastic"
        ]
      },
      {
        "name": "Group 7",
        "type": "param",
        "paramName": "aggregate",
        "defaultValue": "1",
        "widgetIds": [
          "ta_macd",
          "ta_rsi",
          "ta_fibonacci_retracement",
          "ta_stochastic"
        ]
      },
      {
        "name": "Group 8",
        "type": "endpointParam",
        "paramName": "pool",
        "defaultValue": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb480x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e1",
        "widgetIds": [
          "aave_utilization_rate",
          "aave_lending_rate",
          "aave_borrow_rate"
        ]
      }
    ]
  }
]