import streamlit as st
import pandas as pd
from sql_tool.queries import get_all_reports
from ui.ui_tools import display_table,render_filter,filter_reports
from ui.upload import show_new_report


st.set_page_config(
    page_title="RoW Inspection Report",
    layout="wide",
)
st.markdown("""
<style>
/* Hide Deploy button */
[data-testid="stAppDeployButton"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)
st.title("Row Inspection Report")

# Read the data from the database
db_report = get_all_reports()
df = pd.DataFrame(db_report)

#Initialise popover state
if "popover_open" not in st.session_state:
    st.session_state.popover_open = False
    
if "cancel" not in st.session_state:
    st.session_state.confirm_cancel = False

#Define the list of features
if not df.empty and "uav_id" in df.columns:

    uav_ids = sorted(
        df["uav_id"]
        .dropna()
        .unique()
        .tolist()
    )

else:

    uav_ids = []

show_new_report()
uavids_selection,status_selection,date_selection,clearance_selection,sorting_selection,order_selection = render_filter(uav_ids)
filtered_df = filter_reports(df,uavids_selection,status_selection,date_selection,clearance_selection,sorting_selection,order_selection)
display_table(filtered_df)