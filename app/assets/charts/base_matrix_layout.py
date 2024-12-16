import plotly.express as px

def get_matrix_figure(matrix_data, y_label: str = "BTC Amount", hover_label: str = "Value"):
    fig = px.imshow(
        matrix_data.values,
        labels=dict(
            x="CAGR (%)",
            y=y_label,
            color=""
        ),
        x=matrix_data.columns,
        y=matrix_data.index,
        aspect="auto",
        color_continuous_scale=[
            [0, 'rgb(165, 0, 38)'],      # Deep red for very low values
            [0.05, 'rgb(220,100,50)'],   # Lighter red
            [0.1, 'rgb(240,180,80)'],   # Orange-yellow transition
            [0.15, 'rgb(240,230,140)'],  # Yellow
            [0.2, 'rgb(180,230,100)'],  # Yellow-green transition
            [0.6, 'rgb(100,200,50)'],   # Light green
            [1.0, 'rgb(0,103,50)']     # Deep green
        ],
        zmin=0,
        zmax=max(matrix_data.values.max() * 0.1, 1)
    )
    
    fig.update_traces(
        text=matrix_data.values.round(1),
        texttemplate="%{text}",
        textfont=dict(size=11, color="black"),
        hovertemplate=f"CAGR (%): %{{x}}<br>{y_label}: %{{y}}<br>{hover_label}: %{{z}}<extra></extra>"
    )
    
    fig.update_layout(
        xaxis=dict(
            title="CAGR (%)",
            showgrid=False,
            color="#ffffff",
            tickangle=-45,
            tickfont=dict(size=10),
            title_font=dict(size=12),
            side="top",
            title_standoff=15
        ),
        yaxis=dict(
            title=y_label,
            showgrid=True,
            gridcolor="rgba(128, 128, 128, 0.2)",
            color="#ffffff",
            tickfont=dict(size=10),
            title_font=dict(size=12),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff"),
        margin=dict(b=0, l=0, r=0, t=25),
        height=450,
        coloraxis_showscale=False
    )
    return fig