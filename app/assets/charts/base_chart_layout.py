def create_base_layout(
    x_title: str, 
    y_title: str, 
    y_dtype: str = ".2s", 
    theme: str = "dark"
):
    """
    Creates a base layout for a Plotly chart with customizable axis titles and
    y-axis formatting.

    Parameters:
    - x_title (str): The title for the x-axis. If the title is a date-related
      term, it will be set to None.
    - y_title (str): The title for the y-axis.
    - y_dtype (str): Optional. Specifies the format of the y-axis labels.
      Default is ".2s".
      Available options include:
      - ".2s": Short scale formatting with two significant digits (e.g., 1.2K).
      - ".2f": Fixed-point notation with two decimal places (e.g., 1234.56).
      - ".0f": Fixed-point notation with no decimal places (e.g., 1235).
      - ".0%": Percentage with no decimal places (e.g., 50%).
      - ".2%": Percentage with two decimal places (e.g., 50.00%).
      - "$,.2f": Currency format with two decimal places and comma as 
        thousand separator (e.g., $1,234.56).
      - ".2e": Scientific notation with two decimal places (e.g., 1.23e+3).
    - theme (str): Optional. The theme to use, either "light" or "dark".
      Default is "dark".

    Returns:
    - dict: A dictionary representing the layout configuration for a Plotly chart.
    """
    # Define colors based on theme
    if theme == "light":
        text_color = "#333333"  # Dark gray for light theme
        grid_color = "rgba(128, 128, 128, 0.2)"
        paper_bgcolor = "rgba(255,255,255,0)"  # Transparent white
        plot_bgcolor = "rgba(255,255,255,0)"  # Transparent white
        hoverlabel_bgcolor = "black"
        hoverlabel_font_color = "white"
    else:  # dark theme (default)
        text_color = "#ffffff"  # White for dark theme
        grid_color = "rgba(128, 128, 128, 0.2)"
        paper_bgcolor = "rgba(0,0,0,0)"  # Transparent black
        plot_bgcolor = "rgba(0,0,0,0)"  # Transparent black
        hoverlabel_bgcolor = "white"
        hoverlabel_font_color = "black"

    if x_title.lower() in ['date', 'time', 'timestamp', 'datetime']:
        x_title = None
    return dict(
        title=None,
        xaxis=dict(
            title=x_title,
            showgrid=False,  # Remove x-axis gridlines
            color=text_color,
        ),
        yaxis=dict(
            title=y_title,
            showgrid=True,  # Show primary y-axis gridlines
            gridcolor=grid_color,
            color=text_color,
            tickformat=y_dtype
        ),
        yaxis2=dict(
            showgrid=False,  # Hide secondary y-axis gridlines
            color=text_color,
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,  # Position above the plot
            xanchor="center",
            x=0.5,  # Center the legend
            font=dict(color=text_color),
        ),
        margin=dict(b=0, l=0, r=0, t=0),  # Adjust margin for the title
        paper_bgcolor=paper_bgcolor,
        plot_bgcolor=plot_bgcolor,
        font=dict(color=text_color),
        hovermode="x unified",  # Put all hover data on the same x-axis
        hoverlabel=dict(
            bgcolor=hoverlabel_bgcolor,
            font_color=hoverlabel_font_color
        )
    )