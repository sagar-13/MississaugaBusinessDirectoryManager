from model import *
from view import *
import tkinter as tk
from tkinter.ttk import *

'''Creates the model, view, and controller for the application and runs it.
'''
class Controller:
    
    def __init__(self):
        self.model = Model()
        self.root = tk.Tk()
        self.view = View(self.root, self)

        self.root.mainloop()
    def open_file(self):
        self.model.open_file()
   
    def set_selected(self, row_num):
        self.model.select_row(row_num)

    def edit_model(self, entries):
        self.model.edit_record(entries)

    def add_to_model(self, entries):
        self.model.append_record(entries)

    def get_records(self):
        return self.model.get_all_records()
           
        
            
                 
if __name__ == "__main__":
    app = Controller()
