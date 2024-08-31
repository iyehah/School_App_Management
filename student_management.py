from tkinter import ttk, Tk, Frame, StringVar, Toplevel, END, Button
import sqlite3
from tkcalendar import DateEntry
from config import get_classroom_titles

class StudentManagement:
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
        self.registration_frame.grid_rowconfigure(7, weight=1)
        
        # Control buttons frame
        self.control_buttons_frame = Frame(self.first_block, padx=10, pady=10)
        self.control_buttons_frame.pack(side='bottom', fill='x')
        
        # Input fields and save button in registration frame
        ttk.Label(self.registration_frame, text='Name: ').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.name = ttk.Entry(self.registration_frame, width=30)
        self.name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.registration_frame, text='Code Rim: ').grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.code_rim = ttk.Entry(self.registration_frame, width=30)
        self.code_rim.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.registration_frame, text='Gender: ').grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.gender = ttk.Combobox(self.registration_frame, values=["Male", "Female"], width=27)
        self.gender.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.registration_frame, text='Date of Register: ').grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.date_of_register = DateEntry(self.registration_frame, width=27)
        self.date_of_register.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.registration_frame, text='Classroom: ').grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.classroom = ttk.Combobox(self.registration_frame, values=get_classroom_titles(), width=27)
        self.classroom.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(self.registration_frame, text='Price: ').grid(row=6, column=0, padx=5, pady=5, sticky='w')
        self.price = ttk.Entry(self.registration_frame, width=30)
        self.price.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(self.registration_frame, text='Number of Agent: ').grid(row=7, column=0, padx=5, pady=5, sticky='w')
        self.number_of_agent = ttk.Entry(self.registration_frame, width=30)
        self.number_of_agent.grid(row=7, column=1, padx=5, pady=5)

        # Add button
        ttk.Button(self.registration_frame, text='Add', command=self.add_student).grid(row=8, columnspan=2, pady=10, sticky='we')

        # Treeview and control buttons in second block
        self.search_frame = Frame(self.second_block, padx=10, pady=10)
        self.search_frame.pack(side='top', fill='x')

        ttk.Label(self.search_frame, text='Search by Code Rim: ').pack(side='left', padx=5)
        self.search_entry = ttk.Entry(self.search_frame, width=30)
        self.search_entry.pack(side='left', padx=5)
        ttk.Button(self.search_frame, text='Search', command=self.search_student).pack(side='left', padx=5)

        ttk.Label(self.search_frame, text='Filter by Date : ').pack(side='left', padx=5)
        self.filter_date = DateEntry(self.search_frame, width=12)
        self.filter_date.pack(side='left', padx=5)
        ttk.Button(self.search_frame, text='Filter by Date', command=self.filter_by_date).pack(side='left', padx=5)

        classroom_titles = get_classroom_titles()
        classroom_titles.insert(0, " ")  # Insert " " at the first option 

        ttk.Label(self.search_frame, text='Filter by Class: ').pack(side='left', padx=5)
        self.filter_classroom = ttk.Combobox(self.search_frame, values= classroom_titles, width=15)
        self.filter_classroom.pack(side='left', padx=5)
        self.filter_classroom.set("")
        ttk.Button(self.search_frame, text='Filter by Classroom', command=self.filter_by_classroom).pack(side='left', padx=5)

        self.tree = ttk.Treeview(self.second_block, height=15, columns=('id', 'name', 'code_rim', 'gender', 'date_of_register', 'classroom', 'price', 'number_of_agent'), show='headings')
        self.tree.pack(side='top', fill='both', expand=True)
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Name')
        self.tree.heading('code_rim', text='Code Rim')
        self.tree.heading('gender', text='Gender')
        self.tree.heading('date_of_register', text='Date of Register')
        self.tree.heading('classroom', text='Classroom')
        self.tree.heading('price', text='Price')
        self.tree.heading('number_of_agent', text='Number of Agent')

        self.tree.column('id', width=50)
        self.tree.column('name', width=100)
        self.tree.column('code_rim', width=100)
        self.tree.column('gender', width=100)
        self.tree.column('date_of_register', width=100)
        self.tree.column('classroom', width=100)
        self.tree.column('price', width=100)
        self.tree.column('number_of_agent', width=100)

        # Buttons below the Treeview
        self.control_buttons_frame = Frame(self.second_block, padx=10, pady=10)
        self.control_buttons_frame.pack(side='bottom', fill='x')
        
        ttk.Button(self.control_buttons_frame, text='Edit', command=self.edit_student).pack(side='left', padx=5)
        ttk.Button(self.control_buttons_frame, text='Delete', command=self.delete_student).pack(side='left', padx=5)
        ttk.Button(self.control_buttons_frame, text='View', command=self.view_student).pack(side='left', padx=5)

        self.message = ttk.Label(self.second_block, text='', foreground='red')
        self.message.pack(pady=10)

        self.get_students()

    def run_query(self, query, parameters=()):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_students(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'SELECT * FROM students ORDER BY name DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 'end', values=row)

    def search_student(self):
        search_query = self.search_entry.get()
        query = 'SELECT * FROM students WHERE code_rim LIKE ?'
        parameters = [f'%{search_query}%']
        db_rows = self.run_query(query, tuple(parameters))
        self.tree.delete(*self.tree.get_children())
        for row in db_rows:
            self.tree.insert('', 'end', values=row)

    def filter_by_date(self):
        date_filter = self.filter_date.get()
        query = 'SELECT * FROM students WHERE date_of_register = ?'
        parameters = [date_filter]
        db_rows = self.run_query(query, tuple(parameters))
        self.tree.delete(*self.tree.get_children())
        for row in db_rows:
            self.tree.insert('', 'end', values=row)

    def filter_by_classroom(self):
        classroom_filter = self.filter_classroom.get()
        query = 'SELECT * FROM students WHERE classroom = ?'
        parameters = [classroom_filter]
        db_rows = self.run_query(query, tuple(parameters))
        self.tree.delete(*self.tree.get_children())
        for row in db_rows:
            self.tree.insert('', 'end', values=row)

    def add_student(self):
        if self.validate():
            query = 'INSERT INTO students VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)'
            parameters = (self.name.get(), self.code_rim.get(), self.gender.get(), self.date_of_register.get(), self.classroom.get(), self.price.get(), self.number_of_agent.get())
            self.run_query(query, parameters)
            self.message['text'] = f'Student {self.name.get()} added successfully'
            self.get_students()
            self.clear_fields()
        else:
            self.message['text'] = 'All fields are required'

    def delete_student(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError:
            self.message['text'] = 'Please, select a record'
            return
        self.message['text'] = ''
        student_id = self.tree.item(self.tree.selection())['values'][0]
        query = 'DELETE FROM students WHERE id = ?'
        self.run_query(query, (student_id,))
        self.message['text'] = f'Student {student_id} deleted successfully'
        self.get_students()

    def edit_student(self):
        self.message['text'] = ''
        try:
            selected_item = self.tree.item(self.tree.selection())
            student_id = selected_item['values'][0]
            name = selected_item['values'][1]
            code_rim = selected_item['values'][2]
            gender = selected_item['values'][3]
            date_of_register = selected_item['values'][4]
            classroom = selected_item['values'][5]
            price = selected_item['values'][6]
            number_of_agent = selected_item['values'][7]
        except IndexError:
            self.message['text'] = 'Please, select a record'
            return

        self.edit_window = Toplevel()
        self.edit_window.title('Edit Student')
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
        new_name = ttk.Entry(self.edit_window, width=30)
        new_name.grid(row=1, column=1, padx=5, pady=5)
        new_name.insert(0, name)

        ttk.Label(self.edit_window, text='Code Rim: ').grid(row=2, column=0, padx=5, pady=5, sticky='w')
        new_code_rim = ttk.Entry(self.edit_window, width=30)
        new_code_rim.grid(row=2, column=1, padx=5, pady=5)
        new_code_rim.insert(0, code_rim)

        ttk.Label(self.edit_window, text='Gender: ').grid(row=3, column=0, padx=5, pady=5, sticky='w')
        new_gender = ttk.Combobox(self.edit_window, values=["Male", "Female"], width=27)
        new_gender.grid(row=3, column=1, padx=5, pady=5)
        new_gender.set(gender)

        ttk.Label(self.edit_window, text='Date of Register: ').grid(row=4, column=0, padx=5, pady=5, sticky='w')
        new_date_of_register = DateEntry(self.edit_window, width=27)
        new_date_of_register.grid(row=4, column=1, padx=5, pady=5)
        new_date_of_register.set_date(date_of_register)

        ttk.Label(self.edit_window, text='Classroom: ').grid(row=5, column=0, padx=5, pady=5, sticky='w')
        new_classroom = ttk.Combobox(self.edit_window, values=get_classroom_titles(), width=27)
        new_classroom.grid(row=5, column=1, padx=5, pady=5)
        new_classroom.set(classroom)

        ttk.Label(self.edit_window, text='Price: ').grid(row=6, column=0, padx=5, pady=5, sticky='w')
        new_price = ttk.Entry(self.edit_window, width=30)
        new_price.grid(row=6, column=1, padx=5, pady=5)
        new_price.insert(0, price)

        ttk.Label(self.edit_window, text='Number of Agent: ').grid(row=7, column=0, padx=5, pady=5, sticky='w')
        new_number_of_agent = ttk.Entry(self.edit_window, width=30)
        new_number_of_agent.grid(row=7, column=1, padx=5, pady=5)
        new_number_of_agent.insert(0, number_of_agent)

        # Custom style for the Update button
        style = ttk.Style()
        style.configure('Custom.TButton')

        def update_and_close():
            self.update_student(new_name.get(), new_code_rim.get(), new_gender.get(), new_date_of_register.get(), new_classroom.get(), new_price.get(), new_number_of_agent.get(), student_id)
            self.edit_window.destroy()

        ttk.Button(self.edit_window, text='Update', command=update_and_close, style='Custom.TButton').grid(row=8, columnspan=2, pady=10, sticky='we')


    def update_student(self, name, code_rim, gender, date_of_register, classroom, price, number_of_agent, student_id):
        query = 'UPDATE students SET name = ?, code_rim = ?, gender = ?, date_of_register = ?, classroom = ?, price = ?, number_of_agent = ? WHERE id = ?'
        parameters = (name, code_rim, gender, date_of_register, classroom, price, number_of_agent, student_id)
        self.run_query(query, parameters)
        self.edit_window.destroy()
        self.message['text'] = f'Student {student_id} updated successfully'
        self.get_students()

    def view_student(self):
        self.message['text'] = ''
        try:
            selected_item = self.tree.item(self.tree.selection())
            student_id = selected_item['values'][0]
            name = selected_item['values'][1]
            code_rim = selected_item['values'][2]
            gender = selected_item['values'][3]
            date_of_register = selected_item['values'][4]
            classroom = selected_item['values'][5]
            price = selected_item['values'][6]
            number_of_agent = selected_item['values'][7]
        except IndexError:
            self.message['text'] = 'Please, select a record'
            return

        self.view_window = Toplevel()
        self.view_window.title('View Student')

        ttk.Label(self.view_window, text=f'Name: {name}').pack(pady=5)
        ttk.Label(self.view_window, text=f'Code Rim: {code_rim}').pack(pady=5)
        ttk.Label(self.view_window, text=f'Gender: {gender}').pack(pady=5)
        ttk.Label(self.view_window, text=f'Date of Register: {date_of_register}').pack(pady=5)
        ttk.Label(self.view_window, text=f'Classroom: {classroom}').pack(pady=5)
        ttk.Label(self.view_window, text=f'Price: {price}').pack(pady=5)
        ttk.Label(self.view_window, text=f'Number of Agent: {number_of_agent}').pack(pady=5)

    def validate(self):
        return len(self.name.get()) != 0 and len(self.code_rim.get()) != 0 and len(self.gender.get()) != 0 and len(self.date_of_register.get()) != 0 and len(self.classroom.get()) != 0 and len(self.price.get()) != 0 and len(self.number_of_agent.get()) != 0

    def clear_fields(self):
        self.name.delete(0, END)
        self.code_rim.delete(0, END)
        self.gender.set('')
        self.date_of_register.set_date(None)  # Use None to clear the DateEntry widget
        self.classroom.set('')
        self.classroom.set('')
        self.price.delete(0, END)
        self.number_of_agent.delete(0, END)

if __name__ == '__main__':
    root = Tk()
    application = StudentManagement(root)
    root.mainloop()
