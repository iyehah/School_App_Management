# import/import_classrooms.py
import pandas as pd
import sqlite3
from tkinter import filedialog, messagebox

def import_classrooms_data():
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
                INSERT OR REPLACE INTO classrooms (
                    id, title, level, type, subjects
                ) VALUES (?, ?, ?, ?, ?)
            ''', (row.get('id'), row.get('title'), row.get('level'), row.get('type'), row.get('subjects')))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Classrooms data imported successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
