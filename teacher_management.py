from tkinter import ttk, Tk, Frame, StringVar, Toplevel, END, Button
import sqlite3
from tkcalendar import DateEntry
from config import get_classroom_titles

class TeacherManagement:
    def __init__(self, frame):
        self.frame = frame

        # Create main frame with grid layout
        self.main_frame = Frame(self.frame)
        self.main_frame.grid(row=0, column=0, sticky='nsew')
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Create two blocks
        self.first_block = Frame(self.main_frame)
        self.first_block.grid(row=0, column=0, sticky='ns')
        self.second_block = Frame(self.main_frame)
        self.second_block.grid(row=0, column=1, sticky='nsew')

        # Configure column weight to make the second block expand
        self.main_frame.grid_columnconfigure(0, weight=0)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Registration frame
        self.registration_frame = Frame(self.first_block, padx=10, pady=10)
        self.registration_frame.pack(side='top', fill='x')
        self.registration_frame.grid_rowconfigure(6, weight=1)
        
        # Control buttons frame
        self.control_buttons_frame = Frame(self.first_block, padx=10, pady=10)
        self.control_buttons_frame.pack(side='bottom', fill='x')
        
        # Input fields and save button in registration frame
        ttk.Label(self.registration_frame, text='Name: ').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.name = ttk.Entry(self.registration_frame, width=30)
        self.name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.registration_frame, text='Gender: ').grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.gender = ttk.Combobox(self.registration_frame, values=["Male", "Female"], width=27)
        self.gender.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.registration_frame, text='Date of Register: ').grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.date_of_register = DateEntry(self.registration_frame, width=27)
        self.date_of_register.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.registration_frame, text='Classroom: ').grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.classroom = ttk.Combobox(self.registration_frame, values=get_classroom_titles(), width=27)
        self.classroom.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.registration_frame, text='Salary: ').grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.salary = ttk.Entry(self.registration_frame, width=30)
        self.salary.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(self.registration_frame, text='Number of Teachers: ').grid(row=6, column=0, padx=5, pady=5, sticky='w')
        self.number_of_teachers = ttk.Entry(self.registration_frame, width=30)
        self.number_of_teachers.grid(row=6, column=1, padx=5, pady=5)

        # Add button
        ttk.Button(self.registration_frame, text='Add', command=self.add_teacher).grid(row=7, columnspan=2, pady=10, sticky='we')

        # Treeview and control buttons in second block
        self.search_frame = Frame(self.second_block, padx=10, pady=10)
        self.search_frame.pack(side='top', fill='x')

        ttk.Label(self.search_frame, text='Search by Name: ').pack(side='left', padx=5)
        self.search_entry = ttk.Entry(self.search_frame, width=30)
        self.search_entry.pack(side='left', padx=5)
        ttk.Button(self.search_frame, text='Search', command=self.search_teacher).pack(side='left', padx=5)
        
        self.tree = ttk.Treeview(self.second_block, height=15, columns=('id', 'name', 'gender', 'date_of_register', 'classroom', 'salary', 'number_of_teachers'), show='headings')
        self.tree.pack(side='top', fill='both', expand=True)
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Name')
        self.tree.heading('gender', text='Gender')
        self.tree.heading('date_of_register', text='Date of Register')
        self.tree.heading('classroom', text='Classroom')
        self.tree.heading('salary', text='Salary')
        self.tree.heading('number_of_teachers', text='Number of Teachers')

        self.tree.column('id', width=50)
        self.tree.column('name', width=100)
        self.tree.column('gender', width=100)
        self.tree.column('date_of_register', width=100)
        self.tree.column('classroom', width=100)
        self.tree.column('salary', width=100)
        self.tree.column('number_of_teachers', width=150)

        # Buttons below the Treeview
        self.control_buttons_frame = Frame(self.second_block, padx=10, pady=10)
        self.control_buttons_frame.pack(side='bottom', fill='x')
        
        ttk.Button(self.control_buttons_frame, text='Edit', command=self.edit_teacher).pack(side='left', padx=5)
        ttk.Button(self.control_buttons_frame, text='Delete', command=self.delete_teacher).pack(side='left', padx=5)
        ttk.Button(self.control_buttons_frame, text='View', command=self.view_teacher).pack(side='left', padx=5)

        self.message = ttk.Label(self.second_block, text='', foreground='red')
        self.message.pack(pady=10)

        self.get_teachers()

    def run_query(self, query, parameters=()):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_teachers(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'SELECT * FROM teachers ORDER BY name DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 'end', values=row)

    def search_teacher(self):
        search_query = self.search_entry.get()
        query = 'SELECT * FROM teachers WHERE name LIKE ?'
        parameters = [f'%{search_query}%']
        db_rows = self.run_query(query, tuple(parameters))
        self.tree.delete(*self.tree.get_children())
        for row in db_rows:
            self.tree.insert('', 'end', values=row)

    def add_teacher(self):
        if self.validate():
            query = 'INSERT INTO teachers VALUES (NULL, ?, ?, ?, ?, ?, ?)'
            parameters = (self.name.get(), self.gender.get(), self.date_of_register.get(), self.classroom.get(), self.salary.get(), self.number_of_teachers.get())
            self.run_query(query, parameters)
            self.message['text'] = f'Teacher {self.name.get()} added successfully'
            self.get_teachers()
            self.clear_fields()
        else:
            self.message['text'] = 'All fields are required'

    def delete_teacher(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError:
            self.message['text'] = 'Please, select a record'
            return
        self.message['text'] = ''
        teacher_id = self.tree.item(self.tree.selection())['values'][0]
        query = 'DELETE FROM teachers WHERE id = ?'
        self.run_query(query, (teacher_id,))
        self.message['text'] = f'Teacher {teacher_id} deleted successfully'
        self.get_teachers()

    def edit_teacher(self):
        self.message['text'] = ''
        try:
            selected_item = self.tree.item(self.tree.selection())
            teacher_id = selected_item['values'][0]
            name = selected_item['values'][1]
            gender = selected_item['values'][2]
            date_of_register = selected_item['values'][3]
            classroom = selected_item['values'][4]
            salary = selected_item['values'][5]
            number_of_teachers = selected_item['values'][6]
        except IndexError:
            self.message['text'] = 'Please, select a record'
            return

        self.edit_window = Toplevel()
        self.edit_window.title('Edit Teacher')
        self.edit_window.resizable(False, False)

        # Center the window on the screen
        window_width = 310
        window_height = 260
        screen_width = self.edit_window.winfo_screenwidth()
        screen_height = self.edit_window.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.edit_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        ttk.Label(self.edit_window, text='Name: ').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.edit_name = ttk.Entry(self.edit_window, width=30)
        self.edit_name.grid(row=1, column=1, padx=5, pady=5)
        self.edit_name.insert(0, name)

        ttk.Label(self.edit_window, text='Gender: ').grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.edit_gender = ttk.Combobox(self.edit_window, values=["Male", "Female"], width=27)
        self.edit_gender.grid(row=2, column=1, padx=5, pady=5)
        self.edit_gender.set(gender)

        ttk.Label(self.edit_window, text='Date of Register: ').grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.edit_date_of_register = DateEntry(self.edit_window, width=27)
        self.edit_date_of_register.grid(row=3, column=1, padx=5, pady=5)
        self.edit_date_of_register.set_date(date_of_register)

        ttk.Label(self.edit_window, text='Classroom: ').grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.edit_classroom = ttk.Combobox(self.edit_window, width=27)
        self.edit_classroom.grid(row=4, column=1, padx=5, pady=5)
        self.edit_classroom.set(classroom)

        ttk.Label(self.edit_window, text='Salary: ').grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.edit_salary = ttk.Entry(self.edit_window, width=30)
        self.edit_salary.grid(row=5, column=1, padx=5, pady=5)
        self.edit_salary.insert(0, salary)

        ttk.Label(self.edit_window, text='Number of Teachers: ').grid(row=6, column=0, padx=5, pady=5, sticky='w')
        self.edit_number_of_teachers = ttk.Entry(self.edit_window, width=30)
        self.edit_number_of_teachers.grid(row=6, column=1, padx=5, pady=5)
        self.edit_number_of_teachers.insert(0, number_of_teachers)

        ttk.Button(self.edit_window, text='Save', command=lambda: self.save_changes(teacher_id)).grid(row=7, columnspan=2, pady=10, sticky='we')

    def save_changes(self, teacher_id):
        if self.validate_edit():
            query = 'UPDATE teachers SET name = ?, gender = ?, date_of_register = ?, classroom = ?, salary = ?, number_of_teachers = ? WHERE id = ?'
            parameters = (self.edit_name.get(), self.edit_gender.get(), self.edit_date_of_register.get(), self.edit_classroom.get(), self.edit_salary.get(), self.edit_number_of_teachers.get(), teacher_id)
            self.run_query(query, parameters)
            self.message['text'] = f'Teacher {teacher_id} updated successfully'
            self.get_teachers()
            self.edit_window.destroy()
        else:
            self.message['text'] = 'All fields are required'

    def validate(self):
        return all([self.name.get(), self.gender.get(), self.date_of_register.get(), self.classroom.get(), self.salary.get(), self.number_of_teachers.get()])

    def validate_edit(self):
        return all([self.edit_name.get(), self.edit_gender.get(), self.edit_date_of_register.get(), self.edit_classroom.get(), self.edit_salary.get(), self.edit_number_of_teachers.get()])

    def clear_fields(self):
        self.name.delete(0, END)
        self.gender.set('')
        self.date_of_register.set_date(None)
        self.classroom.set('')
        self.salary.delete(0, END)
        self.number_of_teachers.delete(0, END)

    def view_teacher(self):
        try:
            selected_item = self.tree.item(self.tree.selection())
            teacher_id = selected_item['values'][0]
            name = selected_item['values'][1]
            gender = selected_item['values'][2]
            date_of_register = selected_item['values'][3]
            classroom = selected_item['values'][4]
            salary = selected_item['values'][5]
            number_of_teachers = selected_item['values'][6]
        except IndexError:
            self.message['text'] = 'Please, select a record'
            return

        self.view_window = Toplevel()
        self.view_window.title('View Teacher')
        self.view_window.resizable(False, False)

        # Center the window on the screen
        window_width = 200
        window_height = 220
        screen_width = self.view_window.winfo_screenwidth()
        screen_height = self.view_window.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.view_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        ttk.Label(self.view_window, text='Name: ').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        ttk.Label(self.view_window, text=name).grid(row=1, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(self.view_window, text='Gender: ').grid(row=2, column=0, padx=5, pady=5, sticky='w')
        ttk.Label(self.view_window, text=gender).grid(row=2, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(self.view_window, text='Date of Register: ').grid(row=3, column=0, padx=5, pady=5, sticky='w')
        ttk.Label(self.view_window, text=date_of_register).grid(row=3, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(self.view_window, text='Classroom: ').grid(row=4, column=0, padx=5, pady=5, sticky='w')
        ttk.Label(self.view_window, text=classroom).grid(row=4, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(self.view_window, text='Salary: ').grid(row=5, column=0, padx=5, pady=5, sticky='w')
        ttk.Label(self.view_window, text=salary).grid(row=5, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(self.view_window, text='Number of Teachers: ').grid(row=6, column=0, padx=5, pady=5, sticky='w')
        ttk.Label(self.view_window, text=number_of_teachers).grid(row=6, column=1, padx=5, pady=5, sticky='w')

        ttk.Button(self.view_window, text='Close', command=self.view_window.destroy).grid(row=7, columnspan=2, pady=10, sticky='we')
