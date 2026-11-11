"""Screen: Equipment history.

OWNER: Person A (SCOPE.md item 11, nice to have). Only Person A edits this file.
Pick one equipment item and show its inspections, problem reports, and repairs.
"""
import streamlit as st

import db


def render():
    st.header("Equipment history")

    equipment = db.fetch_df(
        "SELECT EQUIP_ID, CONCAT(EQUIP_ASSET_TAG, ' - ', EQUIP_NAME) AS LABEL "
        "FROM EQUIPMENT ORDER BY EQUIP_ASSET_TAG")
    label = st.selectbox("Equipment", equipment["LABEL"])
    equip_id = int(equipment.loc[equipment["LABEL"] == label, "EQUIP_ID"].iloc[0])

    inspections = db.fetch_df("""
        SELECT I.INSP_DATE, I.INSP_RESULT, I.INSP_NOTES,
               CONCAT(T.TECH_FNAME, ' ', T.TECH_LNAME) AS TECHNICIAN
        FROM INSPECTION I
        JOIN TECHNICIAN T ON T.TECH_ID = I.TECH_ID
        WHERE I.EQUIP_ID = %s
        ORDER BY I.INSP_DATE""", (equip_id,))
    problems = db.fetch_df("""
        SELECT PROB_REPORT_DATE, PROB_PRIORITY, PROB_DESCRIPTION
        FROM PROBLEM_REPORT
        WHERE EQUIP_ID = %s
        ORDER BY PROB_REPORT_DATE""", (equip_id,))
    repairs = db.fetch_df("""
        SELECT WO.WO_ID, WO.WO_DESCRIPTION, MR.MAINT_COMPLETION_DATE, MR.MAINT_WORK_PERFORMED
        FROM WORK_ORDER WO
        JOIN MAINTENANCE_RECORD MR ON MR.WO_ID = WO.WO_ID
        WHERE WO.EQUIP_ID = %s
        ORDER BY MR.MAINT_COMPLETION_DATE""", (equip_id,))

    col1, col2, col3 = st.columns(3)
    col1.metric("Inspections", len(inspections))
    col2.metric("Problem reports", len(problems))
    col3.metric("Completed repairs", len(repairs))

    for title, table in [("Inspections", inspections), ("Problem reports", problems),
                         ("Completed repairs", repairs)]:
        st.subheader(title)
        if table.empty:
            st.write("None")
        else:
            st.dataframe(table, hide_index=True)
