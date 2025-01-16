import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Initialize database
def initialize_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            student_id TEXT NOT NULL UNIQUE,
            class TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Add student record
def add_student():
    name = name_entry.get()
    student_id = student_id_entry.get()
    student_class = class_entry.get()
    age = age_entry.get()

    if not (name and student_id and student_class and age.isdigit()):
        messagebox.showerror("Error", "All fields must be filled correctly!")
        return

    try:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, student_id, class, age) VALUES (?, ?, ?, ?)",
            (name, student_id, student_class, int(age))
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student added successfully!")
        display_students()
        clear_inputs()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Student ID must be unique!")

# Display students
def display_students():
    for row in student_table.get_children():
        student_table.delete(row)

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()
    conn.close()

    for record in records:
        student_table.insert("", "end", values=record)

# Delete student record
def delete_student():
    selected_item = student_table.selection()
    if not selected_item:
        messagebox.showerror("Error", "No student selected!")
        return

    student_id = student_table.item(selected_item, "values")[1]
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Student deleted successfully!")
    display_students()

# Clear input fields
def clear_inputs():
    name_entry.delete(0, tk.END)
    student_id_entry.delete(0, tk.END)
    class_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)

# Initialize GUI application
app = tk.Tk()
app.title("Student Records Management")
app.geometry("600x400")

# Input Frame
input_frame = tk.Frame(app)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(input_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Student ID:").grid(row=1, column=0, padx=5, pady=5)
student_id_entry = tk.Entry(input_frame)
student_id_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Class:").grid(row=2, column=0, padx=5, pady=5)
class_entry = tk.Entry(input_frame)
class_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Age:").grid(row=3, column=0, padx=5, pady=5)
age_entry = tk.Entry(input_frame)
age_entry.grid(row=3, column=1, padx=5, pady=5)

# Buttons
button_frame = tk.Frame(app)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Student", command=add_student).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Delete Student", command=delete_student).grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="Clear Inputs", command=clear_inputs).grid(row=0, column=2, padx=10)

# Table Frame
table_frame = tk.Frame(app)
table_frame.pack(pady=10)

columns = ("ID", "Student ID", "Name", "Class", "Age")
student_table = ttk.Treeview(table_frame, columns=columns, show="headings")
for col in columns:
    student_table.heading(col, text=col)
    student_table.column(col, anchor=tk.CENTER)

student_table.pack(fill=tk.BOTH, expand=True)

# Initialize database and display existing records
initialize_db()
display_students()

# Run the application
app.mainloop()
