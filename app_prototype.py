import streamlit as st
import pandas as pd
from sql_tool.queries import get_all_reports
from ui.ui_tools import display_table,render_filter,filter_reports
from ui.upload import show_new_report
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="RoW Inspection Report",
    layout="wide",
)


st.title("3D Drone Viewer")

html = """
<script type="module"
    src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js">
</script>

<model-viewer
    src="drone.glb"
    camera-controls
    auto-rotate
    shadow-intensity="1"
    exposure="1"
    style="
        width: 100%;
        height: 600px;
        background: #f2f2f2;
    ">
</model-viewer>
"""

components.html(html, height=620)
components.html(html, height=320)
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


# uavids_selection,status_selection,date_selection,clearance_selection,sorting_selection,order_selection = render_filter(uav_ids)
# filtered_df = filter_reports(df,uavids_selection,status_selection,date_selection,clearance_selection,sorting_selection,order_selection)
# display_table(filtered_df)