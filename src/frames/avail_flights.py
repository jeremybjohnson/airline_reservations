import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from src.classes.reservation import Reservation


class AvailFlights(tk.Frame):
    def __init__(self, parent, controller, show_home, show_search, show_res):
        super().__init__(parent)
        
        self.controller = controller
        self.show_home = show_home
        self.show_search = show_search
        self.show_res = show_res
        
        """Header Section"""
        header_container = ttk.Frame(self, height=50)
        header_container.grid(row=0, column=0, padx=15, pady=10, sticky='NSEW')
        header_container.columnconfigure(0, weight=1)
        
        header_label = ttk.Label(
            header_container,
            text='Available Flights',
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
            command=self.home,
            width=15,
            style='CustomButton.TButton',
        )
        self.home_button.grid(row=0, column=0, padx=10, pady=10, sticky='W')
        self.home_button.bind('<Return>', self.home_handler)
                
        self.reserve_button = ttk.Button(
            button_container,
            text='Reserve Flight',
            command=self.reserve_flight,
            width=15,
            style='CustomButton.TButton',
        )
        self.reserve_button.grid(row=0, column=1, padx=10, pady=10, sticky='W')
        self.reserve_button.bind('<Return>', self.reserve_handler)
        self.reserve_button.bind('<Tab>', self.tab_order)
        
        self.search_button = ttk.Button(
            button_container,
            text='Search Flights',
            command=self.search,
            width=15,
            style='CustomButton.TButton',
        )
        self.search_button.grid(row=0, column=2, padx=10, pady=10, sticky='W')
        self.search_button.bind('<Return>', self.search_handler)
        self.search_button.bind('<Tab>', self.tab_order_rev)
    
    
    def postupdate(self):
        self.reserve_button.focus()
        self.build_tree()
        
        
    def home_handler(self, event):
        self.show_home()
        
        
    def search_handler(self, event):
        self.show_search()
        
        
    def reserve_handler(self, event):
        self.reserve_flight()
        
        
    def tab_order(self, event):
        widget = [self.reserve_button, self.home_button, self.search_button]
        for w in widget:
            w.lift()
        
        
    def tab_order_rev(self, event):
        widget = [self.search_button, self.home_button, self.reserve_button]
        for w in widget:
            w.lift()
        
        
    def build_tree(self):
        # Treeview scrollbar
        self.tree_scroll = ttk.Scrollbar(self.tree_container)
        self.tree_scroll.grid(row=0, column=1, sticky='NS')
        
        self.tree = ttk.Treeview(self.tree_container, yscrollcommand=self.tree_scroll.set)
        
        # configure scrolllbar
        self.tree_scroll.config(command=self.tree.yview) 
        
        self.tree['columns'] = ('flight_id', 'airline', 'flight_number', 
                                'depart_code', 'dest_code', 'depart_date', 
                                'depart_time','cost', 'avail_seats')

        
        self.tree.column('#0', width=0, stretch=tk.YES)
        self.tree.column('flight_id', anchor=tk.CENTER, width=20)
        self.tree.column('airline', anchor=tk.CENTER, width=140)
        self.tree.column('flight_number', anchor=tk.CENTER, width=100)
        self.tree.column('depart_code', anchor=tk.CENTER, width=120)
        self.tree.column('dest_code', anchor=tk.CENTER, width=120)
        self.tree.column('depart_date', anchor=tk.CENTER, width=120)
        self.tree.column('depart_time', anchor=tk.CENTER, width=120)
        self.tree.column('cost', anchor=tk.CENTER, width=100)
        self.tree.column('avail_seats', anchor=tk.CENTER, width=130)
        
        self.tree.heading('#0', text='', anchor=tk.CENTER)
        self.tree.heading('flight_id', text='Flight ID', anchor=tk.CENTER)
        self.tree.heading('airline', text='\nAirline', anchor=tk.CENTER )
        self.tree.heading('flight_number', text='  Flight\nNumber', anchor=tk.CENTER )
        self.tree.heading('depart_code', text='Departure\n    Code', anchor=tk.CENTER )
        self.tree.heading('dest_code', text='Destination\n     Code', anchor=tk.CENTER)      
        self.tree.heading('depart_date', text='Departure\n    Date', anchor=tk.CENTER )
        self.tree.heading('depart_time', text='Departure\n    Time', anchor=tk.CENTER )
        self.tree.heading('cost', text='\nCost', anchor=tk.CENTER )
        self.tree.heading('avail_seats', text='Available\n    Seats', anchor=tk.CENTER)
        
        flights = self.controller.flight.avail_flights
        
        # tags for alternating row colors
        self.tree.tag_configure('oddrow', background='lightsteelblue1')
        self.tree.tag_configure('evenrow', background='gray93')
        
        for index, value in enumerate(flights):
            if index % 2 == 0:
                self.tree.insert(parent='', index=index, iid=index, text='', 
                    values=(value[0], value[1], value[2], value[3], value[4], 
                            value[5], value[6], value[7], value[8]), tags=('evenrow', ))
            else:
                self.tree.insert(parent='', index=index, iid=index, text='', 
                    values=(value[0], value[1], value[2], value[3], value[4], 
                            value[5], value[6], value[7], value[8]), tags=('oddrow', ))
        # display columns so Flight ID isn't displayed
        self.tree['displaycolumns'] = ['airline', 'flight_number', 
                                    'depart_code', 'dest_code', 'depart_date', 
                                    'depart_time','cost', 'avail_seats']     
        self.tree.grid(row=0, column=0, sticky='NSEW', padx=10, pady=10)
    
    
    def home(self):
        self.controller.flight.avail_flights = []
        self.build_tree()
        self.show_home()
        
        
    def search(self):
        self.controller.flight.avail_flights = []
        self.build_tree()
        self.show_search()

    
    def reserve_flight(self):
        try:
            flight_id = self.tree.item(self.tree.selection()[0])['values'][0]
            username = self.controller.user.username
            seats_requested = self.controller.search.seats_requested
            if self.controller.res.set_res(flight_id, username, seats_requested) == False:
                messagebox.showerror(f'Database Error', 'You already have a reservation for that flight. \nYou have to cancel your reservation and book a new one')
            else:
                self.controller.res.set_res(flight_id, username, seats_requested)
                self.controller.res.set_res_db()
                messagebox.showinfo("Reservation", 'Your reservation has been created')
                self.show_res()
        except IndexError:
            messagebox.showerror(f'No Flight Selected', 'You must select a flight')
                
    
