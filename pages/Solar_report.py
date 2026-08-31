import streamlit as st
import pandas as pd

from sql_tool.queries import get_all_reports
from ui.ui_tools import (
    display_table,
    render_filter,
    filter_reports,
)


st.set_page_config(
    page_title="Reports",
    page_icon="📋",
    layout="wide",
)

st.title("📋 Solar Reports")


# --------------------------------------------------
# Read data from database
# --------------------------------------------------

db_report = get_all_reports()
df = pd.DataFrame(db_report)


# --------------------------------------------------
# Get UAV IDs
# --------------------------------------------------

if not df.empty and "uav_id" in df.columns:

    uav_ids = sorted(
        df["uav_id"]
        .dropna()
        .unique()
        .tolist()
    )

else:

    uav_ids = []


# --------------------------------------------------
# Filters
# --------------------------------------------------

(
    uavids_selection,
    status_selection,
    date_selection,
    clearance_selection,
    sorting_selection,
    order_selection,
) = render_filter(uav_ids)
