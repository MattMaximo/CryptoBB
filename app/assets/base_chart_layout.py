def create_base_layout(x_title: str, y_title: str):
    return dict(
        xaxis=dict(
            title=x_title,
            gridcolor="#2f3338",
            color="#ffffff",
        ),
        yaxis=dict(
            title=y_title,
            gridcolor="#2f3338",
            color="#ffffff",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,  # Position above the plot
            xanchor="center",
            x=0.5,  # Center the legend
            font=dict(color="#ffffff"),
        ),
        margin=dict(b=0, l=0, r=0, t=50),  # Adjust margin for the title
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff"),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            font_color="black"
        )
    )