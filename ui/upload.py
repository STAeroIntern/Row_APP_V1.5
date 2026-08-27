import os
import uuid
from datetime import timezone

import streamlit as st
import yaml

from sql_tool.queries import (
    has_processing_report,
    create_report,
)
from services.report_service import (
    add_files_to_input,
    make_filename,
)


with open("config.yml", "r") as f:
    config = yaml.safe_load(f)





# ==================================================
# UPLOAD DIALOG
# ==================================================

@st.dialog("New Inspection Report", width="large")
def new_report_dialog():

    # --------------------------------------------------
    # Form key
    # --------------------------------------------------

    if "form_key" not in st.session_state:
        st.session_state.form_key = 0

    fk = st.session_state.form_key

    # --------------------------------------------------
    # Upload files
    # --------------------------------------------------

    st.write("### Inspection Files")

    col1, col2 = st.columns(2)

    with col1:

        uploaded_video = st.file_uploader(
            "Choose a MP4 file",
            type=["mp4"],
            key=f"video_{fk}",
        )

    with col2:

        uploaded_srt = st.file_uploader(
            "Choose a SRT file",
            type=["srt"],
            key=f"srt_{fk}",
        )

    # --------------------------------------------------
    # Inspection information
    # --------------------------------------------------

    st.write("### Inspection Information")

    col1, col2 = st.columns(2)

    with col1:

        selected_id = st.text_input(
            "UAV ID",
            key=f"uav_{fk}",
        )


        st.markdown("""
        <style>
        /* Hide +/- buttons in st.number_input */
        div[data-testid="stNumberInput"] button {
            display: none !important;
        }
        </style>
        """, unsafe_allow_html=True)

        safe_clearance = st.number_input(
            "Safe Clearance Distance (m)",
            min_value = 0,
            max_value = 200,
            value=None,
            key=f"sc_{fk}",
        )
                        

    with col2:

        inspection_dt = st.datetime_input(
            "Inspection Date Time",
            value=None,
            key=f"dt_{fk}",
        )

    st.divider()

    # --------------------------------------------------
    # Buttons
    # --------------------------------------------------

    col1, col2 = st.columns(2)

    cancel = col1.button(
        "Cancel",
        key=f"cancel_{fk}",
        use_container_width=True,
    )

    start = col2.button(
        "Start Processing",
        key=f"start_{fk}",
        use_container_width=True,
        type="primary",
    )

    # ==================================================
    # CANCEL
    # ==================================================

    if cancel:

        st.session_state.form_key += 1

        st.rerun()

    # ==================================================
    # START PROCESSING
    # ==================================================

    if start:

        # --------------------------------------------------
        # Validation
        # --------------------------------------------------

        if uploaded_video is None:

            st.error(
                "Please upload an MP4 file."
            )
            return

        if uploaded_srt is None:

            st.error(
                "Please upload an SRT file."
            )
            return

        if not selected_id.strip():

            st.error(
                "Please enter a UAV ID."
            )
            return

        if safe_clearance is None:

            st.error(
                "Please enter the Safe Clearance Distance."
            )
            return

        if inspection_dt is None:

            st.error(
                "Please select an inspection date/time."
            )
            return

        # --------------------------------------------------
        # Determine status
        # --------------------------------------------------

        processing_exist = has_processing_report()

        if processing_exist:
            status = "Queued"
        else:
            status = "Processing"

        # --------------------------------------------------
        # Generate filename
        # --------------------------------------------------

        inspection_dt_utc = inspection_dt.replace(
            tzinfo=timezone.utc
        )

        filename = make_filename(
            selected_id,
            inspection_dt_utc,
            safe_clearance,
        )

        # --------------------------------------------------
        # Add files to input
        # --------------------------------------------------

        add_files_to_input(
            config["directories"]["input"],
            [
                uploaded_video,
                uploaded_srt,
            ],
            filename,
        )

        # --------------------------------------------------
        # Create database record
        # --------------------------------------------------

        report_db_id = create_report(
            filename=filename,
            uav_id=selected_id,
            inspection_datetime=inspection_dt,
            safe_clearance=safe_clearance,
            status=status,
        )

        # --------------------------------------------------
        # Save files
        # --------------------------------------------------

        DEST_DIR = "/data/EGAT/inspections/row"

        os.makedirs(
            DEST_DIR,
            exist_ok=True,
        )

        video_path = os.path.join(
            DEST_DIR,
            f"{filename}.mp4",
        )

        srt_path = os.path.join(
            DEST_DIR,
            f"{filename}.srt",
        )

        with open(video_path, "wb") as f:

            f.write(
                uploaded_video.getvalue()
            )

        with open(srt_path, "wb") as f:

            f.write(
                uploaded_srt.getvalue()
            )

        # --------------------------------------------------
        # Create Dropbox trigger
        # --------------------------------------------------

        dropbox_path = os.path.join(
            DEST_DIR,
            f"{filename}.dropbox",
        )

        with open(dropbox_path, "w"):
            pass

        # --------------------------------------------------
        # Reset form
        # --------------------------------------------------

        st.session_state.form_key += 1

        st.success(
            f"Report '{filename}' created."
        )

        st.rerun()


# ==================================================
# MAIN BUTTON
# ==================================================

def show_new_report():

    if "form_key" not in st.session_state:
        st.session_state.form_key = 0

    if st.button(
        "➕ New Report",
        type="primary",
        use_container_width=True,
    ):

        new_report_dialog()