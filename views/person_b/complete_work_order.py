from datetime import date

import mysql.connector
import streamlit as st

import db
import errors


def render():
    st.header("Complete a Work Order")

    try:
        orders = db.fetch_df(
            """SELECT WO.WO_ID, E.EQUIP_ASSET_TAG, WO.WO_DESCRIPTION, WO.WO_STATUS,
                      COUNT(WA.TECH_ID) AS NUM_TECHS
               FROM WORK_ORDER WO
               JOIN EQUIPMENT E ON E.EQUIP_ID = WO.EQUIP_ID
               LEFT JOIN WORK_ASSIGNMENT WA ON WA.WO_ID = WO.WO_ID
               WHERE NOT EXISTS (SELECT 1 FROM MAINTENANCE_RECORD MR WHERE MR.WO_ID = WO.WO_ID)
               GROUP BY WO.WO_ID, E.EQUIP_ASSET_TAG, WO.WO_DESCRIPTION, WO.WO_STATUS
               ORDER BY WO.WO_ID""")
        parts = db.fetch_df("SELECT PART_ID, PART_NUMBER, PART_NAME, PART_UNIT FROM PART ORDER BY PART_NAME")
    except mysql.connector.Error as err:
        errors.show_db_error(err)
        return

    if orders.empty:
        st.info("Every work order already has a maintenance record.")
        return

    order_labels = {
        int(r.WO_ID): f"#{r.WO_ID}  {r.EQUIP_ASSET_TAG}  {r.WO_DESCRIPTION}  ({r.WO_STATUS}, {r.NUM_TECHS} technician(s))"
        for r in orders.itertuples()
    }
    part_names = {int(r.PART_ID): f"{r.PART_NUMBER}  {r.PART_NAME}" for r in parts.itertuples()}
    part_units = {int(r.PART_ID): r.PART_UNIT for r in parts.itertuples()}

    wo_id = st.selectbox("Work order", list(order_labels), format_func=order_labels.get)
    completion_date = st.date_input("Completion date", value=date.today())
    work_performed = st.text_area("Work performed", max_chars=1000)

    part_ids = st.multiselect("Parts used (optional)", list(part_names), format_func=part_names.get)
    quantities = {}
    for part_id in part_ids:
        quantities[part_id] = st.number_input(
            f"Quantity of {part_names[part_id]} ({part_units[part_id]})",
            min_value=0.0, value=1.0, step=1.0, key=f"qty_{part_id}")

    if not st.button("Save maintenance record"):
        return
    if not work_performed.strip():
        st.warning("Please describe the work performed.")
        return

    conn = None
    try:
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO MAINTENANCE_RECORD (MAINT_COMPLETION_DATE, MAINT_WORK_PERFORMED, WO_ID)
               VALUES (%s, %s, %s)""",
            (completion_date, work_performed.strip(), wo_id),
        )
        maint_id = cur.lastrowid
        for part_id, qty in quantities.items():
            cur.execute("INSERT INTO PART_USAGE (MAINT_ID, PART_ID, USAGE_QTY) VALUES (%s, %s, %s)",
                        (maint_id, part_id, qty))
        conn.commit()
    except mysql.connector.Error as err:
        if conn is not None:
            try:
                conn.rollback()
            except mysql.connector.Error:
                pass  
        errors.show_db_error(err)
        return
    finally:
        if conn is not None:
            conn.close()

    try:
        saved = db.fetch_df("SELECT * FROM MAINTENANCE_RECORD WHERE MAINT_ID = %s", (maint_id,))
        used = db.fetch_df(
            """SELECT PU.MAINT_ID, PU.PART_ID, P.PART_NAME, PU.USAGE_QTY, P.PART_UNIT
               FROM PART_USAGE PU
               JOIN PART P ON P.PART_ID = PU.PART_ID
               WHERE PU.MAINT_ID = %s
               ORDER BY P.PART_NAME""",
            (maint_id,),
        )
        status = db.fetch_df("SELECT WO_STATUS FROM WORK_ORDER WHERE WO_ID = %s", (wo_id,))
    except mysql.connector.Error as err:
        errors.show_db_error(err)
        return

    st.success(f"Saved maintenance record #{maint_id} for work order #{wo_id} "
               f"with {len(quantities)} part(s).")
    st.write(f"Work order #{wo_id} status is now: **{status.iloc[0]['WO_STATUS']}** (set by our trigger)")
    st.dataframe(saved, hide_index=True)
    if not used.empty:
        st.dataframe(used, hide_index=True)
