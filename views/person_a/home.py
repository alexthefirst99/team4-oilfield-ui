"""Screen: Home.

OWNER: Person A (SCOPE.md item 1). Only Person A edits this file.
Connects to MySQL and shows how many rows each of the 11 tables has.
"""
import mysql.connector
import streamlit as st

import db

TABLES = ["SITE", "EQUIPMENT_TYPE", "EQUIPMENT", "TECHNICIAN", "INSPECTION", "PROBLEM_REPORT",
          "WORK_ORDER", "WORK_ASSIGNMENT", "MAINTENANCE_RECORD", "PART", "PART_USAGE"]


def render():
    st.header("Home")
    st.write("Oilfield Equipment Maintenance Management System (Team 4)")

    # One query that counts the rows of every table
    sql = " UNION ALL ".join(f"SELECT '{t}' AS TABLE_NAME, COUNT(*) AS NUM_ROWS FROM {t}" for t in TABLES)
    try:
        counts = db.fetch_df(sql)
    except mysql.connector.Error as err:
        st.error(f"Could not connect to MySQL: {err}")
        st.write("Check that MySQL is running and that .streamlit/secrets.toml has the right login.")
        return

    st.success(f"Connected to the {st.secrets['mysql']['database']} database.")
    st.dataframe(counts, hide_index=True)
