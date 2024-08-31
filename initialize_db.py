import sqlite3

# Path to the database
db_path = 'database.db'

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop existing tables if they exist
cursor.execute("DROP TABLE IF EXISTS students;")
cursor.execute("DROP TABLE IF EXISTS classrooms;")
cursor.execute("DROP TABLE IF EXISTS teachers;")
cursor.execute("DROP TABLE IF EXISTS results;")  # Drop the results table if it exists

# Create new tables
create_students_table = '''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code_rim TEXT NOT NULL,
    gender TEXT NOT NULL,
    date_of_register TEXT NOT NULL,
    classroom TEXT NOT NULL,
    price REAL NOT NULL,
    number_of_agent INTEGER NOT NULL
);
'''

create_classrooms_table = '''
CREATE TABLE IF NOT EXISTS classrooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    level TEXT NOT NULL,
    type TEXT NOT NULL,
    subjects TEXT
);
'''

create_teachers_table = '''
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    gender TEXT NOT NULL,
    date_of_register TEXT NOT NULL,
    classroom TEXT NOT NULL,
    salary REAL NOT NULL,
    number_of_teachers INTEGER NOT NULL
);
'''

# Drop and recreate the results table with the new schema including coefficient columns for each subject
create_results_table = '''
CREATE TABLE IF NOT EXISTS results (
    student_code_rim TEXT NOT NULL,
    student_name TEXT NOT NULL,
    classroom TEXT NOT NULL,
    examen_type TEXT NOT NULL,
    Math INTEGER,
    c_Math INTEGER,
    PC INTEGER,
    c_PC INTEGER,
    SN INTEGER,
    c_SN INTEGER,
    FR INTEGER,
    c_FR INTEGER,
    EN INTEGER,
    c_EN INTEGER,
    AR INTEGER,
    c_AR INTEGER,
    ES INTEGER,
    c_ES INTEGER,
    IE INTEGER,
    c_IE INTEGER,
    CE INTEGER,
    c_CE INTEGER,
    HG INTEGER,
    c_HG INTEGER,
    PH INTEGER,
    c_PH INTEGER,
    IL INTEGER,
    c_IL INTEGER,
    IT INTEGER,
    c_IT INTEGER,
    KH INTEGER,
    c_KH INTEGER,
    ID INTEGER,
    c_ID INTEGER,
    ET INTEGER,
    c_ET INTEGER,
    WS INTEGER,
    c_WS INTEGER,
    MC INTEGER,
    c_MC INTEGER,
    IA INTEGER,
    c_IA INTEGER,
    TA INTEGER,
    c_TA INTEGER
);
'''

# Execute the queries to create the tables
cursor.execute(create_students_table)
cursor.execute(create_classrooms_table)
cursor.execute(create_teachers_table)
cursor.execute(create_results_table)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database initialized successfully.")
