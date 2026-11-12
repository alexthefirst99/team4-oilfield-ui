"""Screen: Home.

OWNER: Person A (SCOPE.md item 1). Only Person A edits this file.
Connects to MySQL and gives a plain-language overview: key numbers, two charts,
work orders waiting for a technician, and how much of each kind of record we keep.
"""
import mysql.connector
import pandas as pd
import streamlit as st

import db
from views.person_a.display import show_table

# Each table in plain words, in the order a user thinks about them
RECORDS = [("SITE", "Sites"), ("EQUIPMENT_TYPE", "Equipment types"), ("EQUIPMENT", "Equipment"),
           ("TECHNICIAN", "Technicians"), ("INSPECTION", "Inspections"), ("PROBLEM_REPORT", "Problem reports"),
           ("WORK_ORDER", "Work orders"), ("WORK_ASSIGNMENT", "Technician assignments"),
           ("MAINTENANCE_RECORD", "Completed repairs"), ("PART", "Parts"), ("PART_USAGE", "Parts used in repairs")]
ORANGE = "#C2410C"


def render():
    st.header("Home")
    st.write("Keep track of equipment, inspections, problems, and repairs across all of our field sites.")

    try:
        numbers = db.fetch_df("""
            SELECT (SELECT COUNT(*) FROM EQUIPMENT) AS equipment,
                   (SELECT COUNT(*) FROM WORK_ORDER WHERE WO_STATUS IN ('Open', 'In Progress')) AS active_orders,
                   (SELECT COUNT(*) FROM EQUIPMENT WHERE EQUIP_STATUS = 'Out of Service') AS out_of_service,
                   (SELECT COUNT(*) FROM MAINTENANCE_RECORD) AS repairs""").iloc[0]
        by_status = db.fetch_df(
            "SELECT WO_STATUS AS Status, COUNT(*) AS `Work orders` FROM WORK_ORDER GROUP BY WO_STATUS")
        by_site = db.fetch_df("""
            SELECT S.SITE_NAME AS Site, COUNT(E.EQUIP_ID) AS Equipment
            FROM SITE S LEFT JOIN EQUIPMENT E ON E.SITE_ID = S.SITE_ID
            GROUP BY S.SITE_NAME""")
        waiting = db.fetch_df("""
            SELECT WO.WO_ID, WO.WO_DESCRIPTION, E.EQUIP_ASSET_TAG, WO.WO_DUE_DATE
            FROM WORK_ORDER WO
            JOIN EQUIPMENT E ON E.EQUIP_ID = WO.EQUIP_ID
            WHERE WO.WO_STATUS = 'Open'
              AND NOT EXISTS (SELECT 1 FROM WORK_ASSIGNMENT WA WHERE WA.WO_ID = WO.WO_ID)
            ORDER BY WO.WO_DUE_DATE""")
        # One query that counts the records of every table
        counts = db.fetch_df(" UNION ALL ".join(
            f"SELECT '{table}' AS TABLE_NAME, COUNT(*) AS NUM_ROWS FROM {table}" for table, _ in RECORDS))
    except mysql.connector.Error as err:
        st.error("The app cannot reach the maintenance database right now.")
        st.caption(f"Check that MySQL is running and that .streamlit/secrets.toml has the right login. ({err})")
        return

    st.success("Connected to the maintenance database.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Equipment items", int(numbers["equipment"]))
    col2.metric("Work orders in progress or open", int(numbers["active_orders"]))
    col3.metric("Equipment out of service", int(numbers["out_of_service"]))
    col4.metric("Repairs completed", int(numbers["repairs"]))

    left, right = st.columns(2)
    with left:
        st.subheader("Work orders by status")
        st.bar_chart(by_status, x="Status", y="Work orders", color=ORANGE, horizontal=True, height=220)
    with right:
        st.subheader("Equipment at each site")
        st.bar_chart(by_site, x="Site", y="Equipment", color=ORANGE, horizontal=True, height=220)

    st.subheader("Waiting for a technician")
    if waiting.empty:
        st.write("Every open work order has a technician.")
    else:
        st.caption("These open work orders cannot start until someone is assigned (rule BR15).")
        show_table(waiting)

    st.subheader("What's in the system")
    names = dict(RECORDS)
    summary = pd.DataFrame({"Record": counts["TABLE_NAME"].map(names), "How many": counts["NUM_ROWS"]})
    show_table(summary)
