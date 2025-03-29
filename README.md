# CryptoBB

Crypto backend to be used by OpenBB Workspace.

![Gm_e1IzXwAAzaYQ](https://github.com/user-attachments/assets/de7f8770-cbed-47ef-93c9-68559b1d3b83)

Powered by:
- CoinGecko
- Velodata
- Glassnode
- CCData
- Google Trends

... and more to come.

## Getting Started

### API keys

Rename the `.env.example` file to `.env` and update the API keys based on what you get from these vendors:

```
COINGECKO_API_KEY="your_coingecko_api_key"
GLASSNODE_API_KEY="your_glassnode_api_key"
VELO_API_KEY="your_velo_api_key"
CCDATA_API_KEY="your_ccdata_api_key"
```

### Running

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 7778
```

## Docker

```bash
docker build -t crypto-backend .
docker run --env-file .env -p 7778:7778 crypto-backend
```

You can test that it is running by accessing [http://127.0.0.1:7778](http://127.0.0.1:7778).

If it is running successfully, you should see:

![CleanShot 2025-03-29 at 16 09 47](https://github.com/user-attachments/assets/d371f85a-49ef-4350-a0f6-0ab4bdbf1b00)


### Integrating to OpenBB

Go into OpenBB Workspace at [https://pro.openbb.co/](https://pro.openbb.co/) and add this custom backend.

- Name: CryptoBB
- URL: http://127.0.0.1:7778)

If all is working you can click "Test" and get the confirmation of how many widgets are valid. See below,

![CleanShot 2025-03-29 at 16 10 41](https://github.com/user-attachments/assets/82949108-b9ce-4f84-819b-943de4360a44)

Note: You can have OpenBB Workspace running as a native app within your desktop, see [https://docs.openbb.co/workspace/native-installation](https://docs.openbb.co/workspace/native-installation).

### Visualizing data

If you go into the "Templates" tab you will see a few out of the box templates to get started.

![CleanShot 2025-03-29 at 16 12 33](https://github.com/user-attachments/assets/52c6b474-705e-4334-9298-44f740b4f2e9)

If you go into Velo data, for instance - you will see:

![CleanShot 2025-03-29 at 16 14 04](https://github.com/user-attachments/assets/061e4694-19f2-4239-81f6-85b9e4f694b2)

And you will be able to use OpenBB's AI agent or bring your own into the workspace.

## Repo Structure 

## Main.py
The main.py file is the entry point of the FastAPI application. It:

- Creates a FastAPI instance with API documentation settings
- Configures CORS middleware to allow cross-origin requests
- Includes routers for the main API endpoints and UDF (Universal Data Feed) endpoints
- Exposes a health check endpoint at "/"

The application serves as a backend API for cryptocurrency market analysis, providing endpoints for market data, dominance metrics, and other crypto-related analytics.

## Services
The `services` folder contains classes responsible for retrieving and processing data from various external sources. Each service is designed to focus on a specific data extraction task, ensuring that the data is cleaned and structured appropriately for further analysis and visualization. The services encapsulate the logic for interacting with APIs, handling data transformations, and returning results in a format that is ready for charting or other analytical purposes.

## API
The `routes.py` file defines the API endpoints for the CryptoBB backend. Each endpoint corresponds to a specific function that accepts parameters as input. These parameters are utilized to invoke the appropriate service, which retrieves the necessary data. The data is then processed to create visualizations, which are returned in JSON format. This structure allows for a clear separation of concerns, where the routing logic is distinct from the data retrieval and processing logic, promoting maintainability and scalability of the application.

## Core
The `core` folder contains essential components that support the functionality of the CryptoBB application. Specifically, the `widgets.py` file defines custom OpenBB widgets that are utilized in the API route outputs. These widgets can represent various data visualizations, such as charts and tables, allowing users to interactively explore and analyze cryptocurrency data. The modular design of the core components promotes reusability and maintainability within the application.

## Assets
The assets folder contains various hardcoded assets such as a manually created list of Aave pools or static images.


# Implementation Guide

## 1. Creating your service
This is where you will make any API or database calls and structure data.

If you are using any secrets, make sure to add your API key to a .env file or set as an environment variable. You will then need to update the settings file with a placeholder like this:

```MY_SECRET_VARIABLE_NAME : str = "your_api_hash"```

In the file for your new service class, you will need to add the following to your imports:

```
from app.core.settings import get_settings

settings = get_settings()
```

You can access the secrets in your script by:

```secret = settings.MY_SECRET_VARIABLE_NAME```

Finally, you can begin writing the python code to extract and clean your data, returning a pandas dataframe with the desired output data. This is a good place to make api calls, database queries, and transaformations.

## 2. API Route
Here you'll create you API endpoint that accepts parameters, passes them to the service to get the data, creates a chart and returns the chart as json.

Example imports to access your service:

```
from app.services.your_services_file_name_no_py import service_class_name

service_name = service_class_name() #instantiate the class
```

The route will be define like this:
```
@router.get('/endpoint_name')
def function_to_create_chart_json(params):
    #call service
    #create chart
    #return chart as json
```

