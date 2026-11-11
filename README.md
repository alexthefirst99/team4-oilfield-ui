# Team 4: Oilfield Equipment Maintenance UI

A simple frontend for our EDS 6343 final project. It connects to our MySQL database (`oilfield_maintenance`) so we can show the data and add new records during the presentation.

- Person A (screens that read data): Alex Tran
- Person B (forms that save data): Rodney Hong

## Important dates

| Date | What |
|---|---|
| Nov 11 | Repo set up, both of us can push |
| Nov 16 | All "Must" items done |
| Nov 17 | Tested together, screenshots taken |
| Nov 18 | Tested on Rodney's laptop (used in class) and over Teams |
| **Nov 19** | **Presentation and live demo** (Group 4 is 3rd) |

## Expected project structure

The app only works if the folder looks like this. Files marked **local only** are on your own laptop and never go to GitHub.

```
team4-oilfield-ui/
├── app.py                         SHARED  Starts the app and wires every screen into the sidebar
├── db.py                          A       MySQL connection helpers (every screen uses these)
├── errors.py                      B       Shows database errors on screen
├── requirements.txt               SHARED  Python packages to install
├── views/
│   ├── __init__.py                        (empty, needed so Python can import the folder)
│   ├── placeholder.py             SHARED  "Not built yet" message for unfinished screens
│   ├── person_a/
│   │   ├── __init__.py                    (empty)
│   │   ├── home.py                A       1. Connection and home page
│   │   ├── equipment.py           A       2. Equipment list
│   │   ├── work_orders.py         A       3. Work orders
│   │   ├── query_highlights.py    A       4. Query highlights
│   │   └── equipment_history.py   A       11. Equipment history (nice)
│   └── person_b/
│       ├── __init__.py                    (empty)
│       ├── add_inspection.py      B       5. Add an inspection
│       ├── report_problem.py      B       6. Report a problem
│       ├── create_work_order.py   B       7. Create a work order
│       ├── complete_work_order.py B       8. Complete a work order
│       └── change_status.py       B       12. Change work order status (nice)
├── .streamlit/
│   ├── secrets.example.toml       SHARED  Template for the MySQL login
│   └── secrets.toml               LOCAL ONLY  Your real MySQL login (copy of the example)
├── sql/
│   ├── Team4_SQL_Build.sql        SHARED  Builds the database + sample data (from Phase 3)
│   └── Team4_Queries.sql          SHARED  Our 14 queries (read by query_highlights.py)
├── screenshots/                   SHARED  UI screenshots for the slides and report
├── SCOPE.md                       SHARED  What each screen does
├── tasks/                         SHARED  person-a.md, person-b.md, shared.md (checklists)
└── .gitignore                     SHARED  Keeps secrets.toml and caches out of GitHub
```

The numbers (1-12) match the items in [SCOPE.md](SCOPE.md).

## The rules that make the pieces fit together

1. **Each person only edits their own files** (A or B in the list above). Then we never get merge conflicts.
2. **Every screen file has a `render()` function.** `app.py` calls `render()` when the screen is picked in the sidebar. Keep the file names and the `render()` name the same, or `app.py` cannot find the screen.
3. **Every screen gets data only through `db.py`:**

   | Function | What it does | Used by |
   |---|---|---|
   | `get_connection()` | Returns an open MySQL connection | Forms that save several rows at once (B) |
   | `fetch_df(sql, params)` | Runs a SELECT, returns a pandas DataFrame | All read screens (A), dropdown lists in forms (B) |
   | `execute(sql, params)` | Runs one INSERT or UPDATE, commits, returns the new row's id | Forms (B) |

   Person A writes these, but **must keep these names and inputs**, because Person B's forms already call them.
4. **When a save fails, call `errors.show_db_error(err)`.** `db.py` does not hide MySQL errors, so the form can show the trigger or CHECK message.
5. **Unfinished screens stay as placeholders.** Each one shows "Not built yet" with a `todo(...)` line. Replace that line with the real code when the screen is done. The app runs the whole time, even when only some screens are finished.
6. **`app.py` is shared.** Only change it together, and only if we add or rename a screen.
7. **Do not rename tables or columns.** The UI uses the database exactly as `sql/Team4_SQL_Build.sql` creates it.

## How to run

1. Build the database: run `sql/Team4_SQL_Build.sql` in MySQL Workbench. Run it again any time you want to reset the sample data.
2. Make a Python environment and install the packages:
   ```bash
   conda create -n team4-ui python=3.11 -y
   conda activate team4-ui
   pip install -r requirements.txt
   ```
3. Copy `.streamlit/secrets.example.toml` to `.streamlit/secrets.toml` and put in your MySQL password (if your MySQL root user has no password, as with a default Homebrew install, use `password = ""`). **Never commit `secrets.toml`** (it is already in `.gitignore`).
4. Start the app from the `team4-oilfield-ui` folder:
   ```bash
   streamlit run app.py
   ```
   It opens in the browser. Pick a screen from the sidebar.

The Home screen shows "Connected to the oilfield_maintenance database" and the row count of every table. If it shows "Could not connect to MySQL", check that MySQL is running and that the login in `secrets.toml` is right. Screens that are not built yet show a "Not built yet" message.

_Person A (README task): check these steps on both laptops before Nov 16 and fix anything that is different._

## Checklists

- [SCOPE.md](SCOPE.md): what each screen does, and the demo plan
- [tasks/person-a.md](tasks/person-a.md): Person A's tasks
- [tasks/person-b.md](tasks/person-b.md): Person B's tasks
- [tasks/shared.md](tasks/shared.md): tasks we do together
