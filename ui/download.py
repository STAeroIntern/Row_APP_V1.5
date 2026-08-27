import io
import os
import streamlit as st
import yaml
import zipfile


with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

OUTPUT_DIR = config["directories"]["output"]


@st.dialog("Download Reports")
def download_dialog(selected_reports):

    st.write(
        f"Download options for **{len(selected_reports)} report(s)**."
    )

    st.write("**Selected files:**")

    for report in selected_reports:
        st.write(f"- {report['filename']}")

    download_type = st.radio(
        "What would you like to download?",
        [
            "Videos",
            "HTML Reports",
            "Videos + HTML Reports",
        ],
        key="download_type",
    )

    # ==================================================
    # SINGLE REPORT
    # ==================================================

    if len(selected_reports) == 1:

        report = selected_reports[0]
        filename = report["filename"]

        # ------------------------------------------
        # Single Video
        # ------------------------------------------

        if download_type == "Videos":

            video_path = os.path.join(
                OUTPUT_DIR,
                filename + ".mp4",
            )

            if os.path.exists(video_path):

                with open(video_path, "rb") as f:
                    video_bytes = f.read()

                st.download_button(
                    label="⬇ Download Video",
                    data=video_bytes,
                    file_name=filename + ".mp4",
                    mime="video/mp4",
                    use_container_width=True,
                    type="primary",
                    key="download_single_video",
                )

            else:

                st.warning(
                    f"Video not found: {filename}.mp4"
                )

        # ------------------------------------------
        # Single HTML
        # ------------------------------------------

        elif download_type == "HTML Reports":

            html_path = os.path.join(
                OUTPUT_DIR,
                filename + ".html",
            )

            if os.path.exists(html_path):

                with open(html_path, "rb") as f:
                    html_bytes = f.read()

                st.download_button(
                    label="⬇ Download HTML Report",
                    data=html_bytes,
                    file_name=filename + ".html",
                    mime="text/html",
                    use_container_width=True,
                    type="primary",
                    key="download_single_html",
                )

            else:

                st.warning(
                    f"HTML report not found: {filename}.html"
                )

        # ------------------------------------------
        # Single Report - Video + HTML
        # ------------------------------------------

        else:

            zip_buffer = io.BytesIO()

            missing_files = []

            with zipfile.ZipFile(
                zip_buffer,
                mode="w",
                compression=zipfile.ZIP_DEFLATED,
            ) as zip_file:

                video_path = os.path.join(
                    OUTPUT_DIR,
                    filename + ".mp4",
                )

                html_path = os.path.join(
                    OUTPUT_DIR,
                    filename + ".html",
                )

                if os.path.exists(video_path):

                    zip_file.write(
                        video_path,
                        arcname=filename + ".mp4",
                    )

                else:

                    missing_files.append(
                        filename + ".mp4"
                    )

                if os.path.exists(html_path):

                    zip_file.write(
                        html_path,
                        arcname=filename + ".html",
                    )

                else:

                    missing_files.append(
                        filename + ".html"
                    )

            zip_buffer.seek(0)

            if missing_files:

                st.warning(
                    "The following files could not be found:\n\n"
                    + "\n".join(
                        f"- {f}"
                        for f in missing_files
                    )
                )

            st.download_button(
                label="⬇ Download Report",
                data=zip_buffer,
                file_name=filename + ".zip",
                mime="application/zip",
                use_container_width=True,
                type="primary",
                key="download_single_both",
            )

        return

    # ==================================================
    # MULTIPLE REPORTS
    # ==================================================

    zip_buffer = io.BytesIO()

    missing_files = []

    with zipfile.ZipFile(
        zip_buffer,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
    ) as zip_file:

        for report in selected_reports:

            filename = report["filename"]

            # ------------------------------------------
            # Videos
            # ------------------------------------------

            if download_type in [
                "Videos",
                "Videos + HTML Reports",
            ]:

                video_path = os.path.join(
                    OUTPUT_DIR,
                    filename + ".mp4",
                )

                if os.path.exists(video_path):

                    zip_file.write(
                        video_path,
                        arcname=filename + ".mp4",
                    )

                else:

                    missing_files.append(
                        filename + ".mp4"
                    )

            # ------------------------------------------
            # HTML
            # ------------------------------------------

            if download_type in [
                "HTML Reports",
                "Videos + HTML Reports",
            ]:

                html_path = os.path.join(
                    OUTPUT_DIR,
                    filename + ".html",
                )

                if os.path.exists(html_path):

                    zip_file.write(
                        html_path,
                        arcname=filename + ".html",
                    )

                else:

                    missing_files.append(
                        filename + ".html"
                    )

    # ------------------------------------------
    # Missing files
    # ------------------------------------------

    if missing_files:

        st.warning(
            "The following files could not be found:\n\n"
            + "\n".join(
                f"- {f}"
                for f in missing_files
            )
        )

    # ------------------------------------------
    # Download ZIP
    # ------------------------------------------

    zip_buffer.seek(0)

    if download_type == "Videos":

        zip_filename = "videos.zip"

    elif download_type == "HTML Reports":

        zip_filename = "html_reports.zip"

    else:

        zip_filename = "reports.zip"

    st.download_button(
        label=f"⬇ Download {zip_filename}",
        data=zip_buffer,
        file_name=zip_filename,
        mime="application/zip",
        use_container_width=True,
        type="primary",
        key="download_multiple",
    )