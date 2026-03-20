import streamlit as st
import pandas as pd

from auth import require_auth
from scoring import scorecard_config

require_auth()

st.title("⚙️ Scoring Model")

config_df = pd.DataFrame(
    scorecard_config,
    columns=[
        "feature",
        "type",
        "reference",
        "threshold",
        "ascending",
        "weight",
        "na_handling",
        "description"
    ]
)

st.dataframe(config_df, use_container_width=True)