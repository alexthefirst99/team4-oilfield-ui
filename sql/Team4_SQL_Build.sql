-- =====================================================================
-- Team 4: Oilfield Equipment Maintenance Management System
-- SQL build script (MySQL 8): creates the database, the 11 tables with
-- their constraints, the business-rule triggers, and the sample data.
-- =====================================================================

DROP DATABASE IF EXISTS oilfield_maintenance;
CREATE DATABASE IF NOT EXISTS oilfield_maintenance;
USE oilfield_maintenance;

CREATE TABLE SITE (
    SITE_ID         INT             NOT NULL AUTO_INCREMENT,
    SITE_NAME       VARCHAR(50)     NOT NULL,
    SITE_LOCATION   VARCHAR(100)    NOT NULL,
    CONSTRAINT PK_SITE        PRIMARY KEY (SITE_ID),
    CONSTRAINT UQ_SITE_NAME   UNIQUE (SITE_NAME)
);
 
CREATE TABLE EQUIPMENT_TYPE (
    TYPE_ID           INT            NOT NULL AUTO_INCREMENT,
    TYPE_NAME         VARCHAR(30)    NOT NULL,
    TYPE_DESCRIPTION  VARCHAR(200)   NULL,
    CONSTRAINT PK_EQUIPMENT_TYPE  PRIMARY KEY (TYPE_ID),
    CONSTRAINT UQ_TYPE_NAME       UNIQUE (TYPE_NAME)
);
 
CREATE TABLE EQUIPMENT (
    EQUIP_ID            INT            NOT NULL AUTO_INCREMENT,
    EQUIP_ASSET_TAG     VARCHAR(20)    NOT NULL,
    EQUIP_NAME          VARCHAR(50)    NOT NULL,
    EQUIP_DESCRIPTION   VARCHAR(200)   NULL,
    EQUIP_STATUS        VARCHAR(20)    NOT NULL,
    EQUIP_INSTALL_DATE  DATE           NULL,
    SITE_ID             INT            NOT NULL,
    TYPE_ID             INT            NOT NULL,
    CONSTRAINT PK_EQUIPMENT        PRIMARY KEY (EQUIP_ID),
    CONSTRAINT UQ_EQUIP_ASSET_TAG  UNIQUE (EQUIP_ASSET_TAG),
    CONSTRAINT CK_EQUIP_STATUS     CHECK (EQUIP_STATUS IN ('Operational', 'Out of Service', 'Retired')),
    CONSTRAINT FK_EQUIPMENT_SITE   FOREIGN KEY (SITE_ID) REFERENCES SITE (SITE_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT FK_EQUIPMENT_TYPE   FOREIGN KEY (TYPE_ID) REFERENCES EQUIPMENT_TYPE (TYPE_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT
);
 
CREATE TABLE TECHNICIAN (
    TECH_ID         INT            NOT NULL AUTO_INCREMENT,
    TECH_FNAME      VARCHAR(30)    NOT NULL,
    TECH_LNAME      VARCHAR(30)    NOT NULL,
    TECH_SPECIALTY  VARCHAR(30)    NULL,
    TECH_PHONE      VARCHAR(20)    NULL,
    TECH_EMAIL      VARCHAR(100)   NOT NULL,
    CONSTRAINT PK_TECHNICIAN  PRIMARY KEY (TECH_ID),
    CONSTRAINT UQ_TECH_EMAIL  UNIQUE (TECH_EMAIL)
);
 
CREATE TABLE INSPECTION (
    INSP_ID      INT            NOT NULL AUTO_INCREMENT,
    INSP_DATE    DATE           NOT NULL,
    INSP_RESULT  VARCHAR(20)    NOT NULL,
    INSP_NOTES   VARCHAR(500)   NULL,
    EQUIP_ID     INT            NOT NULL,
    TECH_ID      INT            NOT NULL,
    CONSTRAINT PK_INSPECTION             PRIMARY KEY (INSP_ID),
    CONSTRAINT CK_INSP_RESULT            CHECK (INSP_RESULT IN ('Pass', 'Needs Maintenance', 'Fail')),
    CONSTRAINT FK_INSPECTION_EQUIPMENT   FOREIGN KEY (EQUIP_ID) REFERENCES EQUIPMENT (EQUIP_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT FK_INSPECTION_TECHNICIAN  FOREIGN KEY (TECH_ID) REFERENCES TECHNICIAN (TECH_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT
);
 
CREATE TABLE PROBLEM_REPORT (
    PROB_ID           INT            NOT NULL AUTO_INCREMENT,
    PROB_REPORT_DATE  DATE           NOT NULL,
    PROB_DESCRIPTION  VARCHAR(500)   NOT NULL,
    PROB_PRIORITY     VARCHAR(10)    NOT NULL,
    EQUIP_ID          INT            NOT NULL,
    INSP_ID           INT            NULL,
    CONSTRAINT PK_PROBLEM_REPORT             PRIMARY KEY (PROB_ID),
    CONSTRAINT CK_PROB_PRIORITY              CHECK (PROB_PRIORITY IN ('Low', 'Medium', 'High')),
    CONSTRAINT FK_PROBLEM_REPORT_EQUIPMENT   FOREIGN KEY (EQUIP_ID) REFERENCES EQUIPMENT (EQUIP_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT FK_PROBLEM_REPORT_INSPECTION  FOREIGN KEY (INSP_ID) REFERENCES INSPECTION (INSP_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT
);
 
CREATE TABLE WORK_ORDER (
    WO_ID             INT            NOT NULL AUTO_INCREMENT,
    WO_DESCRIPTION    VARCHAR(500)   NOT NULL,
    WO_TYPE           VARCHAR(15)    NOT NULL,
    WO_STATUS         VARCHAR(15)    NOT NULL DEFAULT 'Open',
    WO_CREATED_DATE   DATE           NOT NULL,
    WO_DUE_DATE       DATE           NULL,
    EQUIP_ID          INT            NOT NULL,
    PROB_ID           INT            NULL,
    CONSTRAINT PK_WORK_ORDER            PRIMARY KEY (WO_ID),
    CONSTRAINT CK_WO_TYPE               CHECK (WO_TYPE IN ('Routine', 'Corrective')),
    CONSTRAINT CK_WO_STATUS             CHECK (WO_STATUS IN ('Open', 'In Progress', 'Completed', 'Cancelled')),
    -- BR14: Corrective work needs a problem report; Routine work has none
    CONSTRAINT CK_WO_TYPE_PROBLEM       CHECK (
        (WO_TYPE = 'Corrective' AND PROB_ID IS NOT NULL) OR
        (WO_TYPE = 'Routine'    AND PROB_ID IS NULL)
    ),
    -- BR16: due date cannot be before creation date (NULL due date is allowed)
    CONSTRAINT CK_WO_DUE_DATE           CHECK (WO_DUE_DATE >= WO_CREATED_DATE),
    CONSTRAINT FK_WORK_ORDER_EQUIPMENT  FOREIGN KEY (EQUIP_ID) REFERENCES EQUIPMENT (EQUIP_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT FK_WORK_ORDER_PROBLEM    FOREIGN KEY (PROB_ID) REFERENCES PROBLEM_REPORT (PROB_ID)
        ON UPDATE RESTRICT ON DELETE RESTRICT
);
 
CREATE TABLE WORK_ASSIGNMENT (
    WO_ID    INT  NOT NULL,
    TECH_ID  INT  NOT NULL,
    CONSTRAINT PK_WORK_ASSIGNMENT             PRIMARY KEY (WO_ID, TECH_ID),
    CONSTRAINT FK_WORK_ASSIGNMENT_WORK_ORDER  FOREIGN KEY (WO_ID) REFERENCES WORK_ORDER (WO_ID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT FK_WORK_ASSIGNMENT_TECHNICIAN  FOREIGN KEY (TECH_ID) REFERENCES TECHNICIAN (TECH_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT
);
 
CREATE TABLE MAINTENANCE_RECORD (
    MAINT_ID                INT             NOT NULL AUTO_INCREMENT,
    MAINT_COMPLETION_DATE   DATE            NOT NULL,
    MAINT_WORK_PERFORMED    VARCHAR(1000)   NOT NULL,
    WO_ID                   INT             NOT NULL,
    CONSTRAINT PK_MAINTENANCE_RECORD             PRIMARY KEY (MAINT_ID),
    CONSTRAINT UQ_MAINTENANCE_RECORD_WO          UNIQUE (WO_ID),
    CONSTRAINT FK_MAINTENANCE_RECORD_WORK_ORDER  FOREIGN KEY (WO_ID) REFERENCES WORK_ORDER (WO_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT
);
 
CREATE TABLE PART (
    PART_ID      INT           NOT NULL AUTO_INCREMENT,
    PART_NUMBER  VARCHAR(30)   NOT NULL,
    PART_NAME    VARCHAR(50)   NOT NULL,
    PART_UNIT    VARCHAR(10)   NOT NULL,
    CONSTRAINT PK_PART         PRIMARY KEY (PART_ID),
    CONSTRAINT UQ_PART_NUMBER  UNIQUE (PART_NUMBER),
    CONSTRAINT CK_PART_UNIT    CHECK (PART_UNIT IN ('each', 'liter', 'meter'))
);
 
CREATE TABLE PART_USAGE (
    MAINT_ID   INT             NOT NULL,
    PART_ID    INT             NOT NULL,
    USAGE_QTY  DECIMAL(10,2)   NOT NULL,
    CONSTRAINT PK_PART_USAGE              PRIMARY KEY (MAINT_ID, PART_ID),
    CONSTRAINT CK_USAGE_QTY               CHECK (USAGE_QTY > 0),
    CONSTRAINT FK_PART_USAGE_MAINTENANCE  FOREIGN KEY (MAINT_ID) REFERENCES MAINTENANCE_RECORD (MAINT_ID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT FK_PART_USAGE_PART         FOREIGN KEY (PART_ID) REFERENCES PART (PART_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

DELIMITER $$

CREATE TRIGGER TRG_MAINTENANCE_RECORD_AI
AFTER INSERT ON MAINTENANCE_RECORD
FOR EACH ROW
BEGIN
    UPDATE WORK_ORDER
       SET WO_STATUS = 'Completed'
     WHERE WO_ID = NEW.WO_ID;
END$$

CREATE TRIGGER TRG_MAINTENANCE_RECORD_BI
BEFORE INSERT ON MAINTENANCE_RECORD
FOR EACH ROW
BEGIN
    IF NEW.MAINT_COMPLETION_DATE <
       (SELECT WO_CREATED_DATE FROM WORK_ORDER WHERE WO_ID = NEW.WO_ID) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'BR16: Completion date cannot be before the work order creation date.';
    END IF;
 
    IF (SELECT WO_STATUS FROM WORK_ORDER WHERE WO_ID = NEW.WO_ID) = 'Cancelled' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'BR16: A Cancelled work order cannot have a maintenance record.';
    END IF;
 
    IF NOT EXISTS (SELECT 1 FROM WORK_ASSIGNMENT WHERE WO_ID = NEW.WO_ID) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'BR15: Assign at least one technician before recording completed work.';
    END IF;
END$$
 
CREATE TRIGGER TRG_WORK_ORDER_BI
BEFORE INSERT ON WORK_ORDER
FOR EACH ROW
BEGIN
    IF NEW.PROB_ID IS NOT NULL AND NEW.EQUIP_ID <>
       (SELECT EQUIP_ID FROM PROBLEM_REPORT WHERE PROB_ID = NEW.PROB_ID) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'BR18: Work order and its problem report must concern the same equipment.';
    END IF;
 
    IF NEW.WO_STATUS IN ('In Progress', 'Completed') THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'BR15/BR16: A new work order must start as Open (or Cancelled).';
    END IF;
END$$ 

CREATE TRIGGER TRG_WORK_ORDER_BU
BEFORE UPDATE ON WORK_ORDER
FOR EACH ROW
BEGIN
    IF NEW.PROB_ID IS NOT NULL AND NEW.EQUIP_ID <>
       (SELECT EQUIP_ID FROM PROBLEM_REPORT WHERE PROB_ID = NEW.PROB_ID) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'BR18: Work order and its problem report must concern the same equipment.';
    END IF;
 
    IF NEW.WO_STATUS IN ('In Progress', 'Completed')
       AND NOT EXISTS (SELECT 1 FROM WORK_ASSIGNMENT WHERE WO_ID = NEW.WO_ID) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'BR15: Assign at least one technician before the work order is In Progress or Completed.';
    END IF;
 
    IF NEW.WO_STATUS = 'Completed'
       AND NOT EXISTS (SELECT 1 FROM MAINTENANCE_RECORD WHERE WO_ID = NEW.WO_ID) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'BR16: A work order is Completed only when it has a maintenance record.';
    END IF;
 
    IF NEW.WO_STATUS <> 'Completed'
       AND EXISTS (SELECT 1 FROM MAINTENANCE_RECORD WHERE WO_ID = NEW.WO_ID) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'BR16: A work order with a maintenance record must stay Completed.';
    END IF;
 
    IF EXISTS (SELECT 1 FROM MAINTENANCE_RECORD
               WHERE WO_ID = NEW.WO_ID
                 AND MAINT_COMPLETION_DATE < NEW.WO_CREATED_DATE) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'BR16: Completion date cannot be before the work order creation date.';
    END IF;
END$$

CREATE TRIGGER TRG_PROBLEM_REPORT_BI
BEFORE INSERT ON PROBLEM_REPORT
FOR EACH ROW
BEGIN
    IF NEW.INSP_ID IS NOT NULL AND NEW.EQUIP_ID <>
       (SELECT EQUIP_ID FROM INSPECTION WHERE INSP_ID = NEW.INSP_ID) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'BR18: Problem report and its inspection must concern the same equipment.';
    END IF;
END$$

DELIMITER ;

START TRANSACTION; 

INSERT INTO SITE (SITE_ID, SITE_NAME, SITE_LOCATION) VALUES
(1, 'Landman South', 'Midland, TX'), 
(2, 'AES North', 'Kermit, TX'),
(3, 'Terracotta West', 'Pecos, TX');

INSERT INTO EQUIPMENT_TYPE (TYPE_ID, TYPE_NAME, TYPE_DESCRIPTION) VALUES
(1, 'Pump', NULL),
(2, 'Compressor', NULL),
(3, 'Drill Bit', 'Used for drills'),
(4, 'Generator', 'Generating power'),
(5, 'Valve', NULL);

INSERT INTO TECHNICIAN (TECH_ID, TECH_FNAME, TECH_LNAME, TECH_SPECIALTY, TECH_PHONE, TECH_EMAIL) VALUES
(1, 'Rodney', 'Hong', 'Mechanical', '123-456-7890', 'ryhong@example.com'),
(2, 'Alex', 'Tran', 'Mechanical', '098-765-4321', 'atran@example.com'), 
(3, 'Luffy', 'Monkey', NULL, NULL, 'luffy@example.com'),
(4, 'Naruto', 'Uzumaki', 'Electrical', NULL, 'nuzumaki@example.com'),
(5, 'Ben', 'Tennyson', NULL, '111-222-4444', 'bten@example.com');

INSERT INTO PART (PART_ID, PART_NUMBER, PART_NAME, PART_UNIT) VALUES
(1, 'PS-1',   'Oil Filter',      'each'),
(2, 'PS-2',   'Pump Seal',       'each'),
(3, 'PS-20',  'Bearing',         'each'),
(4, 'PS-7',   'Drive Belt',      'each'),
(5, 'PS-420', 'Gasket',          'each'),
(6, 'PS-5',   'Engine Oil',      'liter'),
(7, 'PS-944', 'Hydraulic Hose',  'meter'),
(8, 'PS-8',   'Spark Plug',      'each');

INSERT INTO EQUIPMENT (EQUIP_ID, EQUIP_ASSET_TAG, EQUIP_NAME, EQUIP_DESCRIPTION, EQUIP_STATUS, EQUIP_INSTALL_DATE, SITE_ID, TYPE_ID) VALUES
(1,  'PMP-001', 'Crude Transfer Pump 1',    'Moves crude oil to the sales tank',      'Operational',    '2019-03-15', 1, 1),
(2,  'PMP-002', 'Crude Transfer Pump 2',    'Backup crude transfer pump',             'Operational',    '2019-03-15', 1, 1),
(3,  'PMP-003', 'Water Injection Pump',     'Injects produced water into the well',   'Out of Service', '2020-07-01', 2, 1),
(4,  'CMP-001', 'Gas Lift Compressor',      'Supplies gas for gas lift wells',        'Operational',    '2018-11-20', 1, 2),
(5,  'CMP-002', 'Station Compressor A',     'Main gas compressor',                    'Operational',    '2017-05-10', 2, 2),
(6,  'CMP-003', 'Station Compressor B',     'Second gas compressor',                  'Out of Service', '2017-05-10', 2, 2),
(7,  'GEN-001', 'Pad Generator',            'Main power for the pad',                 'Operational',    '2021-02-08', 1, 4),
(8,  'GEN-002', 'Backup Generator',         NULL,                                     'Operational',    '2022-09-14', 2, 4),
(9,  'GEN-003', 'Old Station Generator',    'Replaced by GEN-002',                    'Retired',        '2012-04-01', 2, 4),
(10, 'VLV-001', 'Emergency Shutdown Valve', 'Closes the sales line in an emergency',  'Operational',    '2019-03-20', 1, 5),
(11, 'VLV-002', 'Pressure Relief Valve',    'Releases pressure on the water line',    'Operational',    NULL,         2, 5),
(12, 'PMP-004', 'Chemical Injection Pump',  'Newly installed; not yet inspected',     'Operational',    '2026-09-30', 1, 1);

INSERT INTO INSPECTION (INSP_ID, INSP_DATE, INSP_RESULT, INSP_NOTES, EQUIP_ID, TECH_ID) VALUES
(1,  '2026-01-12', 'Pass',              'Normal vibration and temperature',        1,  1),
(2,  '2026-01-20', 'Needs Maintenance', 'Pump seal leaking',                       3,  4),
(3,  '2026-02-03', 'Pass',              'Running normally',                        4,  4),
(4,  '2026-02-10', 'Needs Maintenance', 'Running hot on the second stage',         6,  2),
(5,  '2026-03-05', 'Pass',              'Load test passed',                        7,  1),
(6,  '2026-03-18', 'Pass',              'Valve closed in the required time',       10, 3),
(7,  '2026-04-15', 'Needs Maintenance', 'Bearing vibration above normal',          1,  1),
(8,  '2026-05-06', 'Pass',              'Running normally',                        5,  2),
(9,  '2026-06-09', 'Fail',              'Loud knocking; unit shut down',           6,  4),
(10, '2026-07-14', 'Fail',              'Pump will not build pressure',            3,  1),
(11, '2026-08-04', 'Needs Maintenance', 'Battery charger warning light on',        8,  2),
(12, '2026-09-08', 'Pass',              'Vibration back to normal after repair',   1,  4),
(13, '2026-09-22', 'Needs Maintenance', 'Small oil leak at gearbox',               2,  3),
(14, '2025-11-03', 'Fail',              'Failed load test; unit retired',          9,  2),
(15, '2026-10-13', 'Needs Maintenance', 'Drive belt worn and slipping',            4,  4);

INSERT INTO PROBLEM_REPORT (PROB_ID, PROB_REPORT_DATE, PROB_DESCRIPTION, PROB_PRIORITY, EQUIP_ID, INSP_ID) VALUES
(1,  '2026-01-20', 'Pump seal leaking water',                 'Medium', 3,  2),
(2,  '2026-02-10', 'Second stage running hot',                'Medium', 6,  4),
(3,  '2026-04-15', 'Bearing vibration above normal',          'Medium', 1,  7),
(4,  '2026-05-22', 'Operator heard grinding noise from pump', 'High',   1,  NULL),
(5,  '2026-06-09', 'Knocking in cylinder; unit shut down',    'High',   6,  9),
(6,  '2026-07-14', 'Pump cannot build pressure',              'High',   3,  10),
(7,  '2026-08-04', 'Battery charger fault',                   'Medium', 8,  11),
(8,  '2026-09-22', 'Gearbox oil leak',                        'Low',    2,  13),
(9,  '2026-10-01', 'Operator reports valve slow to close',    'High',   10, NULL),
(10, '2026-10-13', 'Drive belt worn and slipping',            'Low',    4,  15);

INSERT INTO WORK_ORDER (WO_ID, WO_DESCRIPTION, WO_TYPE, WO_STATUS, WO_CREATED_DATE, WO_DUE_DATE, EQUIP_ID, PROB_ID) VALUES
(1,  'Replace pump seal',                  'Corrective', 'Open',      '2026-01-21', '2026-01-31', 3,  1),
(2,  'Fix second stage overheating',       'Corrective', 'Open',      '2026-02-11', '2026-02-25', 6,  2),
(3,  'Grease pump bearing',                'Corrective', 'Open',      '2026-04-16', '2026-04-30', 1,  3),
(4,  'Replace pump bearing',               'Corrective', 'Open',      '2026-05-22', '2026-06-01', 1,  4),
(5,  'Repair cylinder knocking',           'Corrective', 'Open',      '2026-06-10', '2026-06-24', 6,  5),
(6,  'Overhaul water injection pump',      'Corrective', 'Open',      '2026-07-15', '2026-08-15', 3,  6),
(7,  'Inspect cylinder after knock returned', 'Corrective', 'Open',   '2026-07-01', '2026-07-31', 6,  5),
(8,  'Replace battery charger',            'Corrective', 'Open',      '2026-08-05', '2026-08-20', 8,  7),
(9,  'Replace gearbox seal',               'Corrective', 'Open',      '2026-09-23', '2026-10-15', 2,  8),
(10, 'Repair valve actuator',              'Corrective', 'Open',      '2026-10-02', '2026-11-06', 10, 9),
(11, 'Quarterly compressor service',       'Routine',    'Open',      '2026-03-01', '2026-03-15', 5,  NULL),
(12, 'Semiannual compressor service',      'Routine',    'Open',      '2026-06-15', '2026-06-30', 4,  NULL),
(13, 'Annual valve function test',         'Routine',    'Cancelled', '2026-08-25', '2026-09-30', 10, NULL),
(14, 'Generator 500-hour service',         'Routine',    'Open',      '2026-10-15', '2026-11-15', 7,  NULL);

INSERT INTO WORK_ASSIGNMENT (WO_ID, TECH_ID) VALUES
(1, 4),  
(1, 1),
(2, 2),  
(2, 4),
(3, 1),
(4, 1),  
(4, 4),
(5, 4),  
(5, 2),
(6, 1),  
(6, 4),
(7, 4),  
(7, 2),
(8, 2),
(10, 3),
(11, 2),
(12, 4), 
(12, 3);

UPDATE WORK_ORDER
SET WO_STATUS = 'In Progress'
WHERE WO_ID IN (6, 7);
 
INSERT INTO MAINTENANCE_RECORD (MAINT_ID, MAINT_COMPLETION_DATE, MAINT_WORK_PERFORMED, WO_ID) VALUES
(1, '2026-01-28', 'Replaced pump seal and gaskets; tested at operating pressure', 1),
(2, '2026-02-20', 'Replaced leaking cooler hose and gasket on second stage',     2),
(3, '2026-04-28', 'Greased bearing and checked alignment',                       3),
(4, '2026-05-30', 'Replaced both bearings and topped up oil',                    4),
(5, '2026-06-22', 'Replaced cylinder gaskets and tightened valve covers',        5),
(6, '2026-08-18', 'Tightened loose charger wiring and reset the fault',          8),
(7, '2026-03-12', 'Changed oil and oil filters',                                 11),
(8, '2026-06-26', 'Changed oil and filters; replaced drive belts',               12);

INSERT INTO PART_USAGE (MAINT_ID, PART_ID, USAGE_QTY) VALUES
(1, 2, 1.00),  
(1, 5, 2.00),
(2, 7, 2.50),  
(2, 5, 1.00),
(4, 3, 2.00),  
(4, 6, 2.00),
(5, 5, 4.00),
(7, 1, 2.00),  
(7, 6, 40.00),
(8, 1, 2.00),  
(8, 6, 40.00), 
(8, 4, 3.00);

COMMIT;

SHOW TABLES;