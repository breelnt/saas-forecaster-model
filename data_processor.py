import pandas as pd

def get_business_actuals():
    cust = pd.read_csv('customers.csv')
    rev = pd.read_csv('revenue.csv')
    subs = pd.read_csv('subscriptions.csv')
    
    # Standardize dates
    rev['month'] = pd.to_datetime(rev['month'])
    cust['churn_date'] = pd.to_datetime(cust['churn_date'])
    
    # 1. High Level Metrics
    latest_month_label = rev['month'].max()
    current_mrr = rev[rev['month'] == latest_month_label]['amount'].sum()
    
    # 2. Historical Trend (Momentum)
    history = rev.groupby('month')['amount'].sum().reset_index()
    history.columns = ['Month', 'Revenue']
    momentum = history['Revenue'].pct_change().tail(4).mean()

    # 3. Product Breakdown
    # Filter for currently active customers (no churn date)
    active_cust = cust[cust['churn_date'].isna()]
    
    product_stats = []
    for plan in ['Basic', 'Pro', 'Enterprise']:
        plan_data = active_cust[active_cust['plan_type'] == plan]
        product_stats.append({
            "Product": plan,
            "Customers": len(plan_data),
            "Monthly Price": plan_data['monthly_fee'].iloc[0] if not plan_data.empty else 0,
            "Annual Revenue": (plan_data['monthly_fee'].sum() * 12)
        })

    # 4. Profitability Logic (Plain English)
    avg_cac = cust['acquisition_cost'].mean()
    avg_bill = active_cust['monthly_fee'].mean()
    loss_rate = (cust['churn_date'].notna().sum() / len(cust)) / 18
    ltv = avg_bill / loss_rate if loss_rate > 0 else avg_bill * 36
    profit_score = ltv / avg_cac

    return {
        "yearly_revenue": current_mrr * 12,
        "monthly_revenue": current_mrr,
        "profit_score": profit_score,
        "cost_per_customer": avg_cac,
        "loss_rate": loss_rate,
        "products": pd.DataFrame(product_stats),
        "history": history,
        "momentum": momentum
    }