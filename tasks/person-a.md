# Person A: screens that read data

Name: Alex Tran

Check each box when it is done. Details for each screen are in [SCOPE.md](../SCOPE.md).

**Your files** (only you edit these): `db.py` and everything in `views/person_a/`. Each screen file already has a `render()` function with a hint. Replace the `todo(...)` line with the real screen.

## Must (by Nov 16)

- [x] **1. Connection and home page.** Do this first, because every other screen needs it.
  - [x] `db.py`: write `get_connection()`, `fetch_df()`, and `execute()`. Read the login from `.streamlit/secrets.toml`. Keep the function names, because Person B's forms already use them.
  - [x] `views/person_a/home.py`: show how many rows each of the 11 tables has.
  - [ ] Push it so Person B can build on it.
  - Done when: the counts match MySQL Workbench.
- [x] **2. Equipment list** (`views/person_a/equipment.py`)
  - [x] Show each equipment item with its site name and type name.
  - [x] Filter by site and by status (Operational, Out of Service, Retired).
  - Done when: the filters give the same rows as Workbench.
- [x] **3. Work orders** (`views/person_a/work_orders.py`)
  - [x] Show each work order with its equipment asset tag and its assigned technicians.
  - [x] Filter by status (Open, In Progress, Completed, Cancelled).
  - Done when: each order shows the right technicians.
- [x] **4. Query highlights** (`views/person_a/query_highlights.py`)
  - [x] List our Phase 3 queries by name (from `sql/Team4_Queries.sql`).
  - [x] Show the SQL of the one picked, and run it.
  - Done when: the results match our Phase 3 screenshots.
- [ ] **10. README**
  - [ ] Check the "How to run" steps in the main README on both laptops and fix anything that is different.
  - Done when: Person B can start the UI by following it.

## Nice (only if there is time)

- [x] **11. Equipment history** (`views/person_a/equipment_history.py`). Pick one equipment item and show its inspections, problem reports, and completed repairs.
  - Done when: the numbers match Advanced Query 2 for that item.
