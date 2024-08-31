import tkinter as tk
from tkinter import ttk
import sqlite3

class ResultsManagement:
    def __init__(self, frame):
        self.frame = frame

        # Title Label
        tk.Label(self.frame, text="Results Management", font=("Arial", 16)).pack(pady=10)

        # Search Frame
        search_frame = ttk.LabelFrame(self.frame, text="Search Student", padding="10")
        search_frame.pack(pady=10, fill='x')

        search_inner_frame = ttk.Frame(search_frame)
        search_inner_frame.pack(anchor='center')

        tk.Label(search_inner_frame, text="Student Code Rim:").pack(side='left', padx=5)
        self.code_rim_entry = ttk.Entry(search_inner_frame, width=30)
        self.code_rim_entry.pack(side='left', padx=5)

        ttk.Button(search_inner_frame, text="Search", command=self.search_student).pack(side='left', padx=5)

        # Result Frame
        self.result_frame = ttk.LabelFrame(self.frame, text="Student Information", padding="10")
        self.result_frame.pack(pady=10, fill='x')

        # Control Frame for Edit, Delete, and Insert buttons (initially hidden)
        self.control_frame = ttk.Frame(self.frame)
        self.control_frame.pack(pady=10, fill='x')
        self.control_frame.pack_forget()

        self.edit_button = ttk.Button(self.control_frame, text="Edit", command=self.edit_student_result)
        self.edit_button.pack(side='left', padx=5)

        self.delete_button = ttk.Button(self.control_frame, text="Delete", command=self.delete_student_result)
        self.delete_button.pack(side='left', padx=5)

        self.insert_button = ttk.Button(self.control_frame, text="Insert", command=self.insert_student_result)
        self.insert_button.pack(side='left', padx=5)

        # Subjects mapping
        self.subjects = {
            "Math": "Mathematic",
            "PC": "Physique Chimie",
            "SN": "Science Naturelle",
            "FR": "Français",
            "EN": "English",
            "AR": "Arabic",
            "ES": "Español",
            "IE": "Islamic Education",
            "CE": "Civic Education",
            "HG": "History Geography",
            "PH": "Philosophy",
            "IL": "Islamic Legislation",
            "IT": "Islamic Thought",
            "KH": "Quran Hadith",
            "ID": "Industrial Drawing",
            "ET": "Electronics",
            "WS": "Workshop",
            "MC": "Mechanical Constructions",
            "IA": "Industrial Analysis",
            "TA": "Technology Automation"
        }

    def search_student(self):
        code_rim = self.code_rim_entry.get()

        if not code_rim:
            self.display_message("Please enter a code rim.")
            return

        # Connect to the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        try:
            # Query the student by code rim
            cursor.execute("""
                SELECT name, code_rim, classroom 
                FROM students 
                WHERE code_rim = ?
            """, (code_rim,))
            student = cursor.fetchone()

            if student:
                name, code_rim, classroom = student

                # Query the subjects for the classroom
                cursor.execute("""
                    SELECT subjects 
                    FROM classrooms 
                    WHERE title = ?
                """, (classroom,))
                subjects = cursor.fetchone()
                
                if subjects and subjects[0]:
                    subjects_list = subjects[0].split(',')
                    self.display_student_info(name, code_rim, classroom, subjects_list)
                else:
                    self.display_message("Subjects not available.")
            else:
                self.display_message("Student not found.")
        except sqlite3.Error as e:
            self.display_message(f"An error occurred: {e}")
        finally:
            conn.close()

    def display_message(self, message):
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        self.control_frame.pack_forget()
        tk.Label(self.result_frame, text=message, font=("Arial", 12)).pack(pady=10)

    def display_student_info(self, name, code_rim, classroom, subjects_list):
        # Clear previous results
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # Top Frame for student information
        top_frame = ttk.Frame(self.result_frame)
        top_frame.pack(pady=10, fill='x')

        # Examen Type Frame within top_frame
        examen_type_frame = ttk.Frame(top_frame)
        examen_type_frame.pack(side='right', padx=10)

        tk.Label(examen_type_frame, text='Examen Type ', font=("Arial", 12), background='#36C2CE').pack(anchor='center', fill='x')

        self.examen_type_combobox = ttk.Combobox(examen_type_frame, values=[
            "devoir 1", "examen 1", "devoir 2", "examen 2", "devoir 3", "examen 3"
        ])
        self.examen_type_combobox.pack(padx=5, pady=5)

        info_text = f"Name: {name} | Code Rim: {code_rim} | Classroom: {classroom}"
        tk.Label(top_frame, text=info_text, font=("Arial", 12)).pack(anchor='center')

        # Bottom Frame for subjects details
        bottom_frame = ttk.Frame(self.result_frame)
        bottom_frame.pack(pady=10, fill='both', expand=True)

        row = 0
        col = 0
        self.subject_entries = {}  # To store references to the entries
        for subject in subjects_list:
            full_subject = self.subjects.get(subject.strip(), subject)

            # Use tk.Frame to set background color
            subject_frame = tk.Frame(bottom_frame, background="white")
            subject_frame.grid(row=row, column=col, padx=10, pady=10, sticky='w')

            tk.Label(subject_frame, text=f"{full_subject} ({subject.strip()})", font=("Arial", 12), background='#36C2CE').pack(side='top', pady=0, fill='x')

            tk.Label(subject_frame, text="Coefficient:", font=("Arial", 12), background="white").pack(side='left', padx=5)
            coef_entry = ttk.Entry(subject_frame, width=5, name=f"{subject.strip().lower()}_coef")
            coef_entry.pack(side='left', padx=5)

            tk.Label(subject_frame, text="Result:", font=("Arial", 12), background="white").pack(side='left', padx=5)
            result_entry = ttk.Entry(subject_frame, width=5, name=f"{subject.strip().lower()}_result")
            result_entry.pack(side='left', padx=5)

            # Store the entries in the dictionary
            self.subject_entries[subject.strip()] = {"coef": coef_entry, "result": result_entry}

            col += 1
            if col == 3:
                col = 0
                row += 1

        # Center the control frame and insert button
        self.control_frame.pack(anchor='center', pady=10)

        # Show control buttons
        self.control_frame.pack(pady=10)

    def insert_student_result(self):
        code_rim = self.code_rim_entry.get()
        if not code_rim:
            self.display_message("Please enter a code rim.")
            return

        examen_type = self.examen_type_combobox.get()  # Retrieve selected exam type
        if not examen_type:
            self.display_message("Please select an examen type.")
            return

        # Retrieve input values for subjects
        subject_values = {}
        for subject in self.subject_entries.keys():
            coef_entry = self.subject_entries[subject]["coef"]
            result_entry = self.subject_entries[subject]["result"]
            subject_values[subject] = {
                "coefficient": coef_entry.get(),
                "result": result_entry.get()
            }

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        try:
            # Get the student info to insert
            cursor.execute("SELECT name, classroom FROM students WHERE code_rim = ?", (code_rim,))
            student_info = cursor.fetchone()

            if not student_info:
                self.display_message("Student not found.")
                return

            name, classroom = student_info

            # Get the classroom subjects
            cursor.execute("SELECT subjects FROM classrooms WHERE title = ?", (classroom,))
            subjects_result = cursor.fetchone()

            if not subjects_result:
                self.display_message("Classroom not found or no subjects available.")
                return

            classroom_subjects = subjects_result[0].split(',')
            classroom_subjects = [subj.strip() for subj in classroom_subjects]

            # Construct the SQL query dynamically based on available subjects
            columns = ["student_code_rim", "student_name", "classroom", "examen_type"]
            values = [code_rim, name, classroom, examen_type]
            for subject in classroom_subjects:
                if subject in self.subject_entries.keys():
                    columns.append(subject)
                    columns.append(f"c_{subject}")
                    values.append(subject_values.get(subject, {}).get("result", 0))
                    values.append(subject_values.get(subject, {}).get("coefficient", 0))

            columns_str = ", ".join(columns)
            placeholders = ", ".join("?" * len(values))

            insert_query = f"""
                INSERT INTO results ({columns_str}) 
                VALUES ({placeholders})
            """
            cursor.execute(insert_query, values)
            conn.commit()

            self.display_message("Student result inserted successfully.")
        except sqlite3.Error as e:
            self.display_message(f"An error occurred: {e}")
        finally:
            conn.close()

    def edit_student_result(self):
        # Placeholder for edit function
        pass

    def delete_student_result(self):
        code_rim = self.code_rim_entry.get()
        if not code_rim:
            self.display_message("Please enter a code rim.")
            return

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM results WHERE student_code_rim = ?", (code_rim,))
            conn.commit()
            self.display_message("Student result deleted successfully.")
        except sqlite3.Error as e:
            self.display_message(f"An error occurred: {e}")
        finally:
            conn.close()
