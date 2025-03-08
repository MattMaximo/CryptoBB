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
  }
]