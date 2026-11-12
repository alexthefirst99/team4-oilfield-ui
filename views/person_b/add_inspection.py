from datetime import date

import mysql.connector
import streamlit as st

import db
import errors

RESULTS = ["Pass", "Needs Maintenance", "Fail"]


def render():
    st.header("Add an Inspection")

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
    tech_id = st.selectbox("Technician", list(tech_labels), format_func=tech_labels.get)
    insp_date = st.date_input("Inspection date", value=date.today())
    result = st.selectbox("Result", RESULTS)
    notes = st.text_area("Notes (optional)", max_chars=500)

    if not st.button("Save inspection"):
        return

    try:
        new_id = db.execute(
            """INSERT INTO INSPECTION (INSP_DATE, INSP_RESULT, INSP_NOTES, EQUIP_ID, TECH_ID)
               VALUES (%s, %s, %s, %s, %s)""",
            (insp_date, result, notes.strip() or None, equip_id, tech_id),
        )
        saved = db.fetch_df("SELECT * FROM INSPECTION WHERE INSP_ID = %s", (new_id,))
    except mysql.connector.Error as err:
        errors.show_db_error(err)
        return

    st.success(f"Saved inspection #{new_id}.")
    st.dataframe(saved, hide_index=True)
