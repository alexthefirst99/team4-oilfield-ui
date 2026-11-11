"""Screen: Equipment.

OWNER: Person A (SCOPE.md item 2). Only Person A edits this file.
Lists every equipment item with its site and type. Filter by site and status.
"""
import streamlit as st

import db

STATUSES = ["Operational", "Out of Service", "Retired"]


def render():
    st.header("Equipment")

    sites = db.fetch_df("SELECT SITE_NAME FROM SITE ORDER BY SITE_NAME")["SITE_NAME"].tolist()
    col1, col2 = st.columns(2)
    site = col1.selectbox("Site", ["All"] + sites)
    status = col2.selectbox("Status", ["All"] + STATUSES)

    sql = """
        SELECT E.EQUIP_ASSET_TAG, E.EQUIP_NAME, ET.TYPE_NAME, S.SITE_NAME,
               E.EQUIP_STATUS, E.EQUIP_INSTALL_DATE
        FROM EQUIPMENT E
        JOIN SITE S ON S.SITE_ID = E.SITE_ID
        JOIN EQUIPMENT_TYPE ET ON ET.TYPE_ID = E.TYPE_ID
        WHERE 1 = 1
    """
    params = []
    if site != "All":
        sql += " AND S.SITE_NAME = %s"
        params.append(site)
    if status != "All":
        sql += " AND E.EQUIP_STATUS = %s"
        params.append(status)
    sql += " ORDER BY S.SITE_NAME, E.EQUIP_ASSET_TAG"

    equipment = db.fetch_df(sql, params)
    st.caption(f"{len(equipment)} equipment item(s)")
    st.dataframe(equipment, hide_index=True)
