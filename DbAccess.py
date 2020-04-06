from tkinter import *
import sqlite3

class DbAccess:

	database = "contact_data.db"

	def connect_to_db(self):
		'''
		This function connects to the database and creates a cursor.
		'''
		conn = sqlite3.connect(self.database)
		c = conn.cursor()
		return c, conn


	def disconnect_to_db(self,conn):
		'''
		This function commits changes and terminates the connection to the database.
		'''
		conn.commit()
		conn.close()
