# update the appointments
from tkinter import *
import tkinter.messagebox 
import sqlite3

def update_appointment(id_, name, age, gender, location, appointment_date, scheduled_time, phone):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(
        "UPDATE appointments SET name=?, age=?, gender=?, location=?, appointment_date=?, scheduled_time=?, phone=? WHERE ID=?",
        (name, age, gender, location, appointment_date, scheduled_time, phone, id_)
    )
    conn.commit()
    conn.close()

def delete_appointment(id_):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM appointments WHERE ID=?", (id_,))
    conn.commit()
    conn.close()

class Application:
    def __init__(self, master):
        self.master = master
        # heading label
        self.heading = Label(master, text="Update Appointments",  fg='steelblue', font=('arial 40 bold'))
        self.heading.place(x=150, y=0)

        # search criteria -->name 
        self.name = Label(master, text="Enter Patient's Name", font=('arial 18 bold'))
        self.name.place(x=0, y=60)

        # entry for  the name
        self.namenet = Entry(master, width=30)
        self.namenet.place(x=280, y=62)

        # search button
        self.search = Button(master, text="Search", width=12, height=1, bg='steelblue', command=self.search_db)
        self.search.place(x=350, y=102)
    # function to search
    def search_db(self):
        self.input = self.namenet.get()
        sql = "SELECT * FROM appointments WHERE name LIKE ?"
        self.res = c.execute(sql, (self.input,))
        for self.row in self.res:
            self.name1 = self.row[1]  # name
            self.age = self.row[2]
            self.gender = self.row[3]
            self.location = self.row[4]
            self.appointment_date = self.row[5]
            self.time = self.row[6]
            self.phone = self.row[7]
        # creating the update form
        self.uname = Label(self.master, text="Patient's Name", font=('arial 18 bold'))
        self.uname.place(x=0, y=140)

        self.uage = Label(self.master, text="Age", font=('arial 18 bold'))
        self.uage.place(x=0, y=180)

        self.ugender = Label(self.master, text="Gender", font=('arial 18 bold'))
        self.ugender.place(x=0, y=220)

        self.ulocation = Label(self.master, text="Location", font=('arial 18 bold'))
        self.ulocation.place(x=0, y=260)

        self.udate = Label(self.master, text="Appointment Date", font=('arial 18 bold'))
        self.udate.place(x=0, y=300)

        self.utime = Label(self.master, text="Appointment Time", font=('arial 18 bold'))
        self.utime.place(x=0, y=340)

        self.uphone = Label(self.master, text="Phone Number", font=('arial 18 bold'))
        self.uphone.place(x=0, y=380)

        # entries for each label
        self.ent1 = Entry(self.master, width=30)
        self.ent1.place(x=300, y=140)
        self.ent1.insert(END, str(self.name1))

        self.ent2 = Entry(self.master, width=30)
        self.ent2.place(x=300, y=180)
        self.ent2.insert(END, str(self.age))

        self.ent3 = Entry(self.master, width=30)
        self.ent3.place(x=300, y=220)
        self.ent3.insert(END, str(self.gender))

        self.ent4 = Entry(self.master, width=30)
        self.ent4.place(x=300, y=260)
        self.ent4.insert(END, str(self.location))

        self.ent5 = Entry(self.master, width=30)
        self.ent5.place(x=300, y=300)
        self.ent5.insert(END, str(self.appointment_date))

        self.ent6 = Entry(self.master, width=30)
        self.ent6.place(x=300, y=340)
        self.ent6.insert(END, str(self.time))

        self.ent7 = Entry(self.master, width=30)
        self.ent7.place(x=300, y=380)
        self.ent7.insert(END, str(self.phone))

        # button to execute update
        self.update = Button(self.master, text="Update", width=20, height=2, bg='lightblue', command=self.update_db)
        self.update.place(x=400, y=420)

        # button to delete
        self.delete = Button(self.master, text="Delete", width=20, height=2, bg='red', command=self.delete_db)
        self.delete.place(x=150, y=420)

    def update_db(self):
        self.var1 = self.ent1.get() # name
        self.var2 = self.ent2.get() # age
        self.var3 = self.ent3.get() # gender
        self.var4 = self.ent4.get() # location
        self.var5 = self.ent5.get() # appointment_date
        self.var6 = self.ent6.get() # scheduled_time
        self.var7 = self.ent7.get() # phone

        query = "UPDATE appointments SET name=?, age=?, gender=?, location=?, appointment_date=?, scheduled_time=?, phone=? WHERE name LIKE ?"
        c.execute(query, (self.var1, self.var2, self.var3, self.var4, self.var5, self.var6, self.var7, self.namenet.get()))
        conn.commit()
        tkinter.messagebox.showinfo("Updated", "Successfully Updated.")
    def delete_db(self):
        # delete the appointment
        sql2 = "DELETE FROM appointments WHERE name LIKE ?"
        c.execute(sql2, (self.namenet.get(),))
        conn.commit()
        tkinter.messagebox.showinfo("Success", "Deleted Successfully")
        self.ent1.destroy()
        self.ent2.destroy()
        self.ent3.destroy()
        self.ent4.destroy()
        self.ent5.destroy()
        self.ent6.destroy()
        self.ent7.destroy()
if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()