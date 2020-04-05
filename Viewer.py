from tkinter import *
from pathlib import Path
from tkinter import messagebox
import sqlite3

from Editor import *
from DataCheck import *
from DbAccess import *

class Viewer(DataCheck, DbAccess):
	def __init__(self, gui):
		self.gui = gui		
	
	def process_data(self, data):
	
		c, conn = self.connect_to_db()
		
		# DatabaseCheck
		number_of_records = len(c.execute("SELECT *, oid FROM contact_data").fetchall())
		chk = self.DbCheck(number_of_records)
		if chk == "false":
			return [],"DB empty"
		
		f_name = data[0]
		if f_name != "":
			# print records with same first name
			c.execute("SELECT *,oid FROM contact_data WHERE first_name ='" +f_name+"'")
			records = c.fetchall()
			txt = "[ " + f_name + " ]"
			chk = self.check_data(records) #TODO
			
		else:
			# print all records
			c.execute("SELECT *, oid FROM contact_data")
			records = c.fetchall() # c.fetchone(), c.fetchmany(50)
			txt = "[all]"
		
		self.disconnect_to_db(conn)
		return records, txt
	
	def print_data(self, window, data):
		self.radio_var = StringVar(window) # set viewer!
		#self.radio_var.set(str(data[0][5]))
		
		# Loop through data and print records
		pos = 0
		for record in data:
			oid = record[5]
			txt = str(record[0])+ " " + str(record[1])
			Radiobutton(window,text=txt, variable=self.radio_var, value=oid).grid(row=pos, column=0,sticky=W)
			pos += 1
					
		return pos
	
	def make_window(self, search_data=None):
		'''
		This class shows the database content
		'''
		self.editor = Editor()
		
		records, txt = self.process_data(search_data)
		if len(records) == 0:
			return
			
		# Create new window
		viewer = Tk()
		viewer.title("Records " + txt)
		y_win = 150 + len(records)*20
		viewer.geometry("400x"+ str(y_win))
		pos = self.print_data(viewer, records)
			
		edit_btn = Button(viewer,text="Edit Record", command=lambda: [self.editor.make_window(self.radio_var.get()),viewer.destroy()])
		edit_btn.grid(row=pos, column=0, columnspan=2, pady=(10,0), padx=10, ipadx=135)

		delete_btn = Button(viewer,text="Delete Record", command=lambda: [self.editor.delete_record(self.radio_var.get()), viewer.destroy()])
		delete_btn.grid(row=pos+1, column=0, columnspan=2, pady=(5,0), padx=10, ipadx=125)		
		
		close_btn = Button(viewer,text="Close", command=viewer.destroy)
		close_btn.grid(row=pos+2, column=0, columnspan=2, pady=(5,0), padx=10, ipadx=153)	
		
