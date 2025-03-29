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

Or using docker:

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
- URL: http://127.0.0.1:7778

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

### Main.py

The main.py file is the entry point of the FastAPI application. It:

- Creates a FastAPI instance with API documentation settings
- Configures CORS middleware to allow cross-origin requests
- Includes routers for the main API endpoints and UDF (Universal Data Feed) endpoints
- Exposes a health check endpoint at "/"
- Registers the /widgets.json and /templates.json based on the valid API keys that the user has set up

### Services

The `services` folder contains classes responsible for retrieving and processing data from various external sources.

Each service is designed to focus on a specific data extraction task, ensuring that the data is cleaned and structured appropriately for further analysis and visualization.

The services encapsulate the logic for interacting with APIs, handling data transformations, and returning results in a format that is ready for charting or other analytical purposes.

### Routes

The `routes` folder contains multiple route files, each dedicated to a specific data source (such as CoinGecko, Glassnode, Velo, etc.).

Each route file defines API endpoints that query their respective service. For example, the CoinGecko routes will call the CoinGecko service, while Glassnode routes will call the Glassnode service.

Each endpoint corresponds to a specific function that accepts parameters as input, which are then passed to the appropriate service to retrieve and process data. The processed data is transformed into visualizations and returned in JSON format.

Importantly, the routes are where users define the widget behavior specifications that are recognized by OpenBB. These specifications include:

- Parameter definitions
- Widget size recommendations (width and height)
- Widget descriptions and documentation
- Category and tags for organization in the OpenBB interface
- Any other metadata needed for proper integration with the OpenBB Workspace

This modular approach allows for a clear separation of concerns, making the application more maintainable and scalable as new data sources can be added by simply creating new route and service files.

### Templates

The templates folder contains specific templates that aggregate multiple widgets together and their respective parameter grouping.

A template may contain widgets from different sources, allowing users to define custom workflows tailored to their specific analytical needs. 

Users have the flexibility to combine various data visualizations and tools to create comprehensive dashboards that support their intended analysis objectives.

### Core

The `core` folder contains essential components that support the functionality of the CryptoBB application:

- `settings.py`: Handles application configuration and API key management, loading environment variables and providing centralized access to application settings
- `registry.py`: Implements the widget registration system, allowing dynamic registration and management of OpenBB widgets
- `session_manager.py`: Manages user sessions and authentication state throughout the application
- `landing.html`: Provides the landing page template for the application
- `plotly_config.py`: Manages the styling and configuration of all Plotly charts in the application, ensuring consistent visualization across all widgets

<details>
<summary>Plotly Chart Configuration</summary>

This directory contains utilities for creating and configuring Plotly charts with consistent styling and behavior across the application.

- `base_chart_layout.py`: Creates the base layout for charts with customizable axis titles and formatting
- `base_matrix_layout.py`: Creates the base layout for matrix/heatmap visualizations
- `plotly_config.py`: Provides standardized configuration options for all Plotly charts

#### Basic Chart Creation

To create a chart with consistent styling and behavior:

```python
from app.assets.charts.base_chart_layout import create_base_layout
from app.assets.charts.plotly_config import apply_config_to_figure
import plotly.graph_objects as go
import json

# Create a figure with base layout
figure = go.Figure(
    layout=create_base_layout(
        x_title="Date",
        y_title="Price"
    )
)

# Add your data traces
figure.add_scatter(
    x=data.index,
    y=data["values"],
    mode="lines",
    name="My Data",
    line=dict(color="#E3BF1E"),
)

# Apply standard configuration to the figure
figure = apply_config_to_figure(figure)

# Convert to JSON for frontend with config
figure_json = figure.to_json()
figure_dict = json.loads(figure_json)

return figure_dict
```

#### Configuration Options

The `plotly_config.py` module provides three main functions:

1. `get_default_config()`: Returns the default configuration for all Plotly charts
2. `get_layout_update()`: Returns standard layout updates to apply to all charts
3. `apply_config_to_figure(figure)`: Applies the layout updates to a figure and returns both the figure and config

You can customize the configuration by modifying these functions in the `plotly_config.py` file.

#### Benefits

Using these utilities ensures:

- Consistent appearance across all charts
- Standard interactive behavior (zooming, panning, etc.)
- Optimized mode bar with relevant tools
- Responsive charts that adapt to different screen sizes
- Consistent hover and click behavior

#### Customization

If you need to override specific settings for a particular chart, you can do so after applying the standard configuration:

```python
# Apply standard configuration
figure = apply_config_to_figure(figure)

# Override specific settings
figure.update_layout(
    yaxis_type='log',  # Use logarithmic scale
    showlegend=False   # Hide legend
)

# Convert to JSON with config
figure_json = figure.to_json()
figure_dict = json.loads(figure_json)

return figure_dict
```

</details>
