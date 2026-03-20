import pandas as pd

def load_data(csv):
    return pd.read_csv(csv, parse_dates=[12, 13, 34, 35])


def preprocessing(data):
    df = data.copy()

    df.fillna({'avg_lead_score': 50}, inplace=True)

    df['arr_gbp'] = df['arr_gbp'].replace(0, 1)

    df['days_to_renewal'] = (df['renewal_date'] - pd.Timestamp.today()).dt.days
    df['revenue_share_gbp'] = df['arr_gbp'] / df['arr_gbp'].sum()
    df['seats_utilisation'] = df['seats_used'] / df['seats_purchased']
    df['open_leads_quality'] = df['open_leads_count'] * df['avg_lead_score']

    df['quarterly_growth_gbp'] = (
        df['mrr_current_gbp'] - df['mrr_3m_ago_gbp']
    ) / df['mrr_3m_ago_gbp']

    df['usage_score_change'] = df['usage_score_current'] - df['usage_score_3m_ago']
    df['overdue_amount_pct_gbp'] = df['overdue_amount_gbp'] / df['arr_gbp']
    df['expansion_pipeline_pct_gbp'] = df['expansion_pipeline_gbp'] / df['arr_gbp']
    df['contraction_risk_pct_gbp'] = df['contraction_risk_gbp'] / df['arr_gbp']

    df['note_sentiment_score'] = df['note_sentiment_hint'].map({
        'Neutral': 0,
        'Positive': 1,
        'Negative': -1,
        'Mixed': 0
    })

    return df