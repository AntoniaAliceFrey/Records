from tkinter import *
from Editor import *
from DataCheck import *
from DbAccess import *

class Selector(DataCheck, DbAccess):
    '''
    This class displays the records in the database.
    '''

    def __init__(self):
        '''
        This...
        '''
        self.editor = Editor()

    def find_records(self, search_data=None):
        '''
        This function is selecting records from the database, based on the search_data.
        '''

        c, conn = self.connect_to_db()

        if search_data:
            f_name = search_data[0]
            l_name = search_data[1]
            # search records with same first name
            c.execute("SELECT *,oid FROM contact_data WHERE first_name ='" +f_name+"'")
            records = c.fetchall()
            self.check_search_result(records)
        else:
            # all records
            c.execute("SELECT *, oid FROM contact_data")
            records = c.fetchall()# c.fetchone(), c.fetchmany(50)

        self.disconnect_to_db(conn)
        return records

    def print_records(self, data):
        '''
        This function prints the record data in the window.
        '''
        self.radio_var = StringVar(self.selector)
        # Uncomment to autoselect first record
        #self.radio_var.set(str(data[0][5]))

        # Loop through data and print records
        pos = 0
        for record in data:
            oid = record[5]
            txt = str(record[0])+ " " + str(record[1])
            Radiobutton(self.selector, text=txt, variable=self.radio_var,
                        value=oid).grid(row=pos, column=0, sticky=W)
            pos += 1

        return pos

    def window_checks(self, tb_data):
        '''
        This function makes sure that the database is not empty,
        and returns all record or records with the searched f_name.
        '''
        try:
            self.selector.destroy()
            func = "update data"
        except:
            func = "show data"
            pass

        chk = self.check_db()
        if not chk:
            return []

        chk = self.check_search_data(tb_data, func)

        if chk == "search record":
            # only records which match textbox content
            records = self.find_records(tb_data)
        elif chk == "all records":
            # all records
            records = self.find_records()
        elif chk == "abort":
            # abort
            return []

        return records

    def edit_record(self, oid, data):
        '''
        This function calls the editor if a radio button is selected
        '''
        # Check whether one radio button is selected
        # XXX why does the selector window close here?
        chk = self.check_sel(oid)
        if chk:
            self.selector.destroy()
            self.editor.make_window(oid) #
            #self.make_window(data)

    def make_window(self, data):
        '''
        This function creates a window to show the records is the database.
        If the textboxes are empty, then all records are shown.
        If the name textboxes have content, then only records with this name are displayed.
        '''
        records = self.window_checks(data)
        if len(records) == 0:
            return

        self.selector = Tk()
        y_win = 150 + len(records)*20
        self.selector.geometry("400x"+ str(y_win))
        self.selector.title("Records")

        pos = self.print_records(records)

        edit_btn = Button(self.selector, text="Edit Record",
                          command=lambda: self.edit_record(self.radio_var.get(), data))
        edit_btn.grid(row=pos, column=0, columnspan=2, pady=(20, 0), padx=10, ipadx=135)

        delete_btn = Button(self.selector, text="Delete Record", 
                            command=lambda: [self.editor.delete_record(self.radio_var.get()),
                                             self.make_window(data)])
        delete_btn.grid(row=pos+1, column=0, columnspan=2, pady=(5, 0), padx=10, ipadx=125)

        close_btn = Button(self.selector, text="Close", command=self.selector.destroy)
        close_btn.grid(row=pos+2, column=0, columnspan=2, pady=(5, 0), padx=10, ipadx=153)
