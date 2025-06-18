import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd


class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = np.array(marks)
        self.average = self.calculate_average()
        self.grade = self.calculate_grade()

    def calculate_average(self):
        return np.mean(self.marks)

    def calculate_grade(self):
        avg = self.average
        if avg >= 90:
            return "A+"
        elif avg >= 80:
            return "A"
        elif avg >= 70:
            return "B+"
        elif avg >= 60:
            return "B"
        elif avg >= 50:
            return "C"
        else:
            return "F"


class StudentManager:
    def __init__(self):
        self.students = []

    def add_student(self, name, marks):
        student = Student(name, marks)
        self.students.append(student)

    def get_data_frame(self):
        data = {
            "Name": [s.name for s in self.students],
            "Marks": [list(s.marks) for s in self.students],
            "Average": [round(s.average, 2) for s in self.students],
            "Grade": [s.grade for s in self.students]
        }
        return pd.DataFrame(data)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Performance Analyzer")
        self.manager = StudentManager()

        self.name_var = tk.StringVar()
        self.marks_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Name:").grid(row=0, column=0, padx=5)
        tk.Entry(frame, textvariable=self.name_var).grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Marks (comma-separated):").grid(row=1, column=0, padx=5)
        tk.Entry(frame, textvariable=self.marks_var).grid(row=1, column=1, padx=5)

        tk.Button(frame, text="Add Student", command=self.add_student).grid(row=2, column=0, columnspan=2, pady=5)

        self.tree = ttk.Treeview(self.root, columns=("Name", "Marks", "Average", "Grade"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10)

    def add_student(self):
        name = self.name_var.get().strip()
        marks_input = self.marks_var.get().strip()

        try:
            marks = list(map(int, marks_input.split(',')))
            if not name or not marks:
                raise ValueError
        except:
            messagebox.showerror("Input Error", "Please enter valid name and marks.")
            return

        self.manager.add_student(name, marks)
        self.update_tree()

        self.name_var.set("")
        self.marks_var.set("")

    def update_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        df = self.manager.get_data_frame()
        for _, row in df.iterrows():
            self.tree.insert("", tk.END, values=(row["Name"], row["Marks"], row["Average"], row["Grade"]))


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
