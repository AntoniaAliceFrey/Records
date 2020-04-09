# Records

## Table of contents
* [General info](#general-info)
* [How to Use](#setup)
* [Technologies Utilized](#technologies)
* [Preview](#preview)
* [Project Status](#status)
    * [Next Steps](#next-steps)
* [Conclusion](#conclusion)
* [Sources](#src)

## General info
*Records* is a database app built with Python, Tkinter, and SQLite.

## How to Use
To launch the app, open the *GUI.py* script via the console. To add a record into the database, fill in the first name, last name, email, and birtday fields and click the *Add Record* button. To search a particular entry, type the text to search in its corresponding field in the contact form and click the *Search Record* button. To view all database entries, click the *Search Record* button while the contact form is blank.
To change or delete records, search and select an entry and click the *Edit Record* or *Delete Record* button. Lastly, to return to the main window, click the *Close* button.

## Technologies Utilized
Project is created with:
* Tkinter
* SQLite

## Preview
<img src="images/gui.png" width="350">
<img src="images/selector.png" width="350">
<img src="images/editor.png" width="350">

## Project Status
Not perfect, but working.

#### Next Steps
Some ideas to improve the functionality:
- [ ] Some fix-me's in code
- [ ] Code cleanup with pylintrc file
- [ ] Create a dist folder, py2app
- [ ] Search record functionality
- [ ] Check birthday and email fields
- [ ] Birthday calendar or drop down menu
- [ ] Return to selector window after editing
- [ ] Select and delete multiple records
- [ ] Print (selected) records in excel file
- [ ] Send a conformation email to new record


## Conclusion
* Simple GUIs can be built with Tkinter windows and widgets. Tkinter arranges label, entry, and button widgets in a window using a grid layout. The button widgets can be linked to functions and the data in entry widgets can be extracted for use elsewhere.
* The main steps for working with a SQLite database are connecting to a database, creating a cursor object, writing an SQL query, commiting changes, and closing the database connection.

## Sources
This app is inspired by the [**Tkinter Course - Create Graphic User Interfaces in Python Tutorial**](https://www.youtube.com/watch?v=YXPyB4XeYLA&t=16842s) by [**freeCodeCamp.org**](https://www.youtube.com/channel/UC8butISFwT-Wl7EV0hUK0BQ).
