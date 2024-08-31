import shutil
from tkinter import filedialog, messagebox

def import_database():
    # Select a database file to import
    db_file = filedialog.askopenfilename(title="Select Database File", filetypes=[("Database Files", "*.db")])
    if db_file:
        try:
            # Copy the selected database file to replace the existing one
            shutil.copy(db_file, 'database.db')
            messagebox.showinfo("Success", "Database imported successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import database: {e}")
