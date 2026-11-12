from datetime import date

import mysql.connector
import streamlit as st

import db
import errors

PRIORITIES = ["Low", "Medium", "High"]


def render():
    st.header("Report a Problem")

    try:
        equipment = db.fetch_df(
            "SELECT EQUIP_ID, EQUIP_ASSET_TAG, EQUIP_NAME FROM EQUIPMENT ORDER BY EQUIP_ASSET_TAG")
    except mysql.connector.Error as err:
        errors.show_db_error(err)
        return

    equip_labels = {int(r.EQUIP_ID): f"{r.EQUIP_ASSET_TAG}  {r.EQUIP_NAME}" for r in equipment.itertuples()}
    equip_id = st.selectbox("Equipment", list(equip_labels), format_func=equip_labels.get)

    try:
        inspections = db.fetch_df(
            """SELECT I.INSP_ID, I.INSP_DATE, I.INSP_RESULT, E.EQUIP_ASSET_TAG
               FROM INSPECTION I
               JOIN EQUIPMENT E ON E.EQUIP_ID = I.EQUIP_ID
               ORDER BY (I.EQUIP_ID = %s) DESC, E.EQUIP_ASSET_TAG, I.INSP_DATE DESC""",
            (equip_id,),
        )
    except mysql.connector.Error as err:
        errors.show_db_error(err)
        return

    insp_labels = {None: "(no inspection)"}
    for r in inspections.itertuples():
        insp_labels[int(r.INSP_ID)] = f"#{r.INSP_ID}  {r.EQUIP_ASSET_TAG}  {r.INSP_DATE}  {r.INSP_RESULT}"

    insp_id = st.selectbox("Inspection (optional)", list(insp_labels), format_func=insp_labels.get)
    report_date = st.date_input("Report date", value=date.today())
    priority = st.selectbox("Priority", PRIORITIES)
    description = st.text_area("Description", max_chars=500)

    if not st.button("Save problem report"):
        return
    if not description.strip():
        st.warning("Please enter a description.")
        return

    try:
        new_id = db.execute(
            """INSERT INTO PROBLEM_REPORT (PROB_REPORT_DATE, PROB_DESCRIPTION, PROB_PRIORITY, EQUIP_ID, INSP_ID)
               VALUES (%s, %s, %s, %s, %s)""",
            (report_date, description.strip(), priority, equip_id, insp_id),
        )
        saved = db.fetch_df("SELECT * FROM PROBLEM_REPORT WHERE PROB_ID = %s", (new_id,))
    except mysql.connector.Error as err:
        errors.show_db_error(err)
        return

    st.success(f"Saved problem report #{new_id}.")
    st.dataframe(saved, hide_index=True)
