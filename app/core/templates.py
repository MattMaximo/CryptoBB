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
  }
]