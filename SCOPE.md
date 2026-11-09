# UI Scope

## Goal

Show that our database works through a simple app: the app **reads** data from MySQL and **saves** new data to MySQL, and our business rules (CHECK constraints and triggers) still protect the data.

## Rules for the build

- Use our database exactly as it is. **Do not rename or change any table or column.** The UI uses the same 11 tables as `sql/Team4_SQL_Build.sql`.
- The UI must run on **Rodney's laptop**, because that laptop is used for the live demo in class.
- Keep it simple. Plain tables and forms are fine.
- When MySQL blocks something (a trigger or a CHECK), show the error message on screen. The app should not crash.

## Screens

**Must** = needed for the Nov 19 demo. **Nice** = only if there is time.

| # | Screen | What the user can do | Tables used | Rules it shows | Priority | Who |
|---|---|---|---|---|---|---|
| 1 | Connection and home page | Connect to MySQL and see how many rows each table has | All 11 tables | - | Must | A |
| 2 | Equipment list | See all equipment with its site and type. Filter by site and status | EQUIPMENT, SITE, EQUIPMENT_TYPE | - | Must | A |
| 3 | Work orders | See work orders with their equipment and assigned technicians. Filter by status | WORK_ORDER, WORK_ASSIGNMENT, TECHNICIAN, EQUIPMENT | - | Must | A |
| 4 | Query highlights | Pick one of our Phase 3 queries, see its SQL, and run it | All (`sql/Team4_Queries.sql`) | - | Must | A |
| 5 | Add an inspection | Pick equipment and technician, enter date, result, and notes, then save | INSPECTION | Result must be Pass, Needs Maintenance, or Fail (CHECK) | Must | B |
| 6 | Report a problem | Pick equipment, optionally link an inspection, choose priority, describe the problem, then save | PROBLEM_REPORT | BR18: the inspection must be on the same equipment (trigger) | Must | B |
| 7 | Create a work order | Choose Routine or Corrective, set dates, link a problem report (Corrective only), and assign technicians | WORK_ORDER, WORK_ASSIGNMENT | BR14 (CHECK), BR18 (trigger), due date not before created date (CHECK) | Must | B |
| 8 | Complete a work order | Record the work done and the parts used. The order changes to Completed by itself | MAINTENANCE_RECORD, PART_USAGE, PART | BR15 and BR16 (triggers) | Must | B |
| 9 | Error messages | Show MySQL's message when a rule blocks a save | - | BR15, BR16, BR18 messages | Must | B |
| 10 | README | How to install, connect, and start the UI | - | - | Must | A |
| 11 | Equipment history | Pick one equipment item and see its inspections, problems, and repairs | EQUIPMENT, INSPECTION, PROBLEM_REPORT, WORK_ORDER, MAINTENANCE_RECORD | - | Nice | A |
| 12 | Change work order status | Move an order from Open to In Progress or Cancelled | WORK_ORDER | BR15: needs a technician first (trigger) | Nice | B |

Each person has 5 Must items and 1 Nice item.

## Demo plan for Nov 19 (about 1.5 minutes)

1. Home page: the row counts prove the UI is connected to MySQL.
2. Equipment list or work orders: filter the data.
3. Save something new (for example an inspection), then show it in the list.
4. Try to complete a work order that has no technician. The BR15 trigger blocks it and the message shows on screen.

Keep screenshots of every step as a backup in case the live demo fails.

## Not in scope

- Login and user accounts
- Deleting records
- A screen for every table
- Styling and design

## Done means

- Every Must item works on Rodney's laptop with a fresh run of the build script.
- Data saved in the UI shows up in MySQL Workbench.
- The README lets someone else start the UI.
