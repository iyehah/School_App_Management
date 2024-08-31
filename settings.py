import tkinter as tk
from tkinter import ttk
from Export.export_students import export_students_data
from Export.export_teachers import export_teachers_data
from Export.export_classrooms import export_classrooms_data
from Export.backup_database import backup_database
from Import.import_students import import_students_data
from Import.import_teachers import import_teachers_data
from Import.import_classrooms import import_classrooms_data
from Import.import_database import import_database

class Settings:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Create the General Data Settings frame
        self.data_settings_frame = ttk.Labelframe(self.frame, text="Data Settings")
        self.data_settings_frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Note recommending regular backups
        self.note_label = ttk.Label(
            self.data_settings_frame,
            text="Note: We recommend that you keep a copy of the database on a regular basis for fear of data loss."
        )
        self.note_label.pack(pady=5)

        # Create the Import and Export Data frame within Data Settings
        self.import_export_frame = ttk.Frame(self.data_settings_frame)
        self.import_export_frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Import Data Section
        self.import_label = ttk.Label(self.import_export_frame, text="Import Data")
        self.import_label.grid(row=0, column=0, padx=5, pady=5)

        self.import_students_button = ttk.Button(self.import_export_frame, text="Import Students", command=import_students_data)
        self.import_students_button.grid(row=1, column=0, padx=5, pady=5)

        self.import_teachers_button = ttk.Button(self.import_export_frame, text="Import Teachers", command=import_teachers_data)
        self.import_teachers_button.grid(row=2, column=0, padx=5, pady=5)

        self.import_classrooms_button = ttk.Button(self.import_export_frame, text="Import Classrooms", command=import_classrooms_data)
        self.import_classrooms_button.grid(row=3, column=0, padx=5, pady=5)

        self.import_db_button = ttk.Button(self.import_export_frame, text="Import Database", command=import_database)
        self.import_db_button.grid(row=4, column=0, padx=5, pady=5)

        # Export Data Section
        self.export_label = ttk.Label(self.import_export_frame, text="Export Data")
        self.export_label.grid(row=0, column=1, padx=5, pady=5)

        self.export_students_button = ttk.Button(self.import_export_frame, text="Export Students", command=export_students_data)
        self.export_students_button.grid(row=1, column=1, padx=5, pady=5)

        self.export_teachers_button = ttk.Button(self.import_export_frame, text="Export Teachers", command=export_teachers_data)
        self.export_teachers_button.grid(row=2, column=1, padx=5, pady=5)

        self.export_classrooms_button = ttk.Button(self.import_export_frame, text="Export Classrooms", command=export_classrooms_data)
        self.export_classrooms_button.grid(row=3, column=1, padx=5, pady=5)

        self.backup_db_button = ttk.Button(self.import_export_frame, text="Backup Database", command=backup_database)
        self.backup_db_button.grid(row=4, column=1, padx=5, pady=5)