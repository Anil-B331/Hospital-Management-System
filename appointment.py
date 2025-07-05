import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

def add_appointment_to_db(name, age, gender, location, appointment_date, scheduled_time, phone):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO appointments (name, age, gender, location, appointment_date, scheduled_time, phone) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (name, age, gender, location, appointment_date, scheduled_time, phone)
    )
    conn.commit()
    conn.close()

# Database setup
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS appointments (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age TEXT,
    gender TEXT,
    location TEXT,
    scheduled_time TEXT,
    phone TEXT,
    appointment_date TEXT
)
''')
conn.commit()

class AppointmentApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("G&G Hospital Appointments")
        self.geometry("900x600")
        self.resizable(False, False)
        self.configure(bg="#f4f6fb")

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TLabel', font=('Segoe UI', 12), background='#f4f6fb')
        style.configure('TEntry', font=('Segoe UI', 12))
        style.configure('TButton', font=('Segoe UI', 12, 'bold'), padding=8)
        style.configure('Accent.TButton', font=('Segoe UI', 12, 'bold'), background='#457b9d', foreground='white')
        style.map('Accent.TButton', background=[('active', '#1d3557')])

        # Main frame
        main_frame = ttk.Frame(self, padding=30, style='TFrame')
        main_frame.pack(fill='both', expand=True)

        # Heading
        heading = ttk.Label(main_frame, text="G&G Hospital Appointments", font=('Segoe UI', 26, 'bold'), foreground='#1d3557')
        heading.grid(row=0, column=0, columnspan=2, pady=(0, 30))

        # Form labels and entries
        labels = [
            "Patient's Name", "Age", "Gender", "Location",
            "Appointment Date", "Appointment Time", "Phone Number"
        ]
        self.entries = []
        for i, label in enumerate(labels):
            ttk.Label(main_frame, text=label).grid(row=i+1, column=0, sticky='e', pady=10, padx=(0, 15))
            entry = ttk.Entry(main_frame, width=30)
            entry.grid(row=i+1, column=1, sticky='w', pady=10)
            self.entries.append(entry)

        # Add Appointment Button
        add_btn = ttk.Button(main_frame, text="Add Appointment", style='Accent.TButton', command=self.add_appointment)
        add_btn.grid(row=8, column=0, columnspan=2, pady=(20, 10))

        # Log area
        ttk.Label(main_frame, text="Logs", font=('Segoe UI', 14, 'bold'), foreground='#457b9d').grid(row=9, column=0, columnspan=2, pady=(30, 10))
        self.log_box = tk.Text(main_frame, width=60, height=6, font=('Segoe UI', 11), bg='#e9ecef', fg='#212529', borderwidth=0)
        self.log_box.grid(row=10, column=0, columnspan=2, pady=(0, 10))
        self.update_log()

        # Enter key navigation
        for i, entry in enumerate(self.entries):
            if i < len(self.entries) - 1:
                entry.bind("<Return>", lambda e, next_entry=self.entries[i+1]: next_entry.focus_set())
            else:
                entry.bind("<Return>", lambda e: add_btn.invoke())

    def add_appointment(self):
        vals = [e.get() for e in self.entries]
        if any(v.strip() == '' for v in vals):
            messagebox.showinfo("Warning", "Please Fill Up All Boxes")
            return
        add_appointment_to_db(*vals)
        messagebox.showinfo("Success", f"Appointment for {vals[0]} has been created")
        self.log_box.insert(tk.END, f'Appointment fixed for {vals[0]} on {vals[4]} at {vals[5]}\n')
        self.update_log()
        for e in self.entries:
            e.delete(0, tk.END)

    def update_log(self):
        c.execute("SELECT COUNT(*) FROM appointments")
        total = c.fetchone()[0]
        self.log_box.delete(1.0, tk.END)
        self.log_box.insert(tk.END, f"Total Appointments till now: {total}\n")

if __name__ == "__main__":
    app = AppointmentApp()
    app.mainloop()