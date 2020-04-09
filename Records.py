from tkinter import *
from pathlib import Path
from Selector import *

class Records(DBAccess):
    '''
    This class contains the functionality of the main GUI window.
    '''

    root = Tk()
    root.title('Sign in!')
    root.geometry("455x340")
    #root.iconbitmap('@my_icon.xbm')

    def __init__(self):
        self.database = "contact_data.db"
        self.my_db = Path(self.database)
        
        if not self.my_db.is_file():
            conn = sqlite3.connect(self.database)
            c = conn.cursor()
            c.execute("""CREATE TABLE contact_data (
                  first_name text,
                  last_name text,
                  email text,
                  phone text,
                  birthday text
                  )""")
        self.selector = Selector()

    def create_labels(self, window):
        '''
        This function creates the contact labels in window.
        '''
        self.f_name_label = Label(window, text="First Name")
        self.l_name_label = Label(window, text="Last Name")
        self.email_label = Label(window, text="Email")
        self.phone_label = Label(window, text="Phone number")
        self.birthday_label = Label(window, text="Birthday")
        
        self.f_name_label.grid(row=0, column=0, pady=(10, 0))
        self.l_name_label.grid(row=1, column=0)
        self.email_label.grid(row=2, column=0)
        self.phone_label.grid(row=3, column=0)
        self.birthday_label.grid(row=4, column=0)

    def create_textboxes(self, window):
        '''
        This function creates the contact textboxes in window.
        '''
        self.f_name = Entry(window, width=30)
        self.f_name.grid(row=0, column=1, padx=20, pady=(10, 0))
        
        self.l_name = Entry(window, width=30)
        self.l_name.grid(row=1, column=1, padx=20)
        
        self.email = Entry(window, width=30)
        self.email.grid(row=2, column=1, padx=20)
        
        self.phone = Entry(window, width=30)
        self.phone.grid(row=3, column=1, padx=20)
        
        self.birthday = Entry(window, width=30)
        self.birthday.grid(row=4, column=1, padx=20)
        
    def get_tb_data(self):
        '''
        This function reads the content in the textboxes and returns a list with the 
        contact data. The function is called when a new record is added to the database 
        and for searching records in the db.
        '''
        record_data = [self.f_name.get(), self.l_name.get(), self.email.get(),
                       self.phone.get(), self.birthday.get()]
        return record_data

    def clear_textboxes(self):
        '''
        This function deletes the content in the textboxes.
        '''
        self.f_name.delete(0, END)
        self.l_name.delete(0, END)
        self.email.delete(0, END)
        self.phone.delete(0, END)
        self.birthday.delete(0, END)

    def submit(self):
        '''
        This function submits a new record to the database.
        It submits the record data to the database if the name textboxes are not empty.
        '''
        new_record = self.get_tb_data()

        # Check
        chk = Editor.check_new_record(self, new_record)

        if chk:
            c, conn = self.connect_to_db()
            c.execute("INSERT INTO contact_data VALUES                          (:f_name, :l_name, :email, :phone, :birthday)",
                      {
                          'f_name': self.f_name.get(),
                          'l_name': self.l_name.get(),
                          'email': self.email.get(),
                          'phone': self.phone.get(),
                          'birthday': self.birthday.get()
                    }
                     )
            self.clear_textboxes()
            self.disconnect_to_db(conn)

    def make_window(self):
        '''
        This function creates the GUI start window.
        '''
        self.contact_form = LabelFrame(self.root, text="Contact Form", padx=2, pady=10)
        self.contact_form.grid(row=0, column=0, columnspan=2, padx=20, pady=30)# padding outside
        self.create_labels(self.contact_form)
        self.create_textboxes(self.contact_form)

        self.submit_btn = Button(self.contact_form, text="Add Record", command=self.submit)
        self.submit_btn.grid(row=5, column=0, columnspan=2, pady=(20, 0), padx=10, ipadx=142)

        self.search_btn = Button(self.contact_form, text="Search Record", 
                                 command=lambda: [self.selector.make_window(self.get_tb_data()),
                                                  self.clear_textboxes])
        self.search_btn.grid(row=6, column=0, columnspan=2, pady=(5, 5), padx=10, ipadx=133)

        # Statusbar at bottom
        status = Label(self.root, text="Records ", relief=SUNKEN, anchor=E)
        status.grid(row=7, column=0, columnspan=2, sticky=W+E)

    def run(self):
        '''
        Keep window open until closed.
        '''
        self.root.mainloop()
  
if __name__ == "__main__":
    gui = Records()
    gui.make_window()
    gui.run()
