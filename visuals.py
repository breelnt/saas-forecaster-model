import plotly.express as px

def plot_growth_forecast(df):
    """
    Creates a simple line chart showing predicted revenue growth.
    """
    fig = px.line(
        df, 
        x="Month", 
        y="Revenue at End",
        labels={
            "Revenue at End": "Monthly Revenue ($)",
            "Month": "Timeframe"
        },
        title="Predicted Revenue Growth"
    )
    
    # Clean, professional styling
    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
        yaxis_tickprefix="$",
        yaxis_tickformat=","
    )
    
    return fig