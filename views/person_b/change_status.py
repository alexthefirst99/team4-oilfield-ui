import mysql.connector
import streamlit as st

import db
import errors

NEXT_STATUSES = {
    "Open": ["In Progress", "Cancelled"],
    "In Progress": ["Open", "Cancelled"],
}


def render():
    st.header("Change Work Order Status")

    try:
        orders = db.fetch_df(
            """SELECT WO.WO_ID, E.EQUIP_ASSET_TAG, WO.WO_DESCRIPTION, WO.WO_STATUS,
                      COUNT(WA.TECH_ID) AS NUM_TECHS
               FROM WORK_ORDER WO
               JOIN EQUIPMENT E ON E.EQUIP_ID = WO.EQUIP_ID
               LEFT JOIN WORK_ASSIGNMENT WA ON WA.WO_ID = WO.WO_ID
               WHERE WO.WO_STATUS IN ('Open', 'In Progress')
               GROUP BY WO.WO_ID, E.EQUIP_ASSET_TAG, WO.WO_DESCRIPTION, WO.WO_STATUS
               ORDER BY WO.WO_ID""")
    except mysql.connector.Error as err:
        errors.show_db_error(err)
        return

    if orders.empty:
        st.info("There are no Open or In Progress work orders.")
        return

    order_labels = {
        int(r.WO_ID): f"#{r.WO_ID}  {r.EQUIP_ASSET_TAG}  {r.WO_DESCRIPTION}  ({r.WO_STATUS}, {r.NUM_TECHS} technician(s))"
        for r in orders.itertuples()
    }
    current = {int(r.WO_ID): r.WO_STATUS for r in orders.itertuples()}

    wo_id = st.selectbox("Work order", list(order_labels), format_func=order_labels.get)
    new_status = st.selectbox(f"New status (now {current[wo_id]})", NEXT_STATUSES[current[wo_id]])

    if not st.button("Save status"):
        return

    try:
        db.execute("UPDATE WORK_ORDER SET WO_STATUS = %s WHERE WO_ID = %s", (new_status, wo_id))
        saved = db.fetch_df("SELECT * FROM WORK_ORDER WHERE WO_ID = %s", (wo_id,))
    except mysql.connector.Error as err:
        errors.show_db_error(err)
        return

    st.success(f"Work order #{wo_id} is now {new_status}.")
    st.dataframe(saved, hide_index=True)
