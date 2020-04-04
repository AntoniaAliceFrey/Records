from tkinter import *
from pathlib import Path
from tkinter import messagebox
import sqlite3

from DataCheck import *
from DbAccess import *

class Viewer(DataCheck, DbAccess):
	def __init__(self, gui):
		self.gui = gui
		
	def select_data(self, window):
		self.selected = self.radio_var.get()
		print(self.selected)
		window.destroy()
		
	
	def print_data(self, window, data):
		
		self.radio_var = StringVar(window) # set viewer!
		self.radio_var.set(str(data[0][5]))
		
		# Loop through data and print records
		pos = 0
		for record in data:
			oid = str(record[5])
			txt = oid +": "+ str(record[0])+ " " + str(record[1])
			Radiobutton(window,text=txt, variable=self.radio_var, value=oid).grid(row=pos, column=0,sticky=W)
			pos += 1
					
		return pos
	
	def make_window(self, search_data):
		#def show_data(self):
		'''
		This class displays the database content
		'''
		c, conn = self.connect_to_db()
		
		self.selected = "oid" # !!! Debug
		
		# DataCheck
		number_of_records = len(c.execute("SELECT *, oid FROM contact_data").fetchall())
		if number_of_records == 0:
			messagebox.showinfo("INFO", "Add Records!")
			return
		
		f_name = search_data[0]
		
		if search_data[0] != "":
			# print records with same first name
			c.execute("SELECT *,oid FROM contact_data WHERE first_name ='" +f_name+"'")
			sel_records = c.fetchall()
			
			chk = self.check_data(data=sel_records,max_data=100)
			if chk == "false":
				return

			# Create new window #TODO
			viewer = Tk()
			viewer.title('Show data')
			viewer.geometry("400x250")
			
			pos = self.print_data(viewer, sel_records)
			
		else:
			
			# Create new window
			viewer = Tk()
			viewer.title('Show data')
			viewer.geometry("400x250")
			
			# print all records
			c.execute("SELECT *, oid FROM contact_data")
			all_records = c.fetchall() # c.fetchone(), c.fetchmany(50)
			pos = self.print_data(viewer, all_records)
		
		select_btn = Button(viewer,text="Select Record", command=lambda: self.select_data(viewer))
		select_btn.grid(row=pos, column=0, columnspan=2, pady=(10,0), padx=10, ipadx=130)
				
		close_btn = Button(viewer,text="Close", command=viewer.destroy)
		close_btn.grid(row=pos+1, column=0, columnspan=2, pady=(5,10), padx=10, ipadx=156)
		
		return self.selected #TODO
		
		self.disconnect_to_db(conn)
