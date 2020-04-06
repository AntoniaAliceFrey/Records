from tkinter import *
import sqlite3

from Editor import *
from DataCheck import *
from DbAccess import *

class Viewer(DataCheck, DbAccess):

	def __init__(self):
		self.editor = Editor()
	
	def find_records(self, search_data=None):
		'''
		This function is selecting records from the database, based on the search_data.
		'''
	
		c, conn = self.connect_to_db()

		if search_data:
			f_name = search_data[0]
			l_name = search_data[1]
			if f_name != "":
				# print records with same first name
				c.execute("SELECT *,oid FROM contact_data WHERE first_name ='" +f_name+"'")
				records = c.fetchall()
				self.check_search_result(records)
		else:
			# all records
			c.execute("SELECT *, oid FROM contact_data")
			records = c.fetchall() # c.fetchone(), c.fetchmany(50)
		
		self.disconnect_to_db(conn)
		return records
		
	
	def print_records(self, data):
		'''
		This function prints the record data in the window.
		'''
		self.radio_var = StringVar(self.viewer)
		# Uncomment to autoselect first record
		#self.radio_var.set(str(data[0][5])) 
		
		# Loop through data and print records
		pos = 0
		for record in data:
			oid = record[5]
			txt = str(record[0])+ " " + str(record[1])
			Radiobutton(self.viewer,text=txt, variable=self.radio_var, value=oid).grid(row=pos, column=0,sticky=W)
			pos += 1
					
		return pos
		
	
	def window_checks(self, data):
		'''
		This function makes sure that the database is not empty,
		and returns all record or records with the searched f_name.
		'''
		try:
			# when updating window
			self.viewer.destroy()
		except:
			pass
		
		chk = self.check_db()
		if not chk:
			return []
			
		search = self.check_search_data(data)

		if search:
			# only records which match textbox content
			records = self.find_records(data)
		else:
			# all records
			records = self.find_records()
		return records 
		
	
	def make_window(self, data):
		'''
		This function creates a window to show the records is the database.
		If the textboxes are empty, then all records are shown.
		If the name textboxes have content, then only records with this name are displayed.
		'''
		records = self.window_checks(data)
		if len(records) == 0:
			return
		
		self.viewer = Tk()
		y_win = 150 + len(records)*20
		self.viewer.geometry("400x"+ str(y_win))
		self.viewer.title("Records")
		
		pos = self.print_records(records)
			
		edit_btn = Button(self.viewer,text="Edit Record", command=lambda: [self.editor.make_window(self.radio_var.get()), self.make_window(data)])
		edit_btn.grid(row=pos, column=0, columnspan=2, pady=(20,0), padx=10, ipadx=135)

		delete_btn = Button(self.viewer,text="Delete Record", command=lambda: [self.editor.delete_record(self.radio_var.get()), self.make_window(data)])
		delete_btn.grid(row=pos+1, column=0, columnspan=2, pady=(5,0), padx=10, ipadx=125)		
		
		close_btn = Button(self.viewer,text="Close", command=self.viewer.destroy)
		close_btn.grid(row=pos+2, column=0, columnspan=2, pady=(5,0), padx=10, ipadx=153)	
		
