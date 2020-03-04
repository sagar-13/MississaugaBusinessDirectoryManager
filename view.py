from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import tkinter.font as font
import re
from tkinter import messagebox

from model import *
from controller import *


''' The visual interface for the application'''
class View():

    def __init__(self, root, controller):
        
        # The controller passes an instance of itself as well as the top level root
        self.controller = controller
        self.root = root

        # data which needs to be stored and used
        self.entries = {}
        self.error_labels = {}
        # creates a dict will regular expression to validate each entry field 
        self.patterns = {}
        self.init_patterns()
        self.headers = ["CENT_X", "CENT_Y", "BusinessID", "Name", "StreetNo", "StreetName", "UnitNo", "PostalCode",
                    "Location", "Ward", "NAICSSector", "EmplRange", "Phone", "Fax", "Email", "WebAddress"]
        
         # Styling and Tkinter macOS bug adjustments
        self.font = "Roboto"
        self.background="#F1FBF7"
        self.root.option_add('*tearOff', FALSE)
        self.root.configure(background=self.background)
        style = Style()
        style.theme_use('classic') 
        style.configure("TButton",
            highlightcolor="#216657", background="#39A78E", 
            foreground="white", relief="flat", font=(self.font, 20))

        # Creates one frame to edit records and one frame to select csv records
        self.records_frame = tk.Frame(self.root)
        self.treeview_frame = tk.Frame(self.root)
        self.records_frame.configure(background=self.background)
        self.treeview_frame.configure(background=self.background)


        # Creation of UI elements 
        business_labels = ["Name", "BusinessID", "EmplRange", "NAICSSector"]
        address_labels = ["StreetNo", "StreetName", "UnitNo", "PostalCode", "Location", "Ward", "CENT_X", "CENT_Y"]
        contact_labels = ["Phone", "Fax", "Email", "WebAddress"]
        self.label_helpers = dict.fromkeys(business_labels + address_labels + contact_labels)

        # Helper label hints 
        self.label_helpers['BusinessID'] = "4-5 Digits"
        self.label_helpers['EmplRange'] = "eg. 1-12"
        self.label_helpers['PostalCode'] = "L6Y 5E7"
        self.label_helpers['Ward'] = "Number from 1-11"
        self.label_helpers['Phone']= "###-###-####"
        self.label_helpers['Fax']= "###-###-####"

        # Create and grid all of the elements for the record fields screen using helpers
        self.section_label_records = Label(self.records_frame, text="""
        Edit the selected record or append a new record with the following data:     
        """, 
        foreground="white", background="#39A78E", font=(self.font, 20), relief=SOLID )    
        self.responsive_grid(self.section_label_records, 0, 0, 5, 10, 9)
        self.make_section("Business", 0, business_labels)
        self.make_section("Address", 3, address_labels)
        self.make_section("Contact", 6, contact_labels)

        # Create and grid the buttons, edit, append, and validate.
        self.edit_record_btn = Button(self.records_frame, text="Edit Selected Record", style="TButton", command=self.edit_record)
        self.responsive_grid(self.edit_record_btn, 18, 7)

        self.done_btn = Button(self.records_frame, text="Validate", style="TButton", command=self.check_all)
        self.responsive_grid(self.done_btn, 17, 7)

        self.add_to_csv_btn = Button(self.records_frame, text="Append New Record", style="TButton", command=self.add_csv)
        self.responsive_grid(self.add_to_csv_btn, 19, 7)

        # Button states are initially disabled until the user has selected a file.
        self.add_to_csv_btn["state"] = DISABLED
        self.edit_record_btn["state"] = DISABLED

        # Register the validation functions for each entry
        self.register_all_validations()


        ###### Creation of the second screen which holds the treeview ####

   
        self.section_label_treeview = Label(self.treeview_frame, text="""
        Welcome to the Mississauga Business Directory Manager!  
        Select a file from the menu to begin adding/editing records.    
        (Double-click a record to edit it)  
        """, foreground="white", background="#39A78E", font=(self.font, 20), relief=SOLID)    

        # Create and style the treeview
        style.configure("mystyle.Treeview", font=(font, 14)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=(font, 15,'bold')) # Modify the font of the headings
        # style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders

        self.tv = Treeview(self.treeview_frame, columns=self.headers, 
                            height=20, selectmode='browse', style="mystyle.Treeview")
        self.tv.heading("#0", text="Record #")
        self.tv.column("#0",minwidth=40,width=80, stretch=NO) 
        
        # configure the treeview headings
        record_number = 0
        for header in self.headers:
            col = str(record_number)
            self.tv.heading(col, text=header)
            self.tv.column(col,minwidth=0,width=150, stretch=NO) 
            record_number +=1

        # Add both a horizontal and vertical scrollbar
        self.scrollbarx = Scrollbar(self.treeview_frame, orient=tk.HORIZONTAL,
        command=self.tv.xview)
        self.tv.configure(xscrollcommand=self.scrollbarx.set)
        
        self.scrollbary = Scrollbar(self.treeview_frame, orient=tk.VERTICAL,
        command=self.tv.yview)
        self.tv.configure(yscrollcommand=self.scrollbary.set)

        # grid everything for the treeview
        self.tv.bind("<Double-1>", self.OnDoubleClick)
        self.responsive_grid(self.section_label_treeview, 0, 0, 0, 10, 1)
        self.scrollbarx.grid(row=2)
        self.scrollbary.grid(row=1, column=0, sticky='NSE')
        self.tv.grid(row=1, column=0, sticky="SW")

         # Create the menu
        # magic names for each menu
        if (self.root.tk.call('tk', 'windowingsystem') != "win32"):
            menubar = Menu(self.root, name="apple")
           
        else: 
            menubar = Menu(self.root, name='system')
  
        # File Menu
        menu_file = Menu(menubar)
        menu_file.add_command(label="Show Record List", command=self.raise_treeview)
        menu_file.add_command(label="Show Record Fields", command=self.raise_fields)
        menu_file.add_command(label="Select File", command=self.open_file)
        menu_file.add_command(label="Quit", command=self.quit_app)
        menubar.add_cascade(menu=menu_file, label="File")
        
        # MacOS help and window menus 
        # if (self.root.tk.call('tk', 'windowingsystem') != "win32"):
        help_menu_mac = Menu(menubar, name="help")
        window_menu_mac = Menu(menubar, name="window")
        menubar.add_cascade(menu=help_menu_mac, label="Help")
        menubar.add_cascade(menu=window_menu_mac, label="Window")

        self.root['menu'] = menubar
    

        # Finally, add both frames to the root
        self.responsive_grid(self.treeview_frame)
        self.responsive_grid(self.records_frame)

        # Make everything resize better
        for x in range(10):
            self.root.grid_rowconfigure(x, weight=1)
            self.root.grid_columnconfigure(x, weight=1)
            self.records_frame.grid_rowconfigure(x, weight=1)
            self.records_frame.grid_columnconfigure(x, weight=1)
            self.treeview_frame.grid_rowconfigure(x, weight=1)
            self.treeview_frame.grid_columnconfigure(x, weight=1)

    def quit_app(self):
     
        if messagebox.askyesno(title="Quit", message="Are you sure you would like to exit?"):
            quit()

    '''Tells the controller to open a new file and populates the treeview 
        with that files records'''
    def open_file(self):
        self.add_to_csv_btn["state"] = NORMAL
        self.controller.open_file()
        self.populate_treeview()
        
    ''' Populate Treeview and number all of the records starting from 1 '''
    def populate_treeview(self):
        self.tv.delete(*self.tv.get_children())
        csv_list = self.controller.get_records()[1:]
      
        record_number = 1
        for entry in csv_list:
            self.tv.insert(
                "",
                "end",
                text=str(record_number),
                values=entry
            )
            record_number+=1
        self.treeview_frame.tkraise()
        
    ''' show the entries screen'''
    def raise_fields(self):
        self.records_frame.tkraise()
    ''' show the records screen with the treeview'''
    def raise_treeview(self):
        self.treeview_frame.tkraise()

    '''Actions for when the user double-clicks on a record. 
    The edit record button is unlocked, and the entry fields 
    are auto-filled with that record's data'''
    def OnDoubleClick(self, event):
        self.edit_record_btn["state"] = NORMAL

        # Tell the controller to assign the selected row in the Model
        curItem = self.tv.focus()
        selected_num = self.tv.item(curItem)['text']
        self.controller.set_selected(selected_num)

        # Create a dictionary to reference the current entries by header name
        record_dict ={}
        records = self.tv.item(curItem)['values']
        index = 0
        
        for header in self.headers:
            record_dict[header] = records[index]
            index +=1
            # autofill entries
            entry = self.entries[header]
            entry.delete(0,END)
            entry.insert(0,record_dict[header])
        
        # Show the entries and validate them all just to give the user feedback
        self.records_frame.tkraise()
        self.check_all()
   
    ''' Basically grid but with spacing and responsive configurations '''
    def responsive_grid(self, widget, row=0, col=0, padx=5, pady=15, columnspan=1):
        widget.grid(row=row, column=col, sticky="NSEW", padx=padx, pady=pady, columnspan=columnspan)
       

    ''' Creates a Field Group with: Label, Entry, Label for displaying errors '''
    def plot_label_and_entry(self, label, row, col):
        label_text = label + ":"
        label_widget = Label(self.records_frame, text=label_text, background=self.background,font=(self.font, 18))
        entry = Entry(self.records_frame, background="white")
        error_label = Label(self.records_frame, text="...", background=self.background, width=8)
        helper_label = Label(self.records_frame, text=self.label_helpers[label], background=self.background)
        
        # Grid them all next to each other
        self.responsive_grid(label_widget,row, col)
        self.responsive_grid(entry,row, col+1)
        self.responsive_grid(error_label,row, col+2)
        self.responsive_grid(helper_label,row+1, col, padx=10, pady=0)
        
        # Store in dictionaries for easy access 
        self.entries[label] = entry
        self.error_labels[label] = error_label
        self.label_helpers[label] = helper_label

    ''' Creates a Section which contains many Field Groups '''
    def make_section(self, section_name, column, label_list):
        # Section Label in row 0, field groups start in row 1
        section_label = Label(self.records_frame, text=section_name, 
        foreground="white", background="#39A78E", font=(self.font, 30))
        self.responsive_grid(section_label, 1, column, 0, 0, 3)

        row_count = 2
        for entry_label in label_list:
            self.plot_label_and_entry(entry_label, row_count, column)
            row_count+=2

    ''' runs the validate command of every entry to double check 
        or just as a way to focus out to trigger the last validation '''
    def check_all(self):
        return_val = True
        for entry in self.entries.values():
            if not entry.validate():
                return_val = False
        return return_val

    '''If all the fields are valid, tell the controller to add to the model, 
        and then populate the treeview with the updated data'''
    def add_csv(self):
        if self.check_all():
            self.controller.add_to_model(self.entries)
            self.populate_treeview()
        else: 
            messagebox.showinfo(title="Check Fields", message="Make sure all fields are valid!")
   
    '''If all the fields are valid, tell the controller to EDIT the currently, 
        selected row in the model, and then populate the treeview with the updated data'''
    def edit_record(self):
        if self.check_all():
            self.controller.edit_model(self.entries)
            self.populate_treeview()
            self.edit_record_btn["state"] = DISABLED
        else: 
            messagebox.showinfo(title="Check Fields", message="Make sure all fields are valid!")
        
    '''Generic validatecommand and invalidcommand functions'''
    def validate(self, entry_text, widget_name):
        # match pattern from dictionary of regexpatterns for each widget
        pattern = re.compile(self.patterns[widget_name])
        # Green "Valid" label on valid
        self.error_labels[widget_name].configure(text="Valid", foreground="green")
        return pattern.match(entry_text) is not None

    def invalid(self, widget):
        entry, error_label = self.entries[widget], self.error_labels[widget]
        # Clear entry and Red "Invalid" label on invalid
        # entry.delete(0, 'end')
        error_label.configure(text="Invalid",foreground="red")

    '''A business name can't just be a number'''
    def name_validate(self,business_name, widget_name):
        if business_name.isnumeric() or business_name == "":
            return False
        else:
            self.error_labels[widget_name].configure(text="Valid", foreground="green")
            return True

    '''
    REGEX patterns for all entries, add them to self.patters
    '''
    def init_patterns(self):
        # patterns['Name'] has it's own validation function
        self.patterns['BusinessID'] = "[0-9]{4,5}$"
        self.patterns['EmplRange'] = "^\d+-\d+$"
        self.patterns['NAICSSector'] = "^\D+$"
        self.patterns['StreetNo'] = "^\d+$"
        self.patterns['StreetName'] = "\D+"
        self.patterns['UnitNo'] = ".*"
        #PostalCode: Assuming user will always put a space in between first 3 and last 3 characters:
        self.patterns['PostalCode'] = "^\D{1}\d{1}\D{1} {1}\d{1}\D{1}\d{1}$" 
        self.patterns['Location'] = "\D+"
        self.patterns['Ward'] = "^([1-9]|1[01])$"
        #CENT_X: exactly like the sample csv 6 digits before . for CENT_X, and 7 before . for 
        self.patterns['CENT_X'] = "^[0-9]{6}\.{1}[0-9]{2,4}$"
        self.patterns['CENT_Y'] = "^[0-9]{7}\.{1}[0-9]{2,4}$"
        #Phone: Assuming dash seperation
        self.patterns['Phone'] = "^\d{3}-\d{3}-\d{4}$"
        self.patterns['Fax'] = "^\d{3}-\d{3}-\d{4}$"
        #Email: this will match stuff like sagar_13@live.com and sagar.suri@mail.utoronto.ca:
        self.patterns['Email'] = "^[\w\.]+@[a-zA-Z_\.]+?\.[a-zA-Z]{2,3}$"
        # this will match stuff like: https://www.regextester.com/94502
        self.patterns['WebAddress'] = "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"

    '''Register each function, assign validatecommand and invalidcommand for all 16 fields.
        Validation is on focusout as some regular expressions match a certain length and key
        validations will prevent the user from typing. '''
    def register_all_validations(self):
        
        Name = (self.root.register(self.name_validate), "%P", "Name")
        self.entries['Name'].configure(validate="focusout", validatecommand=Name, 
                        invalidcommand=lambda: self.invalid('Name'))
        BusinessID = (self.root.register(self.validate), "%P", "BusinessID")
        self.entries['BusinessID'].configure(validate="focusout", validatecommand=BusinessID, 
                        invalidcommand=lambda: self.invalid('BusinessID'))
        EmplRange = (self.root.register(self.validate), "%P", "EmplRange")
        self.entries['EmplRange'].configure(validate="focusout", validatecommand=EmplRange, 
                        invalidcommand=lambda: self.invalid('EmplRange'))
        NAICSSector = (self.root.register(self.validate), "%P", "NAICSSector")
        self.entries['NAICSSector'].configure(validate="focusout", validatecommand=NAICSSector, 
                        invalidcommand=lambda: self.invalid('NAICSSector'))
        StreetNo = (self.root.register(self.validate), "%P", "StreetNo")
        self.entries['StreetNo'].configure(validate="focusout", validatecommand=StreetNo, 
                        invalidcommand=lambda: self.invalid('StreetNo'))
        StreetName = (self.root.register(self.validate), "%P", "StreetName")
        self.entries['StreetName'].configure(validate="focusout", validatecommand=StreetName, 
                        invalidcommand=lambda: self.invalid('StreetName'))
        UnitNo = (self.root.register(self.validate), "%P", "UnitNo")
        self.entries['UnitNo'].configure(validate="focusout", validatecommand=UnitNo, 
                        invalidcommand=lambda: self.invalid('UnitNo'))
        PostalCode = (self.root.register(self.validate), "%P", "PostalCode")
        self.entries['PostalCode'].configure(validate="focusout", validatecommand=PostalCode, 
                        invalidcommand=lambda: self.invalid('PostalCode'))
        Location = (self.root.register(self.validate), "%P", "Location")
        self.entries['Location'].configure(validate="focusout", validatecommand=Location, 
                        invalidcommand=lambda: self.invalid('Location'))
        Ward = (self.root.register(self.validate), "%P", "Ward")
        self.entries['Ward'].configure(validate="focusout", validatecommand=Ward, 
                        invalidcommand=lambda: self.invalid('Ward'))
        CENT_X = (self.root.register(self.validate), "%P", "CENT_X")
        self.entries['CENT_X'].configure(validate="focusout", validatecommand=CENT_X, 
                        invalidcommand=lambda: self.invalid('CENT_X'))
        CENT_Y = (self.root.register(self.validate), "%P", "CENT_Y")
        self.entries['CENT_Y'].configure(validate="focusout", validatecommand=CENT_Y, 
                        invalidcommand=lambda: self.invalid('CENT_Y'))
        Phone = (self.root.register(self.validate), "%P", "Phone")
        self.entries['Phone'].configure(validate="focusout", validatecommand=Phone, 
                        invalidcommand=lambda: self.invalid('Phone'))
        Fax = (self.root.register(self.validate), "%P", "Fax")
        self.entries['Fax'].configure(validate="focusout", validatecommand=Fax, 
                        invalidcommand=lambda: self.invalid('Fax'))
        Email = (self.root.register(self.validate), "%P", "Email")
        self.entries['Email'].configure(validate="focusout", validatecommand=Email, 
                        invalidcommand=lambda: self.invalid('Email'))
        WebAddress = (self.root.register(self.validate), "%P", "WebAddress")
        self.entries['WebAddress'].configure(validate="focusout", validatecommand=WebAddress, 
                        invalidcommand=lambda: self.invalid('WebAddress'))
            



        