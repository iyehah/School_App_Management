import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class ClassroomManagement:
    def __init__(self, master):
        self.master = master

        # Initialize UI components
        self.init_ui()

    def init_ui(self):
        style = ttk.Style()
        style.configure("Treeview.Heading", bg="#4a4a4a",fieldbackground='red',font=('Arial', 10, 'bold'), anchor="center")
        style.configure("Treeview", rowheight=25 , borderwidth=5,relief="solid",bg="#4a4a4a")
        style.configure("Treeview.Cell", anchor="center")
        style.map("Treeview.Heading",background=[('active', 'blue')],foreground=[('active', 'green')])
        style.map('Treeview',
              background=[('selected', '#d9d9d9')],  # Background color for the selected row
              foreground=[('selected', 'black')])  # Text color for the selected row


        self.title_label = ttk.Label(self.master, text="Classroom Management", font=("Arial", 16),background='white')
        self.title_label.pack(pady=10 ,fill="x")

        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame for adding new classroom
        self.add_frame = ttk.LabelFrame(self.main_frame, text="Add New Classroom", padding=(10, 10))
        self.add_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10, anchor='n')

        ttk.Label(self.add_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.title_entry = ttk.Entry(self.add_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.add_frame, text="Level:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.level_var = tk.StringVar()
        self.level_combobox = ttk.Combobox(self.add_frame, textvariable=self.level_var, values=["At School", "Special"], width=28)
        self.level_combobox.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.add_frame, text="Type:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.type_var = tk.StringVar()
        self.type_combobox = ttk.Combobox(self.add_frame, textvariable=self.type_var, values=["Literary", "Scientific", "Professional", "Other"], width=28)
        self.type_combobox.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.add_frame, text="Subjects:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.subject_frame = tk.Frame(self.add_frame)
        self.subject_frame.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

        self.subject_vars = {}
        subjects = {
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

        for i, (abbr, full_name) in enumerate(subjects.items()):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(self.subject_frame, text=full_name, variable=var)
            cb.grid(row=i//2, column=i%2, sticky='w')
            self.subject_vars[abbr] = var

        self.save_button = ttk.Button(self.add_frame, text="Add", command=self.save_classroom)
        self.save_button.grid(row=4, columnspan=2, pady=20, sticky='we')

        # Frame for viewing classrooms
        self.view_frame = ttk.LabelFrame(self.main_frame, text="View Classrooms", padding=(10, 10))
        self.view_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.table_frame = tk.Frame(self.view_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        self.table = ttk.Treeview(self.table_frame, height= 10, columns=("ID", "Title", "Level", "Type", "Subjects"), show='headings',style='Treeview')
        self.table.heading("ID", text="ID")
        self.table.heading("Title", text="Title")
        self.table.heading("Level", text="Level")
        self.table.heading("Type", text="Type")
        self.table.heading("Subjects", text="Subjects")

        self.table.column("ID",width=50, anchor='center')
        self.table.column("Title",width=50, anchor='center')
        self.table.column("Level",width=100, anchor='center')
        self.table.column("Type",width=50, anchor='center')

        self.table.column("Subjects", anchor=tk.W)
        self.table.pack(fill="both", expand=True)

        self.table_scroll = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.table_scroll.pack(side='right', fill='y')
        self.table.configure(yscrollcommand=self.table_scroll.set)

        self.control_frame = tk.Frame(self.view_frame)
        self.control_frame.pack(pady=(10, 0))

        self.edit_button = ttk.Button(self.control_frame, text="Edit", command=self.edit_classroom)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ttk.Button(self.control_frame, text="Delete", command=self.delete_classroom)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.update_table()

    def update_table(self):
        """Update the table with classroom data from the database."""
        for row in self.table.get_children():
            self.table.delete(row)

        query = "SELECT * FROM classrooms"
        result = self.run_query(query)

        for row in result:
            self.table.insert("", tk.END, values=row)

    def run_query(self, query, parameters=()):
        """Run a query and return the result."""
        db_path = 'database.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            result = cursor.execute(query, parameters)
            conn.commit()
            return result.fetchall()
        finally:
            conn.close()

    def save_classroom(self):
        """Save classroom data to the database."""
        title = self.title_entry.get()
        level = self.level_var.get()
        type_ = self.type_var.get()

        if not title or not level or not type_:
            messagebox.showerror("Input Error", "Please fill in all fields")
            return

        subjects = [abbr for abbr, var in self.subject_vars.items() if var.get()]
        subjects_str = ', '.join(subjects)

        query = '''
        INSERT INTO classrooms (title, level, type, subjects)
        VALUES (?, ?, ?, ?)
        '''
        parameters = (title, level, type_, subjects_str)
        self.run_query(query, parameters)
        self.update_table()
        self.clear_fields()

    def clear_fields(self):
        """Clear all input fields."""
        self.title_entry.delete(0, tk.END)
        self.level_var.set("")
        self.type_var.set("")
        for var in self.subject_vars.values():
            var.set(False)

    def edit_classroom(self):
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a classroom to edit")
            return
        
        item = self.table.item(selected_item)
        classroom_id, title, level, type_, subjects = item['values']

        # Set the fields with the selected data
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, title)
        self.level_var.set(level)
        self.type_var.set(type_)
        
        for subject in self.subject_vars.keys():
            self.subject_vars[subject].set(False)
        
        selected_subjects = subjects.split(', ')
        for subject in selected_subjects:
            if subject in self.subject_vars:
                self.subject_vars[subject].set(True)

        def save_edited_classroom():
            new_title = self.title_entry.get()
            new_level = self.level_var.get()
            new_type = self.type_var.get()

            if not new_title or not new_level or not new_type:
                messagebox.showerror("Input Error", "Please fill in all fields")
                return

            new_subjects = [abbr for abbr, var in self.subject_vars.items() if var.get()]
            new_subjects_str = ', '.join(new_subjects)

            query = '''
            UPDATE classrooms
            SET title = ?, level = ?, type = ?, subjects = ?
            WHERE id = ?
            '''
            parameters = (new_title, new_level, new_type, new_subjects_str, classroom_id)
            self.run_query(query, parameters)
            self.update_table()
            self.clear_fields()
            self.save_button.config(text="Add", command=self.save_classroom)

        self.save_button.config(text="Update", command=save_edited_classroom)

    def delete_classroom(self):
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a classroom to delete")
            return
        
        item = self.table.item(selected_item)
        classroom_id = item['values'][0]

        query = "DELETE FROM classrooms WHERE id = ?"
        parameters = (classroom_id,)
        self.run_query(query, parameters)
        self.update_table()

# Testing the UI
if __name__ == "__main__":
    root = tk.Tk()
    root.title("School Management System")
    root.geometry("1000x600")
    ClassroomManagement(root)
    root.mainloop()
