from datetime import date

import mysql.connector
import streamlit as st

import db
import errors

TYPES = ["Routine", "Corrective"]


def render():
    st.header("Create a Work Order")

    try:
        equipment = db.fetch_df(
            "SELECT EQUIP_ID, EQUIP_ASSET_TAG, EQUIP_NAME FROM EQUIPMENT ORDER BY EQUIP_ASSET_TAG")
        techs = db.fetch_df(
            "SELECT TECH_ID, TECH_FNAME, TECH_LNAME FROM TECHNICIAN ORDER BY TECH_LNAME, TECH_FNAME")
    except mysql.connector.Error as err:
        errors.show_db_error(err)
        return

    equip_labels = {int(r.EQUIP_ID): f"{r.EQUIP_ASSET_TAG}  {r.EQUIP_NAME}" for r in equipment.itertuples()}
    tech_labels = {int(r.TECH_ID): f"{r.TECH_FNAME} {r.TECH_LNAME}" for r in techs.itertuples()}

    equip_id = st.selectbox("Equipment", list(equip_labels), format_func=equip_labels.get)
    wo_type = st.selectbox("Type", TYPES)

    try:
        problems = db.fetch_df(
            """SELECT P.PROB_ID, P.PROB_DESCRIPTION, P.PROB_PRIORITY, E.EQUIP_ASSET_TAG
               FROM PROBLEM_REPORT P
               JOIN EQUIPMENT E ON E.EQUIP_ID = P.EQUIP_ID
               ORDER BY (P.EQUIP_ID = %s) DESC, E.EQUIP_ASSET_TAG, P.PROB_ID""",
            (equip_id,),
        )
    except mysql.connector.Error as err:
        errors.show_db_error(err)
        return

    prob_labels = {None: "(no problem report)"}
    for r in problems.itertuples():
        prob_labels[int(r.PROB_ID)] = f"#{r.PROB_ID}  {r.EQUIP_ASSET_TAG}  {r.PROB_DESCRIPTION} ({r.PROB_PRIORITY})"

    prob_id = st.selectbox("Problem report (Corrective only)", list(prob_labels), format_func=prob_labels.get)
    description = st.text_area("Description", max_chars=500)
    created_date = st.date_input("Created date", value=date.today())
    due_date = None
    if st.checkbox("Set a due date"):
        due_date = st.date_input("Due date", value=created_date)

    tech_ids = st.multiselect("Technicians", list(tech_labels), format_func=tech_labels.get)
    if not tech_ids:
        st.caption("No technician assigned. The order can be saved, but BR15 will block "
                   "In Progress or completion until someone is assigned.")

    if not st.button("Save work order"):
        return
    if not description.strip():
        st.warning("Please enter a description.")
        return

    conn = None
    try:
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO WORK_ORDER (WO_DESCRIPTION, WO_TYPE, WO_CREATED_DATE, WO_DUE_DATE, EQUIP_ID, PROB_ID)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (description.strip(), wo_type, created_date, due_date, equip_id, prob_id),
        )
        wo_id = cur.lastrowid
        for tech_id in tech_ids:
            cur.execute("INSERT INTO WORK_ASSIGNMENT (WO_ID, TECH_ID) VALUES (%s, %s)", (wo_id, tech_id))
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
        saved = db.fetch_df("SELECT * FROM WORK_ORDER WHERE WO_ID = %s", (wo_id,))
        assigned = db.fetch_df(
            """SELECT WA.WO_ID, WA.TECH_ID, CONCAT(T.TECH_FNAME, ' ', T.TECH_LNAME) AS TECHNICIAN
               FROM WORK_ASSIGNMENT WA
               JOIN TECHNICIAN T ON T.TECH_ID = WA.TECH_ID
               WHERE WA.WO_ID = %s
               ORDER BY T.TECH_LNAME""",
            (wo_id,),
        )
    except mysql.connector.Error as err:
        errors.show_db_error(err)
        return

    st.success(f"Saved work order #{wo_id} with {len(tech_ids)} technician(s).")
    st.dataframe(saved, hide_index=True)
    st.dataframe(assigned, hide_index=True)
