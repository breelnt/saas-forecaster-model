import pandas as pd

def get_business_actuals():
    cust = pd.read_csv('customers.csv')
    rev = pd.read_csv('revenue.csv')
    subs = pd.read_csv('subscriptions.csv')
    
    rev['month'] = pd.to_datetime(rev['month'])
    
    # Yearly Revenue (ARR)
    latest_month = rev['month'].max()
    current_monthly_revenue = rev[rev['month'] == latest_month]['amount'].sum()
    yearly_revenue = current_monthly_revenue * 12
    
    # Acquisition Cost
    avg_cost_to_get_customer = cust['acquisition_cost'].mean()
    
    # Average Sale Price
    avg_monthly_bill = subs[subs['month'] == subs['month'].max()]['monthly_fee'].mean()
    
    # Customer Loss Rate (Churn)
    total_cust = len(cust)
    lost_count = cust['churn_date'].notna().sum()
    monthly_loss_rate = (lost_count / total_cust) / 18 
    
    # Profitability Score (LTV/CAC)
    customer_lifetime_value = avg_monthly_bill / monthly_loss_rate if monthly_loss_rate > 0 else avg_monthly_bill * 36
    profit_score = customer_lifetime_value / avg_cost_to_get_customer
    
    return {
        "monthly_revenue": current_monthly_revenue,
        "yearly_revenue": yearly_revenue,
        "cost_per_customer": avg_cost_to_get_customer,
        "profit_score": profit_score,
        "loss_rate": monthly_loss_rate,
        "avg_bill": avg_monthly_bill,
        "history": rev.groupby('month')['amount'].sum().reset_index()
    }