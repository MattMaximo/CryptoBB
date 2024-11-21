# CryptoBB

OpenBB backend for Crypto Traders.

#### Docker

```
docker build -t crypto-backend .
docker run --env-file .env -p 7778:7778 crypto-backend
```

# Repo Structure 

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

