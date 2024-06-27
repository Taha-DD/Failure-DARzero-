-- creating students data table 
DROP TABLE IF EXISTS students;

CREATE TABLE students (
    Name TEXT,
    "Grade S1" REAL,
    "Grade S2" REAL,
    "Year Average" REAL,
    Class TEXT
);

-- Drop the class_statistics view if it exists
DROP VIEW IF EXISTS class_statistics;

-- Create a view for class statistics
CREATE VIEW class_statistics AS
SELECT
    Class,
    COUNT(*) AS count,
    (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM students)) AS percentage
FROM students
GROUP BY Class;
