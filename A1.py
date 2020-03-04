# ##############################################
# # Author: Sagar Suri
# # Class: CCT 211, Winter 2020
# # Assignment #2
# # Due: 02/04/2020
# #
# # Description: The program is being created to add newly registered businesses in 
# # Mississauga and reduce errors while doing so.

# ##############################################

# from tkinter import *
# from tkinter.ttk import *
# import csv
# import tkinter.font as font
# import re
# import time
# import os

# '''
# Primary function for the assignment
# '''
# def A1():    
 
#     root = Tk()

#     # storing entries and error labels for easy modification later
#     entries = {}    
#     error_labels = {}

#     # Styling and Tkinter macOS bug adjustments

#     font = "Roboto"
#     background="#F1FBF7"
#     root.configure(background=background)
#     style = Style()
#     style.theme_use('classic') 
#     style.configure("TButton",
#         highlightcolor="#216657", background="#39A78E", 
#         foreground="white", relief="flat", font=(font, 20))

    
#     ############## Helper Functions Section ###################

#     ''' Basically grid but with spacing and responsive configurations '''
#     def responsive_grid(widget, row, col, padx=10, pady=15, columnspan=1):
#         widget.grid(row=row, column=col, sticky="NSEW", padx=padx, pady=pady, columnspan=columnspan)
#         root.grid_rowconfigure(row, weight=1)
#         root.grid_columnconfigure(col, weight=1)

#     ''' Creates a Field Group with: Label, Entry, Label for displaying errors '''
#     def plot_label_and_entry(label, row, col):
#         label_text = label + ": "
#         label_widget = Label(root, text=label_text, background=background,font=(font, 18))
#         entry = Entry(root, background="white")
#         error_label = Label(root, text="...", background=background, width=8)
#         # Grid them all next to each other
#         responsive_grid(label_widget,row, col)
#         responsive_grid(entry,row, col+1)
#         responsive_grid(error_label,row, col+2)
        
#         # Store in dictionaries for easy access 
#         entries[label] = entry
#         error_labels[label] = error_label

#     ''' Creates a Section which contains many Field Groups '''
#     def make_section(section_name, column, label_list):
#         # Section Label in row 0, field groups start in row 1
#         section_label = Label(root, text=section_name, 
#         foreground="white", background="#39A78E", font=(font, 30))
#         responsive_grid(section_label, 0, column, 0, 0, 3)

#         row_count = 1
#         for entry_label in label_list:
#             plot_label_and_entry(entry_label, row_count, column)
#             row_count+=1

#     ''' runs the validate command of every entry to double check 
#         or just as a way to focus out to trigger the last validation '''
#     def check_all():
#         return_val = True
#         for entry in entries.values():
#             if not entry.validate():
#                 return_val = False
#         return return_val

#     def write_csv():
#         if check_all():
#             newfile = not os.path.exists('mississauga_business_data_record.csv')
        

#             # copied headers from sample file, they differ a bit from the data dictionary
#             headers = ["CENT_X", "CENT_Y", "BusinessID", "Name", "StreetNo", "StreetName", "UnitNo", "PostalCode",
#                 "Location", "Ward", "NAICSSector", "EmplRange", "Phone", "Fax", "Email", "WebAddress"]

#             try: 
#                 # Open a new csv for writing, add headers and entry
#                 with open("mississauga_business_data_record.csv", 'w', newline='') as csvfile:
#                     csv_writer = csv.writer(csvfile, delimiter=',',
#                                             quotechar='"', quoting=csv.QUOTE_MINIMAL)
#                     if newfile:
#                         csv_writer.writerow(headers)
#                     row_list = []
#                     for label in labels:
#                         row_list.append(entries[label].get())

#                     csv_writer.writerow(row_list)
#             except FileNotFoundError:
#                 print("\nThe program could not open a CSV file. \n")  

#     ############### UI CREATION SECTION ###############
    
#     # Creation of UI elements using the above helper functions, split into 3 sections
#     business_labels = ["Name", "BusinessID", "EmplRange", "NAICSSector"]
#     address_labels = ["StreetNo", "StreetName", "UnitNo", "PostalCode", "Location", "Ward", "CENT_X", "CENT_Y"]
#     contact_labels = ["Phone", "Fax", "Email", "WebAddress"]
#     labels = business_labels + address_labels + contact_labels

#     make_section("Business", 0, business_labels)
#     make_section("Address", 3, address_labels)
#     make_section("Contact", 6, contact_labels)

#     add_to_csv_btn = Button(root, text="Add Record", style="TButton", command=write_csv)
#     responsive_grid(add_to_csv_btn, 18, 7)

#     done_btn = Button(root, text="Validate", style="TButton", command=check_all)
#     responsive_grid(done_btn, 17, 7)

#     ############### VALIDATION SECTION ###############

#     ############ HELPERS ############

#     '''Generic validatecommand and invalidcommand functions'''
#     def validate(entry_text, widget_name):
#         # match pattern from dictionary of regexpatterns for each widget
#         pattern = re.compile(patterns[widget_name])
#         # Green "Valid" label on valid
#         error_labels[widget_name].configure(text="Valid", foreground="green")
#         return pattern.match(entry_text) is not None

#     def invalid(widget):
#         entry, error_label = entries[widget], error_labels[widget]
#         # Clear entry and Red "Invalid" label on invalid
#         # entry.delete(0, 'end')
#         error_label.configure(text="Invalid",foreground="red")

#     '''A business name can't just be a number'''
#     def name_validate(business_name, widget_name):
#         if business_name.isnumeric() or business_name == "":
#             return False
#         else:
#             error_labels[widget_name].configure(text="Valid", foreground="green")
#             return True

#     ############ REGEX patterns for all entries ############

#     patterns = {}
#     # patterns['Name'] has it's own validation function
#     patterns['BusinessID'] = "[0-9]{4,5}$"
#     patterns['EmplRange'] = "^\d+-\d+$"
#     patterns['NAICSSector'] = "^\D+$"
#     patterns['StreetNo'] = "^\d+$"
#     patterns['StreetName'] = "\D+"
#     patterns['UnitNo'] = ".*"
#     #PostalCode: Assuming user will always put a space in between first 3 and last 3 characters:
#     patterns['PostalCode'] = "^\D{1}\d{1}\D{1} {1}\d{1}\D{1}\d{1}$" 
#     patterns['Location'] = "\D+"
#     patterns['Ward'] = "^([1-9]|1[01])$"
#     #CENT_X: exactly like the sample csv 6 digits before . for CENT_X, and 7 before . for 
#     patterns['CENT_X'] = "^[0-9]{6}\.{1}[0-9]{2,4}$"
#     patterns['CENT_Y'] = "^[0-9]{7}\.{1}[0-9]{2,4}$"
#     #Phone: Assuming dash seperation
#     patterns['Phone'] = "^\d{3}-\d{3}-\d{4}$"
#     patterns['Fax'] = "^\d{3}-\d{3}-\d{4}$"
#     #Email: this will match stuff like sagar_13@live.com and sagar.suri@mail.utoronto.ca:
#     patterns['Email'] = "^[\w\.]+@[a-zA-Z_\.]+?\.[a-zA-Z]{2,3}$"
#     # this will match stuff like: https://www.regextester.com/94502
#     patterns['WebAddress'] = "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"

#     ############ REGEX patterns for all entries ############

#     # Register each function, assign validatecommand and invalidcommand for all 16 fields. 
#     Name = (root.register(name_validate), "%P", "Name")
#     entries['Name'].configure(validate="focusout", validatecommand=Name, 
#                     invalidcommand=lambda: invalid('Name'))
#     BusinessID = (root.register(validate), "%P", "BusinessID")
#     entries['BusinessID'].configure(validate="focusout", validatecommand=BusinessID, 
#                     invalidcommand=lambda: invalid('BusinessID'))
#     EmplRange = (root.register(validate), "%P", "EmplRange")
#     entries['EmplRange'].configure(validate="focusout", validatecommand=EmplRange, 
#                     invalidcommand=lambda: invalid('EmplRange'))
#     NAICSSector = (root.register(validate), "%P", "NAICSSector")
#     entries['NAICSSector'].configure(validate="focusout", validatecommand=NAICSSector, 
#                     invalidcommand=lambda: invalid('NAICSSector'))
#     StreetNo = (root.register(validate), "%P", "StreetNo")
#     entries['StreetNo'].configure(validate="focusout", validatecommand=StreetNo, 
#                     invalidcommand=lambda: invalid('StreetNo'))
#     StreetName = (root.register(validate), "%P", "StreetName")
#     entries['StreetName'].configure(validate="focusout", validatecommand=StreetName, 
#                     invalidcommand=lambda: invalid('StreetName'))
#     UnitNo = (root.register(validate), "%P", "UnitNo")
#     entries['UnitNo'].configure(validate="focusout", validatecommand=UnitNo, 
#                     invalidcommand=lambda: invalid('UnitNo'))
#     PostalCode = (root.register(validate), "%P", "PostalCode")
#     entries['PostalCode'].configure(validate="focusout", validatecommand=PostalCode, 
#                     invalidcommand=lambda: invalid('PostalCode'))
#     Location = (root.register(validate), "%P", "Location")
#     entries['Location'].configure(validate="focusout", validatecommand=Location, 
#                     invalidcommand=lambda: invalid('Location'))
#     Ward = (root.register(validate), "%P", "Ward")
#     entries['Ward'].configure(validate="focusout", validatecommand=Ward, 
#                     invalidcommand=lambda: invalid('Ward'))
#     CENT_X = (root.register(validate), "%P", "CENT_X")
#     entries['CENT_X'].configure(validate="focusout", validatecommand=CENT_X, 
#                     invalidcommand=lambda: invalid('CENT_X'))
#     CENT_Y = (root.register(validate), "%P", "CENT_Y")
#     entries['CENT_Y'].configure(validate="focusout", validatecommand=CENT_Y, 
#                     invalidcommand=lambda: invalid('CENT_Y'))
#     Phone = (root.register(validate), "%P", "Phone")
#     entries['Phone'].configure(validate="focusout", validatecommand=Phone, 
#                     invalidcommand=lambda: invalid('Phone'))
#     Fax = (root.register(validate), "%P", "Fax")
#     entries['Fax'].configure(validate="focusout", validatecommand=Fax, 
#                     invalidcommand=lambda: invalid('Fax'))
#     Email = (root.register(validate), "%P", "Email")
#     entries['Email'].configure(validate="focusout", validatecommand=Email, 
#                     invalidcommand=lambda: invalid('Email'))
#     WebAddress = (root.register(validate), "%P", "WebAddress")
#     entries['WebAddress'].configure(validate="focusout", validatecommand=WebAddress, 
#                     invalidcommand=lambda: invalid('WebAddress'))
         
#     root.mainloop()

# if __name__ == "__main__":
#     A1()

  
##############################################
# Author: Sagar Suri
# Class: CCT 211, Winter 2020
# Assignment #1
# Due: 02/04/2020
#
# Description: The program is being created to add newly registered businesses in 
# Mississauga and reduce errors while doing so.

##############################################

from tkinter import *
from tkinter.ttk import *
import csv
import tkinter.font as font
import re
import time

'''
Primary function for the assignment
'''
def A1():    
 
    root = Tk()

    # storing entries and error labels for easy modification later
    entries = {}    
    error_labels = {}

    # Styling and Tkinter macOS bug adjustments

    font = "Roboto"
    background="#F1FBF7"
    root.configure(background=background)
    style = Style()
    style.theme_use('classic') 
    style.configure("TButton",
        highlightcolor="#216657", background="#39A78E", 
        foreground="white", relief="flat", font=(font, 20))

    
    ############## Helper Functions Section ###################

    ''' Basically grid but with spacing and responsive configurations '''
    def responsive_grid(widget, row, col, padx=10, pady=15, columnspan=1):
        widget.grid(row=row, column=col, sticky="NSEW", padx=padx, pady=pady, columnspan=columnspan)
        

    ''' Creates a Field Group with: Label, Entry, Label for displaying errors '''
    def plot_label_and_entry(label, row, col):
        label_text = label + ": "
        label_widget = Label(root, text=label_text, background=background,font=(font, 18))
        entry = Entry(root, background="white")
        error_label = Label(root, text="...", background=background, width=8)
        # Grid them all next to each other
        responsive_grid(label_widget,row, col)
        responsive_grid(entry,row, col+1)
        responsive_grid(error_label,row, col+2)
        
        # Store in dictionaries for easy access 
        entries[label] = entry
        error_labels[label] = error_label

    ''' Creates a Section which contains many Field Groups '''
    def make_section(section_name, column, label_list):
        # Section Label in row 0, field groups start in row 1
        section_label = Label(root, text=section_name, 
        foreground="white", background="#39A78E", font=(font, 30))
        responsive_grid(section_label, 0, column, 0, 0, 3)

        row_count = 1
        for entry_label in label_list:
            plot_label_and_entry(entry_label, row_count, column)
            row_count+=1

    ''' runs the validate command of every entry to double check 
        or just as a way to focus out to trigger the last validation '''
    def check_all():
        return_val = True
        for entry in entries.values():
            if not entry.validate():
                return_val = False
        return return_val

    ''' Adds all values to the csv '''
    def write_csv():
        if check_all() or True:
            print("Data Successfully Added to CSV")
      
            file_exists = False

            # copied headers from sample file, they differ a bit from the data dictionary
            headers = ["CENT_X", "CENT_Y", "BusinessID", "Name", "StreetNo", "StreetName", "UnitNo", "PostalCode",
                "Location", "Ward", "NAICSSector", "EmplRange", "Phone", "Fax", "Email", "WebAddress"]

            # Try reading the file to see if it exists
            try:
                with open('mississauga_business_data_record.csv', 'r') as csvfile:
                    csv_dict = [row for row in csv.DictReader(csvfile)]
                    if len(csv_dict) > 0:
                        file_exists = True
            except FileNotFoundError:
                file_exists = False

        
            if not file_exists:
                try: 
                    # Open a new csv for writing, add headers and entry
                    with open("mississauga_business_data_record.csv", 'w', newline='') as csvfile:
                        csv_writer = csv.writer(csvfile, delimiter=',',
                                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        csv_writer.writerow(headers)
                        row_list = []
                        for label in headers:
                            row_list.append(entries[label].get())

                        csv_writer.writerow(row_list)
                except FileNotFoundError:
                    print("\nThe program could not open a CSV file. \n")

            else: 
                # Append to an existing csv, ASSUME HEADER IS PRESENT 
                with open("mississauga_business_data_record.csv", 'a', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile, delimiter=',',
                                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    row_list = []
                    for label in headers:
                        row_list.append(entries[label].get())

                    csv_writer.writerow(row_list)
      

    ############### UI CREATION SECTION ###############
    
    # Creation of UI elements using the above helper functions, split into 3 sections
    business_labels = ["Name", "BusinessID", "EmplRange", "NAICSSector"]
    address_labels = ["StreetNo", "StreetName", "UnitNo", "PostalCode", "Location", "Ward", "CENT_X", "CENT_Y"]
    contact_labels = ["Phone", "Fax", "Email", "WebAddress"]
    labels = business_labels + address_labels + contact_labels

    make_section("Business", 0, business_labels)
    make_section("Address", 3, address_labels)
    make_section("Contact", 6, contact_labels)

    add_to_csv_btn = Button(root, text="Add Record", style="TButton", command=write_csv)
    responsive_grid(add_to_csv_btn, 18, 7)

    done_btn = Button(root, text="Validate", style="TButton", command=check_all)
    responsive_grid(done_btn, 17, 7)
    for x in range(10):
        root.grid_rowconfigure(x, weight=1)
        root.grid_columnconfigure(x, weight=1)

    ############### VALIDATION SECTION ###############

    ############ HELPERS ############

    '''Generic validatecommand and invalidcommand functions'''
    def validate(entry_text, widget_name):
        # match pattern from dictionary of regexpatterns for each widget
        pattern = re.compile(patterns[widget_name])
        # Green "Valid" label on valid
        error_labels[widget_name].configure(text="Valid", foreground="green")
        return pattern.match(entry_text) is not None

    def invalid(widget):
        entry, error_label = entries[widget], error_labels[widget]
        # Clear entry and Red "Invalid" label on invalid
        # entry.delete(0, 'end')
        error_label.configure(text="Invalid",foreground="red")

    '''A business name can't just be a number'''
    def name_validate(business_name, widget_name):
        if business_name.isnumeric() or business_name == "":
            return False
        else:
            error_labels[widget_name].configure(text="Valid", foreground="green")
            return True

    ############ REGEX patterns for all entries ############

    patterns = {}
    # patterns['Name'] has it's own validation function
    patterns['BusinessID'] = "[0-9]{4,5}$"
    patterns['EmplRange'] = "^\d+-\d+$"
    patterns['NAICSSector'] = "^\D+$"
    patterns['StreetNo'] = "^\d+$"
    patterns['StreetName'] = "\D+"
    patterns['UnitNo'] = ".*"
    #PostalCode: Assuming user will always put a space in between first 3 and last 3 characters:
    patterns['PostalCode'] = "^\D{1}\d{1}\D{1} {1}\d{1}\D{1}\d{1}$" 
    patterns['Location'] = "\D+"
    patterns['Ward'] = "^([1-9]|1[01])$"
    #CENT_X: exactly like the sample csv 6 digits before . for CENT_X, and 7 before . for CENT_Y
    patterns['CENT_X'] = "^[0-9]{6}\.{1}[0-9]{2,4}$"
    patterns['CENT_Y'] = "^[0-9]{7}\.{1}[0-9]{2,4}$"
    #Phone: Assuming dash seperation
    patterns['Phone'] = "^\d{3}-\d{3}-\d{4}$"
    patterns['Fax'] = "^\d{3}-\d{3}-\d{4}$"
    #Email: this will match stuff like sagar_13@live.com and sagar.suri@mail.utoronto.ca:
    patterns['Email'] = "^[\w\.]+@[a-zA-Z_\.]+?\.[a-zA-Z]{2,3}$"
    # this will match stuff like: https://www.regextester.com/94502
    patterns['WebAddress'] = "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"

    ############ REGEX patterns for all entries ############

    # Register each function, assign validatecommand and invalidcommand for all 16 fields. 
    Name = (root.register(name_validate), "%P", "Name")
    entries['Name'].configure(validate="focusout", validatecommand=Name, 
                    invalidcommand=lambda: invalid('Name'))
    BusinessID = (root.register(validate), "%P", "BusinessID")
    entries['BusinessID'].configure(validate="focusout", validatecommand=BusinessID, 
                    invalidcommand=lambda: invalid('BusinessID'))
    EmplRange = (root.register(validate), "%P", "EmplRange")
    entries['EmplRange'].configure(validate="focusout", validatecommand=EmplRange, 
                    invalidcommand=lambda: invalid('EmplRange'))
    NAICSSector = (root.register(validate), "%P", "NAICSSector")
    entries['NAICSSector'].configure(validate="focusout", validatecommand=NAICSSector, 
                    invalidcommand=lambda: invalid('NAICSSector'))
    StreetNo = (root.register(validate), "%P", "StreetNo")
    entries['StreetNo'].configure(validate="focusout", validatecommand=StreetNo, 
                    invalidcommand=lambda: invalid('StreetNo'))
    StreetName = (root.register(validate), "%P", "StreetName")
    entries['StreetName'].configure(validate="focusout", validatecommand=StreetName, 
                    invalidcommand=lambda: invalid('StreetName'))
    UnitNo = (root.register(validate), "%P", "UnitNo")
    entries['UnitNo'].configure(validate="focusout", validatecommand=UnitNo, 
                    invalidcommand=lambda: invalid('UnitNo'))
    PostalCode = (root.register(validate), "%P", "PostalCode")
    entries['PostalCode'].configure(validate="focusout", validatecommand=PostalCode, 
                    invalidcommand=lambda: invalid('PostalCode'))
    Location = (root.register(validate), "%P", "Location")
    entries['Location'].configure(validate="focusout", validatecommand=Location, 
                    invalidcommand=lambda: invalid('Location'))
    Ward = (root.register(validate), "%P", "Ward")
    entries['Ward'].configure(validate="focusout", validatecommand=Ward, 
                    invalidcommand=lambda: invalid('Ward'))
    CENT_X = (root.register(validate), "%P", "CENT_X")
    entries['CENT_X'].configure(validate="focusout", validatecommand=CENT_X, 
                    invalidcommand=lambda: invalid('CENT_X'))
    CENT_Y = (root.register(validate), "%P", "CENT_Y")
    entries['CENT_Y'].configure(validate="focusout", validatecommand=CENT_Y, 
                    invalidcommand=lambda: invalid('CENT_Y'))
    Phone = (root.register(validate), "%P", "Phone")
    entries['Phone'].configure(validate="focusout", validatecommand=Phone, 
                    invalidcommand=lambda: invalid('Phone'))
    Fax = (root.register(validate), "%P", "Fax")
    entries['Fax'].configure(validate="focusout", validatecommand=Fax, 
                    invalidcommand=lambda: invalid('Fax'))
    Email = (root.register(validate), "%P", "Email")
    entries['Email'].configure(validate="focusout", validatecommand=Email, 
                    invalidcommand=lambda: invalid('Email'))
    WebAddress = (root.register(validate), "%P", "WebAddress")
    entries['WebAddress'].configure(validate="focusout", validatecommand=WebAddress, 
                    invalidcommand=lambda: invalid('WebAddress'))
         
    root.mainloop()

if __name__ == "__main__":
    A1()

  

      
