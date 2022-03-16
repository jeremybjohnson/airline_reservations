import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from src.classes.reservation import Reservation


class ShowRes(tk.Frame):
    def __init__(self, parent, controller, show_home, show_search, show_login):
        super().__init__(parent)
        tk.Frame.__init__(self, parent)
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.controller = controller
        self.show_home = show_home
        self.show_search = show_search
        self.show_login = show_login
        
        """Header Section"""
        header_container = ttk.Frame(self, height=80)
        header_container.grid(row=0, column=0, padx=10, pady=10, sticky='NSEW')
        header_container.columnconfigure(0, weight=1)
        
        header_label = ttk.Label(
            header_container,
            text='Reserved Flights',
            style='Header.TLabel'
        )
        header_label.place(relx=0.5, rely=0.5, anchor='center')

        """Tree Section"""
        self.tree_container = ttk.Frame(self, height=40)
        self.tree_container.grid(row=1, column=0, padx=10, pady=10, sticky='NSEW')
        self.tree_container.columnconfigure(0, weight=1)
        
        self.build_tree()
        
        """Button Section"""
        button_container = ttk.Frame(self, height=40)
        button_container.grid(row=2, column=0, padx=10, pady=10, sticky='NSEW')
        button_container.columnconfigure(0, weight=1)
        
        self.home_button = ttk.Button(
            button_container,
            text='Home',
            command=show_home,
            width=15,
            style = 'CustomButton.TButton',
        )
        self.home_button.grid(row=0, column=0, padx=10, pady=10, sticky='W')
        self.home_button.bind('<Return>', self.home_handler)
        self.home_button.bind('<Tab>', self.tab_order)
        
        self.cancel_button = ttk.Button(
            button_container,
            text='Cancel Reservation',
            command=self.cancel_flight,
            width=15,
            style = 'CustomButton.TButton',
        )
        self.cancel_button.grid(row=0, column=1, padx=10, pady=10, sticky='W')
        self.cancel_button.bind('<Return>', self.cancel_handler)
        
        self.search_button = ttk.Button(
            button_container,
            text='Search Flights',
            command=show_search,
            width=15,
            style = 'CustomButton.TButton',
        )
        self.search_button.grid(row=0, column=2, padx=10, pady=10, sticky='W')
        self.search_button.bind('<Return>', self.search_handler)

        self.login_button = ttk.Button(
            button_container,
            text='Login',
            command=show_login,
            width=15,
            style = 'CustomButton.TButton',
        )
        self.login_button.grid(row=0, column=3, padx=10, pady=10, sticky='W')
        self.login_button.bind('<Return>', self.login_handler)
        self.login_button.bind('<Tab>', self.tab_order_rev)
        
    def postupdate(self):  
        self.home_button.focus()
        self.build_tree()
        
        
    def home_handler(self, event):
        self.show_home()
        
        
    def cancel_handler(self, event):
        self.cancel_flight()
        
        
    def search_handler(self, event):
        self.show_search()
        
        
    def login_handler(self, event):
        self.show_login()
        
        
    def tab_order(self, event):
        widgets = [self.home_button, self.cancel_button, self.search_button, self.login_button]
        for w in widgets:
            w.lift()
            
            
    def tab_order_rev(self, event):
        widgets = [self.login_button, self.search_button, self.cancel_button, self.home_button]
        for w in widgets:
            w.lift()
        
        
    def build_tree(self):
        # Treeview scrollbar
        self.tree_scroll = ttk.Scrollbar(self.tree_container)
        self.tree_scroll.grid(row=0, column=1, sticky='NS')
        
        self.tree = ttk.Treeview(self.tree_container, yscrollcommand=self.tree_scroll.set)
        
        # configure scrollbar
        self.tree_scroll.config(command=self.tree.yview)        
        
        # build     s the treeview
        self.tree['columns'] = ('flight_id', 'f_name', 'l_name', 'airline', 'flight_num', 'depart_code', 
                                'dest_code', 'depart_date', 'depart_time', 'reserved_seats', 'total_cost')
        
        self.tree.column('#0', width=0, stretch=tk.YES)
        self.tree.column('flight_id', anchor=tk.CENTER, width=0)
        self.tree.column('f_name', anchor=tk.CENTER, width=100)
        self.tree.column('l_name', anchor=tk.CENTER, width=100)
        self.tree.column('airline', anchor=tk.CENTER, width=140)
        self.tree.column('flight_num', anchor=tk.CENTER, width=100)
        self.tree.column('depart_code', anchor=tk.CENTER, width=100)
        self.tree.column('dest_code', anchor=tk.CENTER, width=100)
        self.tree.column('depart_date', anchor=tk.CENTER, width=100)
        self.tree.column('depart_time', anchor=tk.CENTER, width=100)
        self.tree.column('reserved_seats', anchor=tk.CENTER, width=110)
        self.tree.column('total_cost', anchor=tk.CENTER, width=110)
        
        self.tree.heading('#0', text='', anchor=tk.CENTER)
        self.tree.heading('flight_id', text='Flight ID', anchor=tk.CENTER)
        self.tree.heading('f_name', text=' First\nName', anchor=tk.CENTER)
        self.tree.heading('l_name', text=' Last\nName', anchor=tk.CENTER)
        self.tree.heading('airline', text='\nAirline', anchor=tk.CENTER )
        self.tree.heading('flight_num', text='  Flight\nNumber', anchor=tk.CENTER )
        self.tree.heading('depart_code', text='Departure\n    Code', anchor=tk.CENTER )
        self.tree.heading('dest_code', text='Destination\n     Code', anchor=tk.CENTER)      
        self.tree.heading('depart_date', text='Departure\n    Date', anchor=tk.CENTER )
        self.tree.heading('depart_time', text='Departure\n    Time', anchor=tk.CENTER )
        self.tree.heading('reserved_seats', text='Reserved\n   Seats', anchor=tk.CENTER )
        self.tree.heading('total_cost', text='Total\nCost', anchor=tk.CENTER)
      
        self.reservation = self.controller.res.get_res_db(self.controller.user.username)
        # tags for alternating row colors
        self.tree.tag_configure('oddrow', background='lightsteelblue1')
        self.tree.tag_configure('evenrow', background='gray93')
        #iterate of the reservations to fill the treeview
        for index, value in enumerate(self.reservation):
            if index % 2 == 0:
                self.tree.insert(parent='', index=index, iid=index, text='', 
                    values=(value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7], value[8], value[9], value[10]), tags=('evenrow', ))
            else:
                self.tree.insert(parent='', index=index, iid=index, text='', 
                    values=(value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7], value[8], value[9], value[10]), tags=('oddrow', ))
                
        self.tree['displaycolumns'] = ['f_name', 'l_name', 'airline', 'flight_num',
                                       'depart_code', 'dest_code', 'depart_date',
                                       'depart_time', 'reserved_seats', 'total_cost']     
        self.tree.grid(row=0, column=0, sticky='EW', padx=10, pady=10)
        
        
    def cancel_flight(self):
        cancel = messagebox.askyesno('Cancel', 'Are you sure you want to cancel your flight?')
        if cancel == False:
            pass
        else:
            flight_id = self.tree.item(self.tree.selection()[0])['values'][0]
            seats_reserved = self.tree.item(self.tree.selection()[0])['values'][9]
            username = self.controller.user.username           
            self.controller.res.delete_res(flight_id, username, seats_reserved)
            messagebox.showinfo('Cancelled', 'Your reservation has been cancelled.')
            self.build_tree()          
