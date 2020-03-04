import csv
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
'''
The model which makes changes the csv containing the information about 
Mississauga businesses. 
'''
class Model:

    def __init__(self):
        
        self.headers = ["CENT_X", "CENT_Y", "BusinessID", "Name", "StreetNo", "StreetName", "UnitNo", "PostalCode",
                "Location", "Ward", "NAICSSector", "EmplRange", "Phone", "Fax", "Email", "WebAddress"]
        self.filename = ""
        self.selected_row = -1

    def select_row(self, row_num):
        '''
        Each record is numbered. When the user selects a record, the selected_row is assigned
        '''
        self.selected_row = int(row_num)
        # print(self.selected_row)

    def open_file(self):
        '''Sets self.filename to whatever file the user picks so the model knows which file to open
        '''
        self.filename =  filedialog.askopenfilename(
            initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
        

    
    def edit_record(self, entries):
            ''' Edits the record referenced by self.selected_row using entries passed from the controller. '''
            if self.selected_row != -1:
                # Get the current csv, populate row_list with the current entries
                csv_list = self.get_all_records()[1:]
                row_list = []
                for label in self.headers:
                    row_list.append(entries[label].get())
                # assign row_list to the selected row
                csv_list[self.selected_row-1] = row_list
                
                # write the whole CSV again with the changes made 
                try: 
                    with open(self.filename, 'w', newline='') as csvfile:
                        csv_writer = csv.writer(csvfile, delimiter=',',
                                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        csv_writer.writerow(self.headers)
                        for row in csv_list:
                            csv_writer.writerow(row)
                except FileNotFoundError:
                    print("\nThe program could not open a CSV file. \n")  

    def append_record(self, entries):
        ''' Add a record to the end of the current csv'''
        try: 
            with open(self.filename, 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=',',
                                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
                row_list = []
                for label in self.headers:
                    row_list.append(entries[label].get())
                csv_writer.writerow(row_list)

        except FileNotFoundError:
            print("\nThe program could not open a CSV file. \n")  


    def get_all_records(self):
        '''Get every record in the csv, store it in a list.'''
        csv_list =[]
        try:
            with open(self.filename, 'r') as csvfile:
             
                csv_list = [row for row in csv.reader(csvfile)]

        except FileNotFoundError:
            pass

        return csv_list


