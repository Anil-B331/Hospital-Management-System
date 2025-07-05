import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import pyttsx3

from appointment import add_appointment_to_db
from display import get_all_appointments
from update import update_appointment, delete_appointment

class AppointmentApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hospital Management System")
        self.geometry("1100x700")
        self.resizable(True, True)
        try:
            self.state('zoomed')
        except Exception:
            pass

        # Menu for window actions
        menubar = tk.Menu(self)
        window_menu = tk.Menu(menubar, tearoff=0)
        window_menu.add_command(label="Minimize", command=self.iconify)
        window_menu.add_command(label="Cascade", command=self.cascade_window)
        menubar.add_cascade(label="Window", menu=window_menu)
        self.config(menu=menubar)

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TNotebook.Tab', font=('Segoe UI', 14, 'bold'), padding=[20, 10])
        style.configure('TButton', font=('Segoe UI', 12), padding=10)
        style.configure('TLabel', font=('Segoe UI', 12))
        style.configure('TEntry', font=('Segoe UI', 12))
        style.configure('TFrame', background='#f4f6fb')
        style.configure('TText', font=('Segoe UI', 12))

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        self.add_frame = ttk.Frame(self.notebook)
        self.display_frame = ttk.Frame(self.notebook)
        self.update_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.add_frame, text='Add Appointment')
        self.notebook.add(self.display_frame, text='Display Appointments')
        self.notebook.add(self.update_frame, text='Update/Delete Appointment')

        # Make the main window and notebook expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        for frame in (self.add_frame, self.display_frame, self.update_frame):
            for i in range(20):
                frame.grid_rowconfigure(i, weight=0)
            frame.grid_rowconfigure(99, weight=1)  # For log/text box expansion
            for j in range(3):
                frame.grid_columnconfigure(j, weight=1)

        self.create_add_tab()
        self.create_display_tab()
        self.create_update_tab()

    def cascade_window(self):
        self.geometry("1100x700+50+50")
        self.deiconify()

    # --- Add Appointment Tab ---
    def create_add_tab(self):
        frame = self.add_frame
        heading = ttk.Label(frame, text="Add Appointment", font=('Segoe UI', 24, 'bold'), foreground='#2d6a4f', background='#f4f6fb')
        heading.grid(row=0, column=0, columnspan=2, pady=(20, 30), sticky='w')

        labels = [
            "Patient's Name", "Age", "Gender", "Location",
            "Appointment Date", "Appointment Time", "Phone Number"
        ]
        self.add_entries = []
        for i, label in enumerate(labels):
            ttk.Label(frame, text=label, background='#f4f6fb').grid(row=i+1, column=0, padx=(40, 10), pady=10, sticky='e')
            entry = ttk.Entry(frame, width=18)  # Reduced width
            entry.grid(row=i+1, column=1, padx=(0, 40), pady=10, sticky='ew')
            self.add_entries.append(entry)
            frame.grid_rowconfigure(i+1, weight=0)
        frame.grid_columnconfigure(1, weight=1)

        add_btn = ttk.Button(frame, text="Add Appointment", command=self.add_appointment, style='Accent.TButton', width=16)
        add_btn.grid(row=8, column=0, columnspan=2, pady=(20, 10), sticky='ew')

        self.add_log = tk.Text(frame, width=60, height=6, font=('Segoe UI', 11), bg='#e9ecef', fg='#212529', borderwidth=0)
        self.add_log.grid(row=9, column=0, columnspan=2, padx=40, pady=(10, 20), sticky='nsew')
        frame.grid_rowconfigure(9, weight=1)
        self.update_add_log()

        # Bind Enter key to move to next entry or click the button
        for i, entry in enumerate(self.add_entries):
            if i < len(self.add_entries) - 1:
                entry.bind("<Return>", lambda e, next_entry=self.add_entries[i+1]: next_entry.focus_set())
            else:
                entry.bind("<Return>", lambda e: add_btn.invoke())

    def add_appointment(self):
        vals = [e.get() for e in self.add_entries]
        if any(v.strip() == '' for v in vals):
            messagebox.showinfo("Warning", "Please Fill Up All Boxes")
            return
        add_appointment_to_db(*vals)
        messagebox.showinfo("Success", f"Appointment for {vals[0]} has been created")
        self.add_log.insert(tk.END, f'Appointment fixed for {vals[0]} on {vals[4]} at {vals[5]}\n')
        self.update_add_log()
        for e in self.add_entries:
            e.delete(0, tk.END)

    def update_add_log(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM appointments")
        total = c.fetchone()[0]
        conn.close()
        self.add_log.delete(1.0, tk.END)
        self.add_log.insert(tk.END, f"Total Appointments till now: {total}\n")

    # --- Display Appointments Tab ---
    def create_display_tab(self):
        frame = self.display_frame
        heading = ttk.Label(frame, text="Appointments", font=('Segoe UI', 28, 'bold'), foreground='#1b4332', background='#f4f6fb')
        heading.grid(row=0, column=0, columnspan=2, pady=(20, 10), sticky='w')

        self.display_box = tk.Text(frame, font=('Segoe UI', 11), bg='#e9ecef', fg='#212529', borderwidth=0, wrap='word')
        self.display_box.grid(row=1, column=0, columnspan=2, padx=30, pady=(10, 20), sticky='nsew')
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(0, 20), sticky='ew')
        ttk.Button(btn_frame, text="Refresh List", command=self.refresh_display, style='Accent.TButton').pack(side='left', padx=20)
        ttk.Button(btn_frame, text="Next Patient (Speak)", command=self.next_patient, style='Accent.TButton').pack(side='left', padx=20)

        self.display_patients = []
        self.display_index = 0
        self.refresh_display()

    def refresh_display(self):
        self.display_box.delete(1.0, tk.END)
        self.display_patients = get_all_appointments()
        for row in self.display_patients:
            display_str = (
                f"ID: {row[0]} | Name: {row[1]} | Age: {row[2]} | Gender: {row[3]} | "
                f"Location: {row[4]} | Date: {row[5]} | Time: {row[6]} | Phone: {row[7]}"
            )
            self.display_box.insert(tk.END, display_str + "\n")
        self.display_index = 0

    def next_patient(self):
        if not self.display_patients:
            messagebox.showinfo("Info", "No appointments found.")
            return
        if self.display_index >= len(self.display_patients):
            self.display_index = 0
        patient = self.display_patients[self.display_index]
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(f"Patient number {patient[0]}, {patient[1]}")
        engine.runAndWait()
        messagebox.showinfo("Next Patient", f"ID: {patient[0]}\nName: {patient[1]}")
        self.display_index += 1

    # --- Update/Delete Appointment Tab ---
    def create_update_tab(self):
        frame = self.update_frame
        heading = ttk.Label(frame, text="Update Appointments", font=('Segoe UI', 24, 'bold'), foreground='#1d3557', background='#f4f6fb')
        heading.grid(row=0, column=0, columnspan=2, pady=(20, 30), sticky='w')

        ttk.Label(frame, text="Enter Patient's Name", background='#f4f6fb').grid(row=1, column=0, padx=(40, 10), pady=10, sticky='e')
        self.update_search_entry = ttk.Entry(frame, width=18)  # Reduced width
        self.update_search_entry.grid(row=1, column=1, padx=(0, 40), pady=10, sticky='ew')
        ttk.Button(frame, text="Search", command=self.search_update, style='Accent.TButton', width=12).grid(row=1, column=2, padx=10, pady=10, sticky='ew')

        self.update_entries = []
        self.update_labels = []
        self.update_buttons = []

    def search_update(self):
        name = self.update_search_entry.get()
        all_rows = get_all_appointments()
        row = next((r for r in all_rows if r[1].lower() == name.lower()), None)
        for widget in self.update_entries + self.update_labels + self.update_buttons:
            widget.destroy()
        self.update_entries.clear()
        self.update_labels.clear()
        self.update_buttons.clear()
        if not row:
            messagebox.showinfo("Not found", "No appointment found for that name.")
            return
        labels = [
            "Patient's Name", "Age", "Gender", "Location",
            "Appointment Date", "Appointment Time", "Phone Number"
        ]
        # row: (ID, name, age, gender, location, appointment_date, scheduled_time, phone)
        values = [
            row[1], row[2], row[3], row[4],
            row[5] if len(row) > 5 and row[5] else "N/A", row[6], row[7]
        ]
        for i, (label, value) in enumerate(zip(labels, values)):
            l = ttk.Label(self.update_frame, text=label, background='#f4f6fb')
            l.grid(row=i+2, column=0, padx=(40, 10), pady=10, sticky='e')
            e = ttk.Entry(self.update_frame, width=18)  # Reduced width
            e.grid(row=i+2, column=1, padx=(0, 40), pady=10, sticky='ew')
            e.insert(tk.END, str(value))
            self.update_labels.append(l)
            self.update_entries.append(e)
        b_update = ttk.Button(self.update_frame, text="Update", command=lambda: self.update_db(row[0]), style='Accent.TButton')
        b_update.grid(row=9, column=0, pady=(20, 10), padx=10, sticky='ew')
        b_delete = ttk.Button(self.update_frame, text="Delete", command=lambda: self.delete_db(row[0]), style='Accent.TButton')
        b_delete.grid(row=9, column=1, pady=(20, 10), padx=10, sticky='ew')
        self.update_buttons.extend([b_update, b_delete])

    def update_db(self, id_):
        vals = [e.get() for e in self.update_entries]
        update_appointment(id_, *vals)
        messagebox.showinfo("Updated", "Successfully Updated.")
        self.refresh_display()

    def delete_db(self, id_):
        delete_appointment(id_)
        messagebox.showinfo("Success", "Deleted Successfully")
        for widget in self.update_entries + self.update_labels + self.update_buttons:
            widget.destroy()
        self.update_entries.clear()
        self.update_labels.clear()
        self.update_buttons.clear()
        self.refresh_display()

if __name__ == "__main__":
    app = AppointmentApp()
    app.mainloop()