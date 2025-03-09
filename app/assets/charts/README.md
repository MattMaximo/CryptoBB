# Plotly Chart Configuration

This directory contains utilities for creating and configuring Plotly charts with consistent styling and behavior across the application.

## Files

- `base_chart_layout.py`: Creates the base layout for charts with customizable axis titles and formatting
- `base_matrix_layout.py`: Creates the base layout for matrix/heatmap visualizations
- `plotly_config.py`: Provides standardized configuration options for all Plotly charts

## How to Use

### Basic Chart Creation

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
figure, config = apply_config_to_figure(figure)

# Convert to JSON for frontend with config
figure_json = figure.to_json()
figure_dict = json.loads(figure_json)
figure_dict["config"] = config

return figure_dict
```

### Configuration Options

The `plotly_config.py` module provides three main functions:

1. `get_default_config()`: Returns the default configuration for all Plotly charts
2. `get_layout_update()`: Returns standard layout updates to apply to all charts
3. `apply_config_to_figure(figure)`: Applies the layout updates to a figure and returns both the figure and config

You can customize the configuration by modifying these functions in the `plotly_config.py` file.

### Benefits

Using these utilities ensures:

- Consistent appearance across all charts
- Standard interactive behavior (zooming, panning, etc.)
- Optimized mode bar with relevant tools
- Responsive charts that adapt to different screen sizes
- Consistent hover and click behavior

## Customization

If you need to override specific settings for a particular chart, you can do so after applying the standard configuration:

```python
# Apply standard configuration
figure, config = apply_config_to_figure(figure)

# Override specific settings
figure.update_layout(
    yaxis_type='log',  # Use logarithmic scale
    showlegend=False   # Hide legend
)

# Convert to JSON with config
figure_json = figure.to_json()
figure_dict = json.loads(figure_json)
figure_dict["config"] = config

return figure_dict
``` 