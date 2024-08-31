# import/import_students.py
import pandas as pd
import sqlite3
from tkinter import filedialog, messagebox

def import_students_data():
    try:
        # Open a file dialog to choose the Excel file
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx")],
            title="Open Excel File"
        )

        if not file_path:
            return  # User cancelled the file dialog

        # Read data from the chosen Excel file
        df = pd.read_excel(file_path)

        # Connect to the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Iterate over the DataFrame and insert each row into the database
        for index, row in df.iterrows():
            cursor.execute('''
                INSERT OR REPLACE INTO students (
                    id, name, code_rim, gender, date_of_register, classroom, price, number_of_agent
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (row.get('id'), row.get('name'), row.get('code_rim'), row.get('gender'),
                  row.get('date_of_register'), row.get('classroom'), row.get('price'),
                  row.get('number_of_agent')))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Data imported successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
