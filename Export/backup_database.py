import shutil
import os
from tkinter import filedialog, messagebox

def backup_database():
    # Select a directory to save the backup
    backup_dir = filedialog.askdirectory(title="Select Backup Directory")
    if backup_dir:
        try:
            # Copy the database to the selected directory
            shutil.copy('database.db', os.path.join(backup_dir, 'database_backup.db'))
            messagebox.showinfo("Success", "Database backup created successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create backup: {e}")
