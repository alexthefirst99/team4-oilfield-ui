"""Screen: Work orders.

OWNER: Person A (SCOPE.md item 3). Only Person A edits this file.
Lists work orders with their equipment and assigned technicians. Filter by status.
"""
import streamlit as st

import db
from views.person_a.display import show_table

STATUSES = ["Open", "In Progress", "Completed", "Cancelled"]


def render():
    st.header("Work Orders")
    st.write("Every job on our equipment. **Corrective** means fixing a reported problem. "
             "**Routine** means regular service, like an oil change.")

    status = st.selectbox("Show", ["All"] + STATUSES)

    # LEFT JOIN so work orders with no technician still show up
    sql = """
        SELECT WO.WO_ID, WO.WO_DESCRIPTION, WO.WO_TYPE, WO.WO_STATUS,
               WO.WO_CREATED_DATE, WO.WO_DUE_DATE, E.EQUIP_ASSET_TAG,
               GROUP_CONCAT(T.TECH_FNAME ORDER BY T.TECH_FNAME SEPARATOR ', ') AS TECHNICIANS
        FROM WORK_ORDER WO
        JOIN EQUIPMENT E ON E.EQUIP_ID = WO.EQUIP_ID
        LEFT JOIN WORK_ASSIGNMENT WA ON WA.WO_ID = WO.WO_ID
        LEFT JOIN TECHNICIAN T ON T.TECH_ID = WA.TECH_ID
    """
    params = []
    if status != "All":
        sql += " WHERE WO.WO_STATUS = %s"
        params.append(status)
    sql += """
        GROUP BY WO.WO_ID, WO.WO_DESCRIPTION, WO.WO_TYPE, WO.WO_STATUS,
                 WO.WO_CREATED_DATE, WO.WO_DUE_DATE, E.EQUIP_ASSET_TAG
        ORDER BY WO.WO_ID
    """

    orders = db.fetch_df(sql, params)
    orders["TECHNICIANS"] = orders["TECHNICIANS"].fillna("Not assigned yet")
    st.caption(f"{len(orders)} work order(s)")
    show_table(orders)
