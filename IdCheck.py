from tkinter import *
from pathlib import Path
from PIL import ImageTk, Image
from tkinter import messagebox
import sqlite3

from DbAccess import *

class IdCheck:
	def check_id(self, oid, number_of_records=0):
		'''
		This function checks the user selected id
		Every record has an unique oid
		'''
		#
		#oid = self.select_box.get()
		
		if oid == "":
			messagebox.showerror("ERROR", "Please enter an ID.")
			return "false"
		elif int(oid) > number_of_records:
			messagebox.showerror("ERROR", "Please select a valid ID")
			return "false"
		
		# TODO	
		#self.select_box.delete(0,END)
		return oid
