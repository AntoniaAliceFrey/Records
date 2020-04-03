from tkinter import *
from pathlib import Path
from PIL import ImageTk, Image
from tkinter import messagebox
import sqlite3

root=Tk()
root.title('Sign in!')
root.geometry("430x450")
#root.iconbitmap('@my_icon.xbm')

database = "contact_data.db"
my_db = Path(database)

if not my_db.is_file():
	conn = sqlite3.connect(database)
	c = conn.cursor()
	c.execute("""CREATE TABLE contact_data (
					first_name text,
					last_name text,
					email text,
					phone text,
					birthday text
					)""")

def connect_to_db():
	'''
	This function connects to the database and creates a cursor
	'''
		# connects to database and create cursor
	conn = sqlite3.connect(database) # in current directory
	c = conn.cursor()
	return c, conn


def disconnect_to_db(conn):
	'''
	This function commits changes and terminates the connection to the database
	'''
	conn.commit()
	conn.close()

def create_labels(window):
	'''
	This function creates the contact labels in the selected window
	'''
	f_name_label = Label(window, text="First Name")
	l_name_label = Label(window, text="Last Name")
	email_label = Label(window, text="Email")
	phone_label = Label(window, text="Phone number")
	birthday_label = Label(window, text="Birthday")
	
	f_name_label.grid(row=0, column=0, pady=(10,0))
	l_name_label.grid(row=1, column=0)
	email_label.grid(row=2, column=0)
	phone_label.grid(row=3, column=0)
	birthday_label.grid(row=4, column=0)


def create_textboxes(window, data=None):
	'''
	This function creates the contact textboxes in the selected window
	'''
	global f_name, l_name, email, phone, birthday
	
	f_name = Entry(window, width=30)
	l_name = Entry(window, width=30)
	email = Entry(window, width=30)
	phone = Entry(window, width=30)
	birthday = Entry(window, width=30)
	
	if data:
		f_name.insert(0, data[0])
		l_name.insert(0, data[1])
		email.insert(0, data[2])
		phone.insert(0, data[3])
		birthday.insert(0, data[4])
	
	f_name.grid(row=0, column=1,padx=20,pady=(10,0)) # Tupel in pady: only 10 to the top
	l_name.grid(row=1, column=1,padx=20)
	email.grid(row=2, column=1,padx=20)
	phone.grid(row=3, column=1,padx=20)
	birthday.grid(row=4, column=1,padx=20)

def submit():
	'''
	This function submits new data to the database
	It sends the contact data to the database
	'''
	c, conn = connect_to_db()
	
	c.execute("INSERT INTO contact_data VALUES (:f_name, :l_name, :email, :phone, :birthday)",
						{
							'f_name': f_name.get(),
							'l_name': l_name.get(),
							'email': email.get(),
							'phone': phone.get(),
							'birthday': birthday.get()
						}
			)
			
	# Clear textboxes
	f_name.delete(0,END)
	l_name.delete(0,END)
	email.delete(0,END)
	phone.delete(0,END)
	birthday.delete(0,END)
	
	disconnect_to_db(conn)
	
	
def select_data(sel_id):
	#print("TODO")
	#select_box.insert(0,str(sel_id))
	return
	
def show_data():
	'''
	This function displays the database content
	'''		
	c, conn = connect_to_db()
	
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
	global record_id #DEBUG
	record_id = StringVar()
	record_id.set(str(records[0][5])) #select first one by default

	data=[]
	for record in records:
		data.append((record[0] + " " + (record[1]) , str(record[5])))
	#print(data)

	pos = 0
	for name, oid in data:
		txt = name + "\t" + oid
		radio_btn = Radiobutton(viewer,text=txt, variable=record_id, value=oid)
		radio_btn.grid(row=pos, column=0)
		pos += 1
		
# TODO: Print oid of selected record in select_box in root window
#	pos = 0
#	for record in records:
#		txt = str(record[0])+ " " + str(record[1]) + "\t" + str(record[5])
#		radio_btn = Radiobutton(viewer,text=txt, variable=record_id, value=str(record[5]))
#		radio_btn.grid(row=pos, column=0)
#		pos += 1
	
	select_btn = Button(viewer,text="Select Record", command=lambda: select_data(record_id.get())) # command XXX
	select_btn.grid(row=pos, column=0, columnspan=2, pady=(10,0), padx=10, ipadx=130)
			
	close_btn = Button(viewer,text="Close", command=viewer.destroy)
	close_btn.grid(row=pos+1, column=0, columnspan=2, pady=(5,10), padx=10, ipadx=156)
	
	disconnect_to_db(conn)
	

def check_id(number_of_records=0):
	'''
	This function checks the user selected id
	Every record has an unique oid
	'''
	oid = select_box.get()
	if oid == "":
		messagebox.showerror("ERROR", "Please enter an ID.")
		return "false"
	elif int(oid) > number_of_records:
		messagebox.showerror("ERROR", "Please select a valid ID")
		return "false"
	return oid


def delete():
	'''
	This function deletes a selected record in the database
	The record is selected with its oid
	'''
	c, conn = connect_to_db()
	
	number_of_records = len(c.execute("SELECT *, oid FROM contact_data").fetchall())
	sel_id = check_id(number_of_records)
	if sel_id == "false":
		return
	
	c.execute("DELETE from contact_data WHERE oid = " + sel_id)

	select_box.delete(0,END)
	disconnect_to_db(conn)


def update():
	'''
	This function saves changes of editing records
	'''
	c, conn = connect_to_db()
	
	global oid, record_id
	record_id = select_box.get()
	
	c.execute(""" UPDATE contact_data SET 
		first_name = :first, 
		last_name = :last,
		email = :email,
		phone = :phone,
		birthday = :birthday
		
		WHERE oid = :oid """,
		{'first': f_name.get(),
			'last': l_name.get(),
			'email': email.get(),
			'phone': phone.get(),
			'birthday': birthday.get(),
			
			'oid': record_id # necessary	
		})
	
	disconnect_to_db(conn)

def edit():
	'''
	This function edits a record in the database
	The record is selected with its oid
	'''
	global f_name, l_name, email, phone, birthday
	c, conn = connect_to_db()
	
	number_of_records = len(c.execute("SELECT *, oid FROM contact_data").fetchall())
	sel_id = check_id(number_of_records)
	if sel_id == "false":
		return
	
	# Create new window for editing
	editor = Tk()
	editor.title('Edit data')
	editor.geometry("400x250")
	create_labels(editor)
	create_textboxes(editor)
	save_btn = Button(editor,text="Save changes", command=update)
	save_btn.grid(row=6, column=0, columnspan=2, pady=(10,0), padx=10, ipadx=130)

	c.execute("SELECT * FROM contact_data WHERE oid = " + sel_id)
	sel_records = c.fetchall()
	
	if len(sel_records) == 1:
		create_textboxes(editor, sel_records[0])
		
	select_box.delete(0,END)
	disconnect_to_db(conn)

# frame
# labels and textboxes to enter data
# submit button and show records button
data_frame = LabelFrame(root, text="Contact Data", padx=2, pady=10)
data_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5) # padding outside
create_labels(data_frame)
create_textboxes(data_frame)

submit_btn = Button(data_frame, text="Add Record To Database", command=submit)
submit_btn.grid(row=5, column=0, columnspan=2, pady=(20,0), padx=10, ipadx=100)

query_btn = Button(data_frame,text="Show Records", command=show_data)
query_btn.grid(row=6, column=0, columnspan=2, pady=(5,5), padx=10, ipadx=135)

# Create a frame
# select label and box
# edit button and delete button

select_frame = LabelFrame(root, text="Edit Data", padx=2, pady=10)
select_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5) # padding outside

select_box_label = Label(select_frame, text="Select ID")
select_box_label.grid(row=0, column=0)
select_box = Entry(select_frame, width=30)
select_box.grid(row=0, column=1)

edit_btn = Button(select_frame,text="Edit Record", command=edit)
edit_btn.grid(row=1, column=0, columnspan=2, pady=(20,0), padx=10, ipadx=145)

delete_btn = Button(select_frame,text="Delete Record", command=delete)
delete_btn.grid(row=2, column=0, columnspan=2, pady=(5,5), padx=10, ipadx=135)

# Statusbar at bottom of root window
#status = Label(root, text="myStatus", relief=SUNKEN, anchor=E)
#status.grid(row=13,column=0,columnspan=2, sticky=W+E)

root.mainloop()
