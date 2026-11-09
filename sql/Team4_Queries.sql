USE oilfield_maintenance;

-- =====================================================================
-- BASIC QUERIES (joins, filters, ordering)
-- =====================================================================

-- Basic Query 1: Shows all the inspections that technician Rodney Hong has done with the equipment's asset tag, name, date, and result sorted by date
select T.TECH_FNAME, E.EQUIP_ASSET_TAG, E.EQUIP_NAME, I.INSP_DATE, I.INSP_RESULT
from INSPECTION I
join TECHNICIAN T on I.TECH_ID = T.TECH_ID
join EQUIPMENT E ON E.EQUIP_ID = I.EQUIP_ID
where T.TECH_FNAME = 'Rodney'
and T.TECH_LNAME = 'Hong'
order by I.INSP_DATE desc;

-- Basic Query 2: Shows the problem reports that are medium and high priority, showing the report date, description, priority, equipment asset tag, and site name that the equipment is at
select PR.PROB_REPORT_DATE, PR.PROB_DESCRIPTION, PR.PROB_PRIORITY, E.EQUIP_ASSET_TAG, S.SITE_NAME
from PROBLEM_REPORT PR
join EQUIPMENT E on E.EQUIP_ID = PR.EQUIP_ID
join SITE S on S.SITE_ID = E.SITE_ID
where PR.PROB_PRIORITY in ('Medium', 'High')
order by PR.PROB_PRIORITY, PR.PROB_REPORT_DATE desc;

-- Basic Query 3: Shows the work orders that are still active and sorted by the earliest due date
select WO_ID, WO_DESCRIPTION, WO_TYPE, WO_STATUS, WO_CREATED_DATE, WO_DUE_DATE
from WORK_ORDER
where WO_STATUS in ('Open', 'In Progress')
order by WO_DUE_DATE;

-- Basic Query 4: Shows every equipment item with its type and the site it is located at, sorted by site and then asset tag
select S.SITE_NAME, E.EQUIP_ASSET_TAG, E.EQUIP_NAME, ET.TYPE_NAME, E.EQUIP_STATUS
from EQUIPMENT E
join SITE S on S.SITE_ID = E.SITE_ID
join EQUIPMENT_TYPE ET on ET.TYPE_ID = E.TYPE_ID
order by S.SITE_NAME, E.EQUIP_ASSET_TAG;

-- Basic Query 5: Shows the equipment that is not operational (Out of Service or Retired) and where it is located
select E.EQUIP_ASSET_TAG, E.EQUIP_NAME, E.EQUIP_STATUS, S.SITE_NAME, S.SITE_LOCATION
from EQUIPMENT E
join SITE S on S.SITE_ID = E.SITE_ID
where E.EQUIP_STATUS <> 'Operational'
order by E.EQUIP_STATUS, E.EQUIP_ASSET_TAG;

-- Basic Query 6: Shows the completed repair history of pump PMP-001, with the work order, completion date, and the work that was done
select E.EQUIP_ASSET_TAG, WO.WO_ID, WO.WO_DESCRIPTION, MR.MAINT_COMPLETION_DATE, MR.MAINT_WORK_PERFORMED
from EQUIPMENT E
join WORK_ORDER WO on WO.EQUIP_ID = E.EQUIP_ID
join MAINTENANCE_RECORD MR on MR.WO_ID = WO.WO_ID
where E.EQUIP_ASSET_TAG = 'PMP-001'
order by MR.MAINT_COMPLETION_DATE;

-- Basic Query 7: Shows the replacement parts used to complete work order 4, with the quantity and unit of each part
select WO.WO_ID, WO.WO_DESCRIPTION, P.PART_NUMBER, P.PART_NAME, PU.USAGE_QTY, P.PART_UNIT
from WORK_ORDER WO
join MAINTENANCE_RECORD MR on MR.WO_ID = WO.WO_ID
join PART_USAGE PU on PU.MAINT_ID = MR.MAINT_ID
join PART P on P.PART_ID = PU.PART_ID
where WO.WO_ID = 4
order by P.PART_NAME;

-- =====================================================================
-- INTERMEDIATE QUERIES (GROUP BY + HAVING, subqueries)
-- =====================================================================

-- Intermediate Query 1: Shows how many inspections every technician has done if they've done at least 3
select T.TECH_ID, T.TECH_FNAME, count(I.INSP_ID) as numInspections
from TECHNICIAN T
join INSPECTION I on I.TECH_ID = T.TECH_ID
group by T.TECH_ID, T.TECH_FNAME
having numInspections >= 3
order by numInspections desc;

-- Intermediate Query 2: Shows the total quantity used of each part if its total quantity is over 2
select P.PART_ID, P.PART_NAME, P.PART_UNIT, sum(PU.USAGE_QTY) as totalQty
from PART P
join PART_USAGE PU on PU.PART_ID = P.PART_ID
group by P.PART_ID, P.PART_NAME, P.PART_UNIT
having totalQty > 2
order by totalQty;

-- Intermediate Query 3: Shows the list of technicians who have never been assigned a work order
select T.TECH_ID, T.TECH_FNAME, T.TECH_LNAME
from TECHNICIAN T
where T.TECH_ID not in (
	select WA.TECH_ID
    from WORK_ASSIGNMENT WA
);

-- Intermediate Query 4: Shows the equipment that has had more than one work order, with the number of work orders for each
select E.EQUIP_ASSET_TAG, E.EQUIP_NAME, count(WO.WO_ID) as numWorkOrders
from EQUIPMENT E
join WORK_ORDER WO on WO.EQUIP_ID = E.EQUIP_ID
group by E.EQUIP_ID, E.EQUIP_ASSET_TAG, E.EQUIP_NAME
having numWorkOrders > 1
order by numWorkOrders desc, E.EQUIP_ASSET_TAG;

-- Intermediate Query 5: Shows the equipment that has never been inspected
select E.EQUIP_ASSET_TAG, E.EQUIP_NAME, E.EQUIP_STATUS, E.EQUIP_INSTALL_DATE
from EQUIPMENT E
where not exists (
	select 1
    from INSPECTION I
    where I.EQUIP_ID = E.EQUIP_ID
)
order by E.EQUIP_ASSET_TAG;

-- =====================================================================
-- ADVANCED QUERIES (Bonus)
-- =====================================================================

-- Advanced Query 1: Shows how many days each completed work order took, and compares it with the average number of days for that work order type (window function)
select WO.WO_ID, WO.WO_TYPE, E.EQUIP_ASSET_TAG,
       datediff(MR.MAINT_COMPLETION_DATE, WO.WO_CREATED_DATE) as daysToComplete,
       round(avg(datediff(MR.MAINT_COMPLETION_DATE, WO.WO_CREATED_DATE))
             over (partition by WO.WO_TYPE), 1) as avgDaysForType
from WORK_ORDER WO
join MAINTENANCE_RECORD MR on MR.WO_ID = WO.WO_ID
join EQUIPMENT E on E.EQUIP_ID = WO.EQUIP_ID
order by WO.WO_TYPE, daysToComplete desc;

-- Advanced Query 2: Shows a maintenance summary for every equipment item, counting its inspections, problem reports, and completed repairs, including equipment with no records (CTE)
with REPAIRS as (
	select WO.EQUIP_ID, count(*) as numRepairs
    from WORK_ORDER WO
    join MAINTENANCE_RECORD MR on MR.WO_ID = WO.WO_ID
    group by WO.EQUIP_ID
)
select E.EQUIP_ASSET_TAG, E.EQUIP_NAME,
       (select count(*) from INSPECTION I where I.EQUIP_ID = E.EQUIP_ID) as numInspections,
       (select count(*) from PROBLEM_REPORT PR where PR.EQUIP_ID = E.EQUIP_ID) as numProblems,
       coalesce(R.numRepairs, 0) as numRepairs
from EQUIPMENT E
left join REPAIRS R on R.EQUIP_ID = E.EQUIP_ID
order by numRepairs desc, numProblems desc, E.EQUIP_ASSET_TAG;
