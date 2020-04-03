from tkinter import *
from pathlib import Path
from tkinter import messagebox
import sqlite3

from IdCheck import *
from DbAccess import *

class Editor(IdCheck, DbAccess):

	def make_window(self, oid): #TODO delete sel_record here
		'''
		This function edits a record in the database
		The record is selected with its oid
		'''
		c, conn = self.connect_to_db()
		
		# Check
		number_of_records = len(c.execute("SELECT *, oid FROM contact_data").fetchall())
		sel_id = self.check_id(oid, number_of_records)
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
		
		# Create labels and textboxes
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
		
			self.f_name_editor.grid(row=0, column=1,padx=20,pady=(10,0))
			self.l_name_editor.grid(row=1, column=1,padx=20)
			self.email_editor.grid(row=2, column=1,padx=20)
			self.phone_editor.grid(row=3, column=1,padx=20)
			self.birthday_editor.grid(row=4, column=1,padx=20)
		
		self.disconnect_to_db(conn)
