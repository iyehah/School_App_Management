# export_students.py
import pandas as pd
import sqlite3
from tkinter import filedialog, messagebox

def export_students_data():
    try:
        # Connect to the database
        conn = sqlite3.connect('database.db')
        query = "SELECT * FROM students"

        # Fetch data from the students table
        df = pd.read_sql_query(query, conn)

        # Close the database connection
        conn.close()

        # Open a file dialog to choose the file location and name
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Save As"
        )

        if not file_path:
            return  # User cancelled the file dialog

        # Save the data to the chosen Excel file
        df.to_excel(file_path, index=False)

        messagebox.showinfo("Success", f"Data exported successfully to {file_path}!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
