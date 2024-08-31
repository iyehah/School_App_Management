import sys
import tkinter as tk
from tkinter import ttk
import dashboard
import student_management
import results_management  # Updated import
import teacher_management
import classroom_management
import settings  # Import the settings module

class SchoolManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("School Management System")

        # Get the screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set window size to the screen dimensions
        self.root.geometry(f"{screen_width}x{screen_height}")

        # Configure the style for the notebook and tabs
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[10, 5], font=('Arial', 12))
        style.configure('TNotebook', background='#f0f0f0')
        style.map('TNotebook.Tab',
                  background=[('selected', '#d0d0d0')],
                  foreground=[('selected', 'black')],
                  relief=[('selected', 'flat')],
                  )

        # Create a Notebook widget to hold the tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Create frames for each tab
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.student_management_frame = ttk.Frame(self.notebook)
        self.teacher_management_frame = ttk.Frame(self.notebook)
        self.classroom_management_frame = ttk.Frame(self.notebook)
        self.results_management_frame = ttk.Frame(self.notebook)  # Updated frame name
        self.settings_frame = ttk.Frame(self.notebook)

        # Add frames as tabs to the notebook
        self.notebook.add(self.dashboard_frame, text="Dashboard")
        self.notebook.add(self.student_management_frame, text="Student Management")
        self.notebook.add(self.teacher_management_frame, text="Teacher Management")
        self.notebook.add(self.classroom_management_frame, text="Classroom Management")
        self.notebook.add(self.results_management_frame, text="Results Management")  # Updated tab label
        self.notebook.add(self.settings_frame, text="Settings")

        # Initialize the UI for each tab
        dashboard.Dashboard(self.dashboard_frame)
        student_management.StudentManagement(self.student_management_frame)
        teacher_management.TeacherManagement(self.teacher_management_frame)
        classroom_management.ClassroomManagement(self.classroom_management_frame)
        results_management.ResultsManagement(self.results_management_frame)  # Updated class name
        settings.Settings(self.settings_frame)  # Initialize the Settings UI

        # Bind the close event to the exit function
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # Perform any cleanup tasks here
        print("Closing application...")  # For debugging
        self.root.destroy()
        sys.exit()  # Ensure the application exits completely

if __name__ == "__main__":
    window = tk.Tk()
    app = SchoolManagementSystem(window)
    window.mainloop()
