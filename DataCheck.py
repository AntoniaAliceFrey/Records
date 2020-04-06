from tkinter import messagebox
import sqlite3

class DataCheck:

	def is_int(self,var):
		try: 
		 int(var)
		 return True
		except ValueError:
		 pass
		 
	def check_search_data(self, search_data):
		if search_data[0] == "" and search_data[1]=="":
			# no search data, print all records
			return False
		else:
			return True

	def check_new_record(self, data):
		'''
		This function checks whether the name textboxes have some content.
		data[0] = first name
		data[1] = last name
		'''		
		if data[0] == "" or data[1] == "":
			messagebox.showerror("ERROR", "Name cannot be empty!")
			return False
		else:
			return True
			
	def check_db(self):
		'''
		This function makes sure that the database is not empty.
		'''		
		c, conn = self.connect_to_db()
		number_of_records = len(c.execute("SELECT *, oid FROM contact_data").fetchall())
		if number_of_records == 0:
			messagebox.showinfo("INFO", "Add Records!")
			return False
		return True
	
	def check_sel(self, oid):
		'''
		This function checks whether a record is selected.
		The user can select records via radio button which have a variable with the value oid.
		'''
		if self.is_int(oid):
			return True
		else:
			messagebox.showinfo("INFO", "Select Record!!!")
			return False
		
	def check_search_result(self, data):
		'''
		This function checks whether a record is found, if the user wants to search a specific record.
		'''
		if len(data) == 0:
			messagebox.showerror("ERROR", "No matching Record found.\n")
			return False
		return True
