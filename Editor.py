from tkinter import *
import sqlite3
from DataCheck import *
from DbAccess import *

class Editor(DataCheck, DbAccess):

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
		
	def delete_record(self, oid):
		'''
		This function deletes a selected record in the database
		The record is selected with its oid
		'''
		chk = self.check_sel(oid)
		if not chk:
			return
		
		c, conn = self.connect_to_db()	
		c.execute("DELETE from contact_data WHERE oid = " + oid)		
		self.disconnect_to_db(conn)
	
	def update(self, record_oid, window):
		'''
		This function updates the record database
		'''
		c, conn = self.connect_to_db()
		
		c.execute(""" UPDATE contact_data 
		              SET first_name = :first, 
											last_name = :last,
											email = :email,
											phone = :phone,
											birthday = :birthday
									WHERE oid = :oid """,
			{	'first': self.f_name.get(),
				'last': self.l_name.get(),
				'email': self.email.get(),
				'phone': self.phone.get(),
				'birthday': self.birthday.get(),
				'oid': record_oid
			})
		window.destroy()
		self.disconnect_to_db(conn)

	def make_window(self, oid):
		'''
		This function creates a window to edit a user selected record.
		A record is selected by clicking a radiobutton in the viewer window.
		All radiobuttons have one variable which contains the oid value of the selected record.
		'''
		chk = self.check_sel(oid)
		if not chk:
			return
	
		c, conn = self.connect_to_db()
		
		c.execute("SELECT * FROM contact_data WHERE oid = " + oid)
		data = c.fetchall()
		record_data = data[0]

		# Create new window for editing
		editor = Tk()
		editor.title('Edit data')
		editor.geometry("400x200")
		
		# Create labels and textboxes
		self.create_labels(editor)
		self.create_textboxes(editor, record_data)
		
		# Create a save button
		save_btn = Button(editor,text="Save changes", command=lambda: self.update(oid, editor))
		save_btn.grid(row=6, column=0, columnspan=2, pady=(10,0), padx=10, ipadx=130)
		
		self.disconnect_to_db(conn)
