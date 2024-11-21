def create_base_layout(x_title: str, y_title: str):
    return dict(
        title=None,
        xaxis=dict(
            title=x_title,
            gridcolor="#2f3338",  # Dark gray
            color="#ffffff",  # White
        ),
        yaxis=dict(
            title=y_title,
            gridcolor="#2f3338",  # Dark gray
            color="#ffffff",  # White
            tickformat=".2s" # Format large numbers with 2 decimals. Need to manual override for percentage
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,  # Position above the plot
            xanchor="center",
            x=0.5,  # Center the legend
            font=dict(color="#ffffff"),  # White
        ),
        margin=dict(b=0, l=0, r=0, t=50),  # Adjust margin for the title
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent black
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent black
        font=dict(color="#ffffff"),  # White
        hovermode="x unified", # Put all hover data on the same x-axis
        hoverlabel=dict(
            bgcolor="white",  # White
            font_color="black"  # Black
        )
    )