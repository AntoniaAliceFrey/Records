from tkinter import *
from pathlib import Path
from PIL import ImageTk, Image
from tkinter import messagebox
import sqlite3

from DbAccess import *

class DataCheck:

	def check_new_record(self, data):
		'''
		This function ...
		'''		
		if data[0] == "" or data[1] == "":
			messagebox.showerror("ERROR", "Name cannot be empty!")
			return "false"
			
	def DbCheck(self, number_of_records):
		if number_of_records == 0:
			messagebox.showinfo("INFO", "Add Records!")
			return "false"
	 
	def check_id(self, oid, oid_max):
		'''
		This function checks the user selected id
		Every record has an unique oid
		'''		
		if oid == "":
			messagebox.showerror("ERROR", "Please enter an ID.")
			return "false"
			
#		elif int(oid) > oid_max:
#			messagebox.showerror("ERROR", "Please select a valid ID")
#			return "false"
			
		return oid
		
	def check_data(self, data, func=None):
		'''
		This function controls ...
		'''
		if len(data) == 0:
			messagebox.showerror("ERROR", "Record not found.\n")
			return "false"
		
		if len(data) == 1 and func=="edit":
			#messagebox.showinfo("Good", "Don't forget to save changes!")
			return(data[0])
