"""
Plotly config settings for consistent chart behavior.

This module provides standardized configuration options for Plotly charts,
ensuring consistent interactivity, responsiveness, and appearance.
"""


def get_default_config():
    """
    Returns the default configuration for all Plotly charts in the application.
    
    This configuration:
    - Enables responsive behavior for charts
    - Configures the mode bar with appropriate settings
    - Sets up standard interaction modes
    - Defines transition animations
    
    Returns:
        dict: A dictionary of Plotly configuration settings
    """
    return {
        # Display options
        'displayModeBar': True,  # Always show the mode bar
        'responsive': True,  # Make charts responsive to window size
        'scrollZoom': True,  # Enable scroll to zoom
        
        # Mode bar configuration
        'modeBarButtonsToRemove': [
            'lasso2d',  # Remove lasso selection tool
            'select2d',  # Remove box selection tool
            'autoScale2d',  # Remove auto scale
            'toggleSpikelines',  # Remove spike lines
            'hoverClosestCartesian',  # Remove closest point hover
            'hoverCompareCartesian'  # Remove compare hover
        ],
        'modeBarButtonsToAdd': [
            'drawline',
            'drawcircle',
            'drawrect',
            'eraseshape'
        ],
        
        # Interaction settings
        'doubleClick': 'reset+autosize',  # Double-click to reset view
        'showTips': True,  # Show tips for interactions
        
        # Other settings
        'watermark': False,
        'staticPlot': False,  # Enable interactivity
        'locale': 'en',
        'showAxisDragHandles': True,  # Show axis drag handles
        'showAxisRangeEntryBoxes': True,  # Show axis range entry boxes
    }


def get_chart_colors(theme="dark"):
    """
    Returns standard colors for chart elements based on the theme.
    
    Parameters:
        theme (str): The theme to use, either "light" or "dark"
    
    Returns:
        dict: A dictionary of color settings for various chart elements
    """
    if theme == "light":
        return {
            # Main chart line colors
            'text': '#2E5090',
            'main_line': '#2E5090',   # Navy blue for light theme
            'positive': '#00AA44',    # Forest green for positive values
            'negative': '#CC0000',    # Red for negative values
            'neutral': '#3366CC',     # Blue for neutral values
            'sma_line': 'black',      # SMA line color
            # Additional colors for multiple series
            'secondary': '#8C4646',   # Burgundy
            'tertiary': '#5F4B8B',    # Muted purple
        }
    else:  # dark theme (default)
        return {
            # Main chart line colors
            'text': '#FF8000',
            'main_line': '#FF8000',   # orange
            'positive': '#00B140',    # green
            'negative': '#F4284D',    # red
            'neutral': '#2D9BF0',     # blue
            'sma_line': 'white',      # SMA line color
            # Additional colors for multiple series
            'secondary': '#9E69AF',   # purple
            'tertiary': '#00C2DE',    # teal
        }


def get_layout_update(theme="dark"):
    """
    Returns standard layout updates to apply to all charts.
    
    This includes:
    - UI revision settings for maintaining state
    - Transition animations
    - Drag mode settings
    - Hover and click behavior
    
    Parameters:
        theme (str): The theme to use, either "light" or "dark"
    
    Returns:
        dict: A dictionary of layout settings to update Plotly charts
    """
    # Define color schemes based on theme
    if theme == "light":
        text_color = '#333333'
        grid_color = 'rgba(221, 221, 221, 0.3)'  # Very faded grid
        line_color = '#AAAAAA'
        tick_color = '#AAAAAA'
        bg_color = '#ffffff'  # More opaque background
        active_color = '#3366CC'  # Nice blue color for light theme
        # Black text for better contrast in light mode
        legend_text_color = '#000000'
        # Darker border for better visibility
        legend_border_color = '#ffffff'
    else:  # dark theme (default)
        text_color = '#FFFFFF'
        grid_color = 'rgba(51, 51, 51, 0.3)'  # Very faded grid
        line_color = '#444444'
        tick_color = '#444444'
        bg_color = '#151518'  # More opaque background
        active_color = '#FF8000'  # Orange color for dark theme
        legend_text_color = text_color  # Use the same text color
        legend_border_color = "#151518"  # Use the same border color
    
    return {
        'uirevision': 'constant',  # Maintains view state during updates
        'autosize': True,  # Enables auto-sizing for responsive behavior
        'dragmode': 'zoom',  # Sets default mode to zoom instead of pan
        'hovermode': 'closest',  # Improves hover experience
        'clickmode': 'event',  # Makes clicking more responsive
        'margin': {
            't': 50,  # Top margin - increase this for more modebar space
            'r': 30,  # Right margin
            'b': 40,  # Bottom margin
            'l': 40,  # Left margin
            'pad': 4   # Padding between the plotting area and the axis lines
        },
        'transition': {
            'duration': 50,  # Small transition for smoother feel
            'easing': 'cubic-in-out'  # Smooth easing function
        },
        'modebar': {
            'orientation': 'v',  # Vertical orientation for modebar
            'activecolor': active_color  # Active button color
        },
        'font': {
            'family': 'Arial, sans-serif',  # Sans-serif font
            'size': 12,
            'color': text_color  # Text color based on theme
        },
        'xaxis': {
            'rangeslider': {'visible': False},  # Disable rangeslider
            'autorange': True,  # Enable autorange
            'constrain': 'domain',  # Constrain to domain for better zoom
            'showgrid': True,  # Show vertical grid lines
            'gridcolor': grid_color,  # Very faded grid lines
            'linecolor': line_color,  # Axis line color based on theme
            'tickcolor': tick_color,  # Tick color based on theme
            'linewidth': 1,  # Match y-axis line width
            'mirror': True,  # Mirror axis to match y-axis
            'showline': False,  # Hide the axis line to remove the box
            'zeroline': False,  # Hide zero line to match y-axis
            'ticks': 'outside',  # Place ticks outside
            'tickwidth': 1  # Match y-axis tick width
        },
        'yaxis': {
            'autorange': True,  # Enable autorange
            'constrain': 'domain',  # Constrain to domain
            'fixedrange': False,  # Allow y-axis zooming
            'showgrid': True,  # Show horizontal grid lines
            'gridcolor': grid_color,  # Very faded grid lines
            'linecolor': line_color,  # Axis line color based on theme
            'tickcolor': tick_color,  # Tick color based on theme
            'linewidth': 1,  # Consistent line width
            'mirror': True,  # Mirror axis
            'showline': False,  # Hide the axis line to remove the box
            'zeroline': False,  # Hide zero line
            'ticks': 'outside',  # Place ticks outside
            'tickwidth': 1  # Consistent tick width
        },
        'legend': {
            # Legend text color with better contrast
            'font': {'color': legend_text_color},
            'bgcolor': bg_color,  # More opaque background
            'bordercolor': legend_border_color,  # Better visible border
            'borderwidth': 1  # Add border width for better visibility
        },
    }


def apply_config_to_figure(figure, theme="dark"):
    """
    Applies the default configuration and layout updates to a Plotly figure.
    
    Parameters:
        figure (plotly.graph_objects.Figure): The Plotly figure to configure
        theme (str): The theme to use, either "light" or "dark"
        
    Returns:
        tuple: (figure, config) where figure is the configured Plotly figure
               and config is the configuration dictionary
    """
    # Apply layout updates with the specified theme
    figure.update_layout(**get_layout_update(theme))
    
    # Return both the figure and the config
    return figure
