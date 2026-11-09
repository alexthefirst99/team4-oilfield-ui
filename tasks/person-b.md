# Person B: forms that save data

Name: _______________ (Rodney picks A or B)

Check each box when it is done. Details for each screen are in [SCOPE.md](../SCOPE.md).

**Your files** (only you edit these): `errors.py` and everything in `views/person_b/`. Each screen file already has a `render()` function with a hint. Replace the `todo(...)` line with the real form.

You can start the forms right away using the function names in `db.py` (`get_connection()`, `fetch_df()`, `execute()`). They work once Person A finishes item 1.

## Must (by Nov 16)

- [ ] **5. Add an inspection** (`views/person_b/add_inspection.py`)
  - [ ] Pick equipment and technician from lists. Enter date, result, and notes.
  - [ ] Result is a list with only Pass, Needs Maintenance, and Fail (matches our CHECK).
  - Done when: the new row shows up in MySQL Workbench.
- [ ] **6. Report a problem** (`views/person_b/report_problem.py`)
  - [ ] Pick equipment, choose priority (Low, Medium, High), and write a description.
  - [ ] Optionally link an inspection.
  - Done when: the new row is saved, and linking an inspection of a different equipment item shows the BR18 message.
- [ ] **7. Create a work order** (`views/person_b/create_work_order.py`)
  - [ ] Choose Routine or Corrective. Corrective must link a problem report, Routine must not (BR14).
  - [ ] Enter created date and due date (due date cannot be before created date).
  - [ ] Assign one or more technicians (saves rows in WORK_ASSIGNMENT).
  - Done when: the order and its technicians show up in Workbench.
- [ ] **8. Complete a work order** (`views/person_b/complete_work_order.py`)
  - [ ] Pick an order, enter the completion date and the work performed.
  - [ ] Add the parts used with their quantity.
  - Done when: the order shows Completed by itself (our trigger does this).
- [ ] **9. Error messages** (`errors.py`)
  - [ ] When MySQL blocks a save, show its message on screen instead of crashing.
  - Done when: completing an order with no technician shows the BR15 message. This is our demo moment.

## Nice (only if there is time)

- [ ] **12. Change work order status** (`views/person_b/change_status.py`). Move an order from Open to In Progress or Cancelled.
  - Done when: it works, or the BR15 message shows when no technician is assigned.
