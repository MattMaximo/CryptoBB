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
            "i": "coingecko/price",
            "x": 0,
            "y": 0,
            "w": 40,
            "h": 12
          },
          {
            "i": "coingecko/vm-ratio",
            "x": 0,
            "y": 12,
            "w": 20,
            "h": 9
          },
          {
            "i": "coingecko/dominance",
            "x": 20,
            "y": 12,
            "w": 20,
            "h": 9
          }
        ]
      },
      "screener": {
        "id": "screener",
        "name": "Screener",
        "layout": [
          {
            "i": "coingecko/coin-list",
            "x": 0,
            "y": 21,
            "w": 40,
            "h": 9
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
          "coingecko/price",
          "coingecko/vm-ratio",
          "coingecko/dominance",
          "coingecko/coin-list"
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
            "i": "velo/short-liquidations",
            "x": 0,
            "y": 2,
            "w": 20,
            "h": 12
          },
          {
            "i": "velo/long-liquidations",
            "x": 20,
            "y": 2,
            "w": 20,
            "h": 12
          },
          {
            "i": "velo/net-liquidations",
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
            "i": "velo/oi-weighted-funding-rates",
            "x": 0,
            "y": 2,
            "w": 40,
            "h": 11
          },
          {
            "i": "velo/exchange-funding-rates",
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
            "i": "velo/ohlcv",
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
            "i": "velo/open-interest",
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
            "i": "velo/basis",
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
          "velo/short-liquidations",
          "velo/long-liquidations",
          "velo/net-liquidations",
          "velo/oi-weighted-funding-rates",
          "velo/exchange-funding-rates",
          "velo/open-interest",
          "velo/basis"
        ]
      },
      {
        "name": "Group 2",
        "type": "endpointParam",
        "paramName": "resolution",
        "defaultValue": "1d",
        "widgetIds": [
          "velo/short-liquidations",
          "velo/long-liquidations",
          "velo/net-liquidations",
          "velo/oi-weighted-funding-rates",
          "velo/exchange-funding-rates",
          "velo/open-interest",
          "velo/basis"
        ]
      },
      {
        "name": "Group 3",
        "type": "param",
        "paramName": "begin",
        "defaultValue": "2024-01-01",
        "widgetIds": [
          "velo/short-liquidations",
          "velo/long-liquidations",
          "velo/net-liquidations",
          "velo/oi-weighted-funding-rates",
          "velo/exchange-funding-rates",
          "velo/open-interest",
          "velo/basis"
        ]
      },
      {
        "name": "Group 4",
        "type": "param",
        "paramName": "exchange",
        "defaultValue": "binance",
        "widgetIds": [
          "ta/stochastic"
        ]
      },
      {
        "name": "Group 5",
        "type": "param",
        "paramName": "symbol",
        "defaultValue": "BTC-USDT",
        "widgetIds": [
          "ta/stochastic"
        ]
      },
      {
        "name": "Group 6",
        "type": "param",
        "paramName": "interval",
        "defaultValue": "days",
        "widgetIds": [
          "ta/stochastic"
        ]
      },
      {
        "name": "Group 7",
        "type": "param",
        "paramName": "aggregate",
        "defaultValue": "1",
        "widgetIds": [
          "ta/stochastic"
        ]
      },
      {
        "name": "Group 8",
        "type": "endpointParam",
        "paramName": "pool",
        "defaultValue": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb480x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e1",
        "widgetIds": [
          "aave/utilization-rate",
          "aave/lending-rate",
          "aave/borrow-rate"
        ]
      },
      {
        "name": "Group 9",
        "type": "param",
        "paramName": "ticker",
        "defaultValue": "BTCUSDT",
        "widgetIds": [
          "velo/ohlcv"
        ]
      },
      {
        "name": "Group 10",
        "type": "param",
        "paramName": "exchange",
        "defaultValue": "binance",
        "widgetIds": [
          "velo/ohlcv"
        ]
      },
      {
        "name": "Group 11",
        "type": "endpointParam",
        "paramName": "resolution",
        "defaultValue": "1d",
        "widgetIds": [
          "velo/ohlcv"
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
            "i": "velo/short-liquidations",
            "x": 0,
            "y": 2,
            "w": 20,
            "h": 12
          },
          {
            "i": "velo/long-liquidations",
            "x": 20,
            "y": 2,
            "w": 20,
            "h": 12
          },
          {
            "i": "velo/net-liquidations",
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
            "i": "velo/oi-weighted-funding-rates",
            "x": 0,
            "y": 2,
            "w": 40,
            "h": 11
          },
          {
            "i": "velo/exchange-funding-rates",
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
            "i": "velo/open-interest",
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
            "i": "velo/basis",
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
        "name": "Long Term Holders",
        "layout": [
          {
            "i": "glassnode/lth-supply",
            "x": 0,
            "y": 0,
            "w": 40,
            "h": 15
          },
          {
            "i": "glassnode/lth-net-change",
            "x": 0,
            "y": 15,
            "w": 40,
            "h": 15
          },
          {
            "i": "glassnode/lth-nupl",
            "x": 0,
            "y": 30,
            "w": 40,
            "h": 15
          }
        ]
      },
      "btc-matrix": {
        "id": "btc-matrix",
        "name": "BTC Matrix",
        "layout": [
          {
            "i": "btc-matrix/reserve-dollars",
            "x": 0,
            "y": 0,
            "w": 40,
            "h": 20
          },
          {
            "i": "btc-matrix/reserve-pct",
            "x": 0,
            "y": 20,
            "w": 40,
            "h": 20
          }
        ]
      },
      "mstr": {
        "id": "mstr",
        "name": "MSTR",
        "layout": [
          {
            "i": "microstrategy/info",
            "x": 0,
            "y": 0,
            "w": 40,
            "h": 9
          },
          {
            "i": "microstrategy/premium",
            "x": 0,
            "y": 9,
            "w": 40,
            "h": 9
          }
        ]
      },
      "exchanges": {
        "id": "exchanges",
        "name": "Exchanges",
        "layout": [
          {
            "i": "ccdata/exchange-price-deltas",
            "x": 0,
            "y": 0,
            "w": 40,
            "h": 15
          },
          {
            "i": "ccdata/exchange-spot-volume",
            "x": 0,
            "y": 15,
            "w": 40,
            "h": 15
          },
          {
            "i": "ccdata/candles",
            "x": 0,
            "y": 30,
            "w": 40,
            "h": 20
          }
        ]
      },
      "ta": {
        "id": "ta",
        "name": "TA",
        "layout": [
          {
            "i": "ta/macd",
            "x": 0,
            "y": 2,
            "w": 20,
            "h": 9
          },
          {
            "i": "ta/rsi",
            "x": 20,
            "y": 2,
            "w": 20,
            "h": 9
          },
          {
            "i": "ta/fibonacci-retracement",
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
            "i": "ta/stochastic",
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
            "i": "aave/utilization-rate",
            "x": 0,
            "y": 11,
            "w": 40,
            "h": 13
          },
          {
            "i": "aave/lending-rate",
            "x": 0,
            "y": 2,
            "w": 20,
            "h": 9
          },
          {
            "i": "aave/borrow-rate",
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
          "velo/short-liquidations",
          "velo/long-liquidations",
          "velo/net-liquidations",
          "velo/oi-weighted-funding-rates",
          "velo/exchange-funding-rates",
          "velo/open-interest",
          "velo/basis"
        ]
      },
      {
        "name": "Group 2",
        "type": "endpointParam",
        "paramName": "resolution",
        "defaultValue": "1w",
        "widgetIds": [
          "velo/short-liquidations",
          "velo/long-liquidations",
          "velo/net-liquidations",
          "velo/oi-weighted-funding-rates",
          "velo/exchange-funding-rates",
          "velo/open-interest",
          "velo/basis"
        ]
      },
      {
        "name": "Group 3",
        "type": "param",
        "paramName": "begin",
        "defaultValue": "2024-01-01",
        "widgetIds": [
          "velo/short-liquidations",
          "velo/long-liquidations",
          "velo/net-liquidations",
          "velo/oi-weighted-funding-rates",
          "velo/exchange-funding-rates",
          "velo/open-interest",
          "velo/basis"
        ]
      },
      {
        "name": "Group 4",
        "type": "param",
        "paramName": "asset",
        "defaultValue": "btc",
        "widgetIds": [
          "glassnode/lth-supply",
          "glassnode/lth-net-change",
          "glassnode/lth-nupl",
          "glassnode/price",
          "glassnode/mvrv-zscore"
        ]
      },
      {
        "name": "Group 5",
        "type": "param",
        "paramName": "exchange",
        "defaultValue": "binance",
        "widgetIds": [
          "ccdata/exchange-spot-volume"
        ]
      }
    ]
  },
  {
    "name": "Glassnode",
    "img": "https://tvblog-static.tradingview.com/uploads/2021/08/glassnode-preview.png",
    "img_dark": "",
    "img_light": "",
    "description": "Glassnode on-chain metrics including Long Term Holders Supply, MVRV Z-Score, and more.",
    "allowCustomization": True,
    "tabs": {
      "long-term-holders": {
        "id": "long-term-holders",
        "name": "Long Term Holders",
        "layout": [
          {
            "i": "glassnode/lth-supply",
            "x": 0,
            "y": 0,
            "w": 40,
            "h": 15
          },
          {
            "i": "glassnode/lth-net-change",
            "x": 0,
            "y": 15,
            "w": 40,
            "h": 15
          },
          {
            "i": "glassnode/lth-nupl",
            "x": 0,
            "y": 30,
            "w": 40,
            "h": 15
          }
        ]
      },
      "market-metrics": {
        "id": "market-metrics",
        "name": "Market Metrics",
        "layout": [
          {
            "i": "glassnode/price",
            "x": 0,
            "y": 0,
            "w": 40,
            "h": 15
          },
          {
            "i": "glassnode/mvrv-zscore",
            "x": 0,
            "y": 15,
            "w": 40,
            "h": 15
          }
        ]
      }
    },
    "groups": [
      {
        "name": "Group 1",
        "type": "param",
        "paramName": "asset",
        "defaultValue": "btc",
        "widgetIds": [
          "glassnode/lth-supply",
          "glassnode/lth-net-change",
          "glassnode/lth-nupl",
          "glassnode/price",
          "glassnode/mvrv-zscore"
        ]
      }
    ]
  },
  {
    "name": "BTC Matrix",
    "img": "https://cryptologos.cc/logos/bitcoin-btc-logo.png",
    "img_dark": "",
    "img_light": "",
    "description": "Bitcoin reserve matrices showing holdings of countries and companies.",
    "allowCustomization": True,
    "tabs": {
      "reserve-matrices": {
        "id": "reserve-matrices",
        "name": "Reserve Matrices",
        "layout": [
          {
            "i": "btc-matrix/reserve-dollars",
            "x": 0,
            "y": 0,
            "w": 40,
            "h": 20
          },
          {
            "i": "btc-matrix/reserve-pct",
            "x": 0,
            "y": 20,
            "w": 40,
            "h": 20
          }
        ]
      }
    }
  },
  {
    "name": "CCData",
    "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR9qxD4QtL8MxMebdzeiPEI-0NNmUidxRdfBw&s",
    "img_dark": "",
    "img_light": "",
    "description": "Cryptocurrency market data from CCData including exchange price deltas and candles.",
    "allowCustomization": True,
    "tabs": {
      "exchange-data": {
        "id": "exchange-data",
        "name": "Exchange Data",
        "layout": [
          {
            "i": "ccdata/exchange-price-deltas",
            "x": 0,
            "y": 0,
            "w": 40,
            "h": 15
          },
          {
            "i": "ccdata/exchange-spot-volume",
            "x": 0,
            "y": 15,
            "w": 40,
            "h": 15
          }
        ]
      },
      "market-data": {
        "id": "market-data",
        "name": "Market Data",
        "layout": [
          {
            "i": "ccdata/candles",
            "x": 0,
            "y": 0,
            "w": 40,
            "h": 20
          }
        ]
      }
    },
    "groups": [
      {
        "name": "Group 1",
        "type": "param",
        "paramName": "exchange",
        "defaultValue": "binance",
        "widgetIds": [
          "ccdata/exchange-spot-volume"
        ]
      }
    ]
  }
]