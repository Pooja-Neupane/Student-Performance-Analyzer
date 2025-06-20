import tkinter as tk
from tkinter import ttk, messagebox, filedialog
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
            "Marks": [", ".join(map(str, s.marks)) for s in self.students],
            "Average": [round(s.average, 2) for s in self.students],
            "Grade": [s.grade for s in self.students]
        }
        return pd.DataFrame(data)

    def export_to_csv(self, filepath):
        df = self.get_data_frame()
        df.to_csv(filepath, index=False)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Student Performance Analyzer")
        self.root.geometry("650x400")
        self.manager = StudentManager()

        self.name_var = tk.StringVar()
        self.marks_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.LabelFrame(self.root, text="Enter Student Details", padding=10)
        frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame, text="👤 Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="✏️ Marks (comma-separated):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.marks_var, width=30).grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame, text="➕ Add Student", command=self.add_student).grid(row=2, column=0, columnspan=2, pady=10)

        # Treeview for table
        columns = ("Name", "Marks", "Average", "Grade")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(pady=10, fill="both", expand=True)

        # Export Button
        ttk.Button(self.root, text="💾 Export to CSV", command=self.export_csv).pack(pady=5)

    def add_student(self):
        name = self.name_var.get().strip()
        marks_input = self.marks_var.get().strip()

        try:
            marks = list(map(int, marks_input.split(',')))
            if not name or not marks:
                raise ValueError("Missing input")
        except:
            messagebox.showerror("Input Error", "Please enter a valid name and comma-separated numeric marks.")
            return

        self.manager.add_student(name, marks)
        self.update_tree()

        self.name_var.set("")
        self.marks_var.set("")

    def update_tree(self):
        self.tree.delete(*self.tree.get_children())

        df = self.manager.get_data_frame()
        for _, row in df.iterrows():
            self.tree.insert("", tk.END, values=(row["Name"], row["Marks"], row["Average"], row["Grade"]))

    def export_csv(self):
        if not self.manager.students:
            messagebox.showwarning("No Data", "No student data to export.")
            return
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save as"
        )
        if filepath:
            self.manager.export_to_csv(filepath)
            messagebox.showinfo("Export Successful", f"Student data exported to:\n{filepath}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
