from tkinter import *
from pathlib import Path
from PIL import ImageTk, Image
from tkinter import messagebox
import sqlite3

from DbAccess import *

class DataCheck:
	def check_new_record(self, data):
		if data[0] == "" or data[1] == "":
			messagebox.showerror("ERROR", "Name cannot be empty!")
			return "false"
	 
	 
	def check_id(self, oid, number_of_records):
		'''
		This function checks the user selected id
		Every record has an unique oid
		'''		
		if oid == "":
			messagebox.showerror("ERROR", "Please enter an ID.")
			return "false"
		elif int(oid) > number_of_records:
			messagebox.showerror("ERROR", "Please select a valid ID")
			return "false"
			
		return oid
		
	def check_data(self, data, func=None, max_data=1):
		'''
		This function controls ...
		'''
		if len(data) == 0:
			messagebox.showerror("ERROR", "Selected Record not found.\n Check the Record ID")
			return "false"
		
		if len(data) > int(max_data):
			messagebox.showerror("ERROR", "Ooops something went wrong")
			return "false"
		
		if len(data) == 1 and func=="edit":
			messagebox.showinfo("Good", "Don't forget to save changes!")
			return(data[0])
