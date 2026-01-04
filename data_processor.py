import pandas as pd

def get_integrated_metrics():
    # Load Datasets
    cust = pd.read_csv('customers.csv')
    rev = pd.read_csv('revenue.csv')
    subs = pd.read_csv('subscriptions.csv')

    # 1. CALCULATE THE 'NATURAL TREND' (Historical Momentum)
    # We look at the actual revenue history to find the average growth velocity
    history_df = rev.groupby('month')['amount'].sum().reset_index()
    history_df.columns = ['Month', 'Revenue']
    history_df['growth'] = history_df['Revenue'].pct_change()
    
    # Natural growth rate (avg of last 6 months)
    organic_momentum = history_df['growth'].tail(6).mean()

    # 2. CALCULATE UNIT ECONOMIC DNA (Predictive Inputs)
    # This establishes the starting point for the simulation
    latest_mrr = history_df.iloc[-1]['Revenue']
    avg_cac = cust['acquisition_cost'].mean()
    avg_arpu = subs[subs['month'] == subs['month'].max()]['monthly_fee'].mean()
    
    return {
        "history_df": history_df,
        "organic_momentum": organic_momentum,
        "current_mrr": latest_mrr,
        "avg_cac": avg_cac,
        "avg_arpu": avg_arpu,
        "base_churn": (cust['churn_date'].notna().sum() / len(cust)) / 18
    }