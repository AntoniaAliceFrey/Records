from tkinter import messagebox
import sqlite3

class DataCheck:

    def __init__(self):
        '''
        Init method
        '''

    def is_int(self, var):
        '''
        This function checks if var (string) contains numbers and is an integer.
        '''
        try:
            int(var)
            return True
        except ValueError:
            pass

    def check_new_record(self, tb_data):
        '''
        This function checks whether the name textboxes have some content.
        data[0] = first name
        data[1] = last name
        '''
        # check new record
        if tb_data[0] == "" or tb_data[1] == "":
            messagebox.showerror("ERROR", "Name cannot be empty!")
            return False
        return True

    def check_search_data(self, tb_data, func):
        '''
        This function checks whether the name textboxes have some content.
        data[0] = first name
        data[1] = last name
        '''
        # new window
        if func == "show data":
            if tb_data[0] == "":
                # no search request
                response = messagebox.askyesno("", "Show all records?")
                if response == 1:
                    return "all records"
                else:
                    return "abort"

        # search request
        if tb_data[0] != "":
            return "search record"

        # update window
        if func == "update data":
            # no search request
            return "all records"

    def check_db(self):
        '''
        This function makes sure that the database is not empty.
        '''
        c, conn = self.connect_to_db() #XXX
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
        if not self.is_int(oid):
            messagebox.showinfo("INFO", "Select Record!!!")
            return False
        return True

    def check_search_result(self, data):
        '''
        This function checks whether a record is found, if the user wants to search a specific record.
        '''
        if len(data) == 0:
            messagebox.showerror("ERROR", "No matching Record found.\n")
            return False
        return True
