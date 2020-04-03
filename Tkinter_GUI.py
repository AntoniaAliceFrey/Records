from tkinter import *
from pathlib import Path
from PIL import ImageTk, Image
from tkinter import messagebox
import sqlite3

class GUI:
	root=Tk()
	root.title('Sign in!')
	root.geometry("430x450")
	#root.iconbitmap('@my_icon.xbm')

	database = "contact_data.db"
	my_db = Path(database)
	

	def __init__(self):
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


	def connect_to_db(self):
		'''
		This function connects to the database and creates a cursor
		'''
			# connects to database and create cursor
		conn = sqlite3.connect(self.database) # in current directory
		c = conn.cursor()
		return c, conn


	def disconnect_to_db(self,conn):
		'''
		This function commits changes and terminates the connection to the database
		'''
		conn.commit()
		conn.close()

	def create_labels(self,window):
		'''
		This function creates the contact labels in the selected window
		'''
		self.f_name_label = Label(window, text="First Name")
		self.l_name_label = Label(window, text="Last Name")
		self.email_label = Label(window, text="Email")
		self.phone_label = Label(window, text="Phone number")
		self.birthday_label = Label(window, text="Birthday")
		
		self.f_name_label.grid(row=0, column=0, pady=(10,0))
		self.l_name_label.grid(row=1, column=0)
		self.email_label.grid(row=2, column=0)
		self.phone_label.grid(row=3, column=0)
		self.birthday_label.grid(row=4, column=0)


	def create_textboxes(self, window, data=None):
		'''
		This function creates the contact textboxes in the selected window
		'''
		
		self.f_name = Entry(window, width=30)
		self.l_name = Entry(window, width=30)
		self.email = Entry(window, width=30)
		self.phone = Entry(window, width=30)
		self.birthday = Entry(window, width=30)
		
		if data:
			self.f_name.insert(0, data[0])
			self.l_name.insert(0, data[1])
			self.email.insert(0, data[2])
			self.phone.insert(0, data[3])
			self.birthday.insert(0, data[4])
		
		self.f_name.grid(row=0, column=1,padx=20,pady=(10,0)) # Tupel in pady: only 10 to the top
		self.l_name.grid(row=1, column=1,padx=20)
		self.email.grid(row=2, column=1,padx=20)
		self.phone.grid(row=3, column=1,padx=20)
		self.birthday.grid(row=4, column=1,padx=20)

	def submit(self):
		'''
		This function submits new data to the database
		It sends the contact data to the database
		'''
		c, conn = self.connect_to_db()
		
		c.execute("INSERT INTO contact_data VALUES (:f_name, :l_name, :email, :phone, :birthday)",
							{
								'f_name': self.f_name.get(),
								'l_name': self.l_name.get(),
								'email': self.email.get(),
								'phone': self.phone.get(),
								'birthday': self.birthday.get()
							}
				)
				
		# Clear textboxes
		self.f_name.delete(0,END)
		self.l_name.delete(0,END)
		self.email.delete(0,END)
		self.phone.delete(0,END)
		self.birthday.delete(0,END)
		
		self.disconnect_to_db(conn)
		
	def select_data(self, sel_id, window):
		self.select_box.delete(0,END)
		self.select_box.insert(0,sel_id)
		window.destroy()

		
	def show_data(self):
		'''
		This function displays the database content
		'''		
		c, conn = self.connect_to_db()
		
		# Check
		number_of_records = len(c.execute("SELECT *, oid FROM contact_data").fetchall())
		if number_of_records == 0:
			messagebox.showinfo("INFO", "Add Records!")
			return
		
		# Query the database
		c.execute("SELECT *, oid FROM contact_data") # * everything, oid=ID
		records = c.fetchall() # c.fetchone(), c.fetchmany(50)
		
		# Create new window for editing
		viewer = Tk()
		viewer.title('Show data')
		viewer.geometry("400x250")
		
		# Loop through records and print data
		radio_var = StringVar(viewer) # set viewer!
		radio_var.set(str(records[0][5])) #select first one by default
		pos = 0
		for record in records:
			oid = str(record[5])
			txt = str(record[0])+ " " + str(record[1]) + "\t" + oid
			Radiobutton(viewer,text=txt, variable=radio_var, value=oid).grid(row=pos, column=0)
			pos += 1
		
		select_btn = Button(viewer,text="Select Record", command=lambda: self.select_data(radio_var.get(),viewer)) # command XXX
		select_btn.grid(row=pos, column=0, columnspan=2, pady=(10,0), padx=10, ipadx=130)
				
		close_btn = Button(viewer,text="Close", command=viewer.destroy)
		close_btn.grid(row=pos+1, column=0, columnspan=2, pady=(5,10), padx=10, ipadx=156)
		
		self.disconnect_to_db(conn)
		

	def check_id(self, number_of_records=0):
		'''
		This function checks the user selected id
		Every record has an unique oid
		'''
		oid = self.select_box.get()
		if oid == "":
			messagebox.showerror("ERROR", "Please enter an ID.")
			return "false"
		elif int(oid) > number_of_records:
			messagebox.showerror("ERROR", "Please select a valid ID")
			return "false"
		return oid


	def delete(self):
		'''
		This function deletes a selected record in the database
		The record is selected with its oid
		'''
		c, conn = self.connect_to_db()
		
		number_of_records = len(c.execute("SELECT *, oid FROM contact_data").fetchall())
		sel_id = self.check_id(number_of_records)
		if sel_id == "false":
			return
		
		c.execute("DELETE from contact_data WHERE oid = " + sel_id)

		self.select_box.delete(0,END)
		self.disconnect_to_db(conn)


	def update(self,window=None):
		'''
		This function saves changes of editing records
		'''
		c, conn = self.connect_to_db()
		record_id = self.select_box.get()
		
		c.execute(""" UPDATE contact_data 
		              SET first_name = :first, 
											last_name = :last,
											email = :email,
											phone = :phone,
											birthday = :birthday
									WHERE oid = :oid """,
			{	'first': self.f_name_editor.get(),
				'last': self.l_name_editor.get(),
				'email': self.email_editor.get(),
				'phone': self.phone_editor.get(),
				'birthday': self.birthday_editor.get(),
				'oid': record_id # necessary	
			})
		window.destroy()
		self.disconnect_to_db(conn)


	def edit(self):
		'''
		This function edits a record in the database
		The record is selected with its oid
		'''
		c, conn = self.connect_to_db()
		
		number_of_records = len(c.execute("SELECT *, oid FROM contact_data").fetchall())
		sel_id = self.check_id(number_of_records)
		if sel_id == "false":
			return
		
		# Create new window for editing
		editor = Tk()
		editor.title('Edit data')
		editor.geometry("400x250")
		
		save_btn = Button(editor,text="Save changes", command=lambda: self.update(editor))
		save_btn.grid(row=6, column=0, columnspan=2, pady=(10,0), padx=10, ipadx=130)

		c.execute("SELECT * FROM contact_data WHERE oid = " + sel_id)
		sel_records = c.fetchall()
		
		# create labels and textboxes
		self.create_labels(editor)
		if len(sel_records) == 1:
			data = sel_records[0]
			
			self.f_name_editor = Entry(editor, width=30)
			self.l_name_editor = Entry(editor, width=30)
			self.email_editor = Entry(editor, width=30)
			self.phone_editor = Entry(editor, width=30)
			self.birthday_editor = Entry(editor, width=30)
		
			self.f_name_editor.insert(0, data[0])
			self.l_name_editor.insert(0, data[1])
			self.email_editor.insert(0, data[2])
			self.phone_editor.insert(0, data[3])
			self.birthday_editor.insert(0, data[4])
		
			self.f_name_editor.grid(row=0, column=1,padx=20,pady=(10,0)) # Tupel in pady: only 10 to the top
			self.l_name_editor.grid(row=1, column=1,padx=20)
			self.email_editor.grid(row=2, column=1,padx=20)
			self.phone_editor.grid(row=3, column=1,padx=20)
			self.birthday_editor.grid(row=4, column=1,padx=20)
			
		self.select_box.delete(0,END)
		self.disconnect_to_db(conn)


	def make_window(self):
		# Create a LabelFrame
		# labels and textboxes to enter data
		# submit button and show records button
		self.data_frame = LabelFrame(self.root, text="Contact Data", padx=2, pady=10)
		self.data_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5) # padding outside
		self.create_labels(self.data_frame)
		self.create_textboxes(self.data_frame)

		self.submit_btn = Button(self.data_frame, text="Add Record To Database", command=self.submit)
		self.submit_btn.grid(row=5, column=0, columnspan=2, pady=(20,0), padx=10, ipadx=100)

		self.query_btn = Button(self.data_frame,text="Show Records", command=self.show_data)
		self.query_btn.grid(row=6, column=0, columnspan=2, pady=(5,5), padx=10, ipadx=135)

		# Create a LabelFrame
		# select label and box
		# edit button and delete button

		self.select_frame = LabelFrame(self.root, text="Edit Data", padx=2, pady=10)
		self.select_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5) # padding outside

		self.select_box_label = Label(self.select_frame, text="Select ID")
		self.select_box_label.grid(row=0, column=0)
		self.select_box = Entry(self.select_frame, width=30)
		self.select_box.grid(row=0, column=1)

		self.edit_btn = Button(self.select_frame,text="Edit Record", command=self.edit)
		self.edit_btn.grid(row=1, column=0, columnspan=2, pady=(20,0), padx=10, ipadx=145)

		self.delete_btn = Button(self.select_frame,text="Delete Record", command=self.delete)
		self.delete_btn.grid(row=2, column=0, columnspan=2, pady=(5,5), padx=10, ipadx=135)

		# Statusbar at bottom of root window
		#status = Label(root, text="myStatus", relief=SUNKEN, anchor=E)
		#status.grid(row=13,column=0,columnspan=2, sticky=W+E)

	def run(self):
		self.root.mainloop()
	
	
if __name__ == "__main__":
	g = GUI()
	g.make_window()
	g.run()
