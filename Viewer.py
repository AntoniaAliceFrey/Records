from tkinter import *
from pathlib import Path
from tkinter import messagebox
import sqlite3

from Check import *
from DbAccess import *

class Viewer(Check, DbAccess):
	def __init__(self, gui):
		self.gui = gui
		
	def select_data(self, sel_id, window):
		#TODO: Insert selected data into GUI main window
		#self.select_box.delete(0,END)
		#self.select_box.insert(0,sel_id)
		window.destroy()
		
	def make_window(self):
		#def show_data(self):
		'''
		This class displays the database content
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
