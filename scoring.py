import numpy as np

scorecard_config = [
    ('days_to_renewal', 'risk', 'absolute', 30, True, 1, 0, 'days to renewal < 30 days'),
    ('latest_nps', 'risk', 'relative', 0.25, True, 1, 'ignore', 'low NPS score'),
    ('open_tickets_count', 'risk', 'relative', 0.25, False, 1, 0, 'high ticket volume'),
    ('urgent_open_tickets_count', 'risk', 'absolute', 3, False, 1, 0, 'urgent tickets > 3'),
    ('sla_breaches_90d', 'risk', 'absolute', 3, False, 1, 0, 'SLA breaches ≥ 3'),
    ('avg_csat_90d', 'risk', 'relative', 0.25, True, 1, 0, 'low CSAT'),
    ('quarterly_growth_gbp', 'risk', 'absolute', 0, True, 1, 'ignore', 'negative growth'),
    ('usage_score_change', 'risk', 'absolute', 0, True, 1, 'ignore', 'declining usage'),
    ('overdue_amount_pct_gbp', 'risk', 'absolute', 0.05, False, 1, 0, 'overdue > 5% ARR'),
    ('contraction_risk_pct_gbp', 'risk', 'relative', 0.25, False, 1, 0, 'high contraction risk'),
    ('note_sentiment_score', 'risk', 'absolute', -1, True, 1, 0, 'negative sentiment'),

    ('seats_utilisation', 'opp', 'absolute', 0.8, False, 1, 0, 'high utilisation'),
    ('open_leads_quality', 'opp', 'relative', 0.25, False, 1, 0, 'strong leads'),
    ('expansion_pipeline_gbp', 'opp', 'relative', 0.25, False, 1, 0, 'large pipeline'),
    ('expansion_pipeline_pct_gbp', 'opp', 'relative', 0.25, False, 1, 0, 'pipeline vs ARR high'),
    ('note_sentiment_score', 'opp', 'absolute', 1, True, 1, 0, 'positive sentiment')
]


def add_scorecard(data, config):
    df = data.copy()
    risk_idx = []
    opp_idx = []

    df["risk_reasons"] = [[] for _ in range(len(df))]
    df["opp_reasons"] = [[] for _ in range(len(df))]

    for col, typ, ref, val, asc, weight, na, exp in config:

        if na != 'ignore':
            df.fillna({col: na}, inplace=True)

        df[col + '_rank'] = df[col].rank(pct=True, ascending=asc)

        if ref == 'absolute':
            condition = df[col] <= val if asc else df[col] >= val
        else:
            condition = df[col + '_rank'] <= val

        df[col + '_' + typ + '_flag'] = np.where(condition, weight, 0)

        for i in df[condition].index:
            if typ == 'risk':
                df.at[i, "risk_reasons"].append(exp)
            else:
                df.at[i, "opp_reasons"].append(exp)

        if typ == 'risk':
            risk_idx.append(col + '_' + typ + '_flag')
        else:
            opp_idx.append(col + '_' + typ + '_flag')

    df['risk_score'] = df[risk_idx].sum(axis=1)
    df['opp_score'] = df[opp_idx].sum(axis=1)

    return df