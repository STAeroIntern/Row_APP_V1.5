from sql_tool.connection import get_connection


def get_all_reports():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            filename,
            uav_id,
            inspection_datetime,
            safe_clearance_distance,
            status
        FROM row_database.reports
    """)

    reports = cursor.fetchall()

    cursor.close()
    conn.close()

    return reports

def get_reports_status_by_ids(report_ids):

    if not report_ids:
        return []

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    placeholders = ", ".join(
        ["%s"] * len(report_ids)
    )

    query = f"""
        SELECT
            id,
            status
        FROM row_database.reports
        WHERE id IN ({placeholders})
    """

    cursor.execute(
        query,
        tuple(report_ids),
    )

    reports = cursor.fetchall()

    cursor.close()
    conn.close()

    return reports


def get_report_by_id(report_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            r.id,
            r.filename,
            r.uav_id,
            r.inspection_datetime,
            r.safe_clearance_distance,
            r.status,
            rf.report_path,
            rf.video_path,
            rf.debug_path
        FROM row_database.reports AS r
        LEFT JOIN row_database.report_files AS rf
            ON r.id = rf.report_id
        WHERE r.id = %s
        """,
        (report_id,),
    )

    report = cursor.fetchone()

    cursor.close()
    conn.close()

    return report

def get_all_dag_run_id(report_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT dag_run_id
        FROM row_database.reports
        WHERE id = %s
        """,
        (report_id,),
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return result["dag_run_id"]

    return None

def get_all_filename(report_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT filename
        FROM row_database.reports
        WHERE id = %s
        """,
        (report_id,),
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return result["filename"]

    return None


def delete_from_database(report_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM row_database.report_files
        WHERE report_id = %s
        """,
        (report_id,),
    )

    conn.commit()

    cursor.execute(
            """
            DELETE FROM row_database.reports
            WHERE id = %s
            """,
            (report_id,),
        )
    conn.commit()

    cursor.close()
    conn.close()


def create_report(
    filename,
    uav_id,
    inspection_datetime,
    safe_clearance,
    status,
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO row_database.reports (
            filename,
            uav_id,
            inspection_datetime,
            safe_clearance_distance,
            status
        )
        VALUES (%s, %s, %s, %s, %s)
    """, (
        filename,
        uav_id,
        inspection_datetime,
        safe_clearance,
        status,
    ))

    conn.commit()

    report_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return report_id

def has_processing_report():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT EXISTS (
            SELECT 1
            FROM row_database.reports
            WHERE status = 'Processing'
        )
    """)

    result = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return bool(result)