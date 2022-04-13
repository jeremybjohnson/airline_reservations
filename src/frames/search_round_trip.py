import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import datetime

from src.classes.search import Search


class SearchReturnFlights(tk.Frame):
    def __init__(self, parent, controller, show_home, 
                 show_login, show_avail_flights):
        super().__init__(parent)
        
        self.controller = controller
        self.show_login = show_login
        self.show_avail_flights = show_avail_flights
        self.show_home = show_home
        
        self.depart_code = tk.StringVar()
        self.dest_code = tk.StringVar()
        self.depart_date = tk.StringVar() 
        self.return_date = tk.StringVar()
        self.seats_requested = tk.IntVar()
        
        """Header Section"""
        header_container = ttk.Frame(self, height=80)
        header_container.grid(row=0, column=0, padx=10, pady=10, sticky='NSEW')
        header_container.columnconfigure(0, weight=1)
        
        header_label = ttk.Label(
            header_container,
            text='Search Flights',
            style='Header.TLabel'
        )
        header_label.place(relx=0.5, rely=0.5, anchor='center')
        
        """Entry Section"""
        self.entry_container = ttk.Frame(self, height=40)
        self.entry_container.grid(row=1, column=0, padx=10, pady=10, sticky='NSEW')
        self.entry_container.columnconfigure(0, weight=1)
        
        self.depart_label = ttk.Label(
            self.entry_container,
            text='Departure Code',
        )
        self.depart_label.grid(row=0, column=0, padx=10, pady=10, sticky='W')
        
        self. depart_entry = ttk.Entry(
            self.entry_container,
            textvariable=self.depart_code,
            font=('Calibri', 16),
        )
        self.depart_entry.grid(row=0, column=1, padx=10, pady=10, sticky='W')
        self.depart_entry.bind('<Tab>', self.tab_order)
        
        self.dest_label = ttk.Label(
            self.entry_container,
            text='Destination Code',
        )
        self.dest_label.grid(row=1, column=0, padx=10, pady=10, sticky='W')
        
        self.dest_entry =ttk.Entry(
            self.entry_container,
            textvariable=self.dest_code,
            font=('Calibri', 16),
        )
        self.dest_entry.grid(row=1, column=1, padx=10, pady=10, sticky='W')
        
        self.date_label = ttk.Label(
            self.entry_container,
            text='Departure Date',
        )
        self.date_label.grid(row=2, column=0, padx=10, pady=10, sticky='W')

        self.date_entry=DateEntry(
            self.entry_container,
            selectmode='day',
            textvariable=self.depart_date
        )
        self.date_entry.grid(row=2,column=1, padx=10, pady=10, sticky='W')
        
        self.return_date_label = ttk.Label(
            self.entry_container,
            text='Return Date',
        )
        self.return_date_label.grid(row=3,column=0, padx=10, pady=10, sticky='W')
        
        self.return_date_entry = DateEntry(
            self.entry_container,
            selectmode='day',
            textvariable=self.return_date
        )
        self.return_date_entry.grid(row=3,column=1, padx=10, pady=10, sticky='W')
        
        self.seats_label = ttk.Label(
            self.entry_container,
            text='Seats Requested',
        )
        self.seats_label.grid(row=4, column=0, padx=10, pady=10, sticky='W')
        
        self.seats_entry =ttk.Entry(
            self.entry_container,
            textvariable=self.seats_requested,
            font=('Calibri', 16),
        )
        self.seats_entry.grid(row=4, column=1, padx=10, pady=10, sticky='W')
        
        """Buttons Section"""
                
        self.search_button = ttk.Button(
            self.entry_container,
            text='Search Flights',
            command=self.search_flights,
            width=15,
            style = 'CustomButton.TButton',
        )
        self.search_button.grid(row=5, column=0, padx=10, pady=20, sticky='W')
        self.search_button.bind('<Return>', self.search_handler)
        
        self.home_button = ttk.Button(
            self.entry_container,
            text='Home',
            command=show_home,
            width=15,
            style = 'CustomButton.TButton',
        )
        self.home_button.grid(row=5, column=1, padx=10, pady=20, sticky='E')
        self.home_button.bind('<Return>', self.home_handler)
        
        self.login_button = ttk.Button(
            self.entry_container,
            text='Login',
            command=show_login,
            width=15,
            style = 'CustomButton.TButton',
        )
        self.login_button.grid(row=6, column=0, padx=10, pady=10, sticky='W')
        self.login_button.bind('<Return>', self.login_handler)
        
        self.clear_button = ttk.Button(
            self.entry_container,
            text='Clear',
            command=self.clear_text,
            width=15,
            style = 'CustomButton.TButton',
        )
        self.clear_button.grid(row=6, column=1, padx=10, pady=10, sticky='E')
        self.clear_button.bind('<Return>', self.clear_handler)
        self.clear_button.bind('<Tab>', self.tab_order_rev)
        
    
    def postupdate(self):
        self.depart_entry.focus()
        
    
    def search_handler(self, event):
        self.search_flights()
        
        
    def home_handler(self, event):
        self.show_home()
        
        
    def login_handler(self, event):
        self.show_login()
        
        
    def clear_handler(self, event):
        self.clear_text()


    def tab_order_rev(self, event):
        widgets =[self.clear_button, self.login_button, self.home_button, 
                  self.search_button, self.seats_entry, self.return_date_entry, 
                  self.date_entry, self.dest_entry, self.depart_entry
                  ]
        for w in widgets:
            w.lift()
    
    
    def tab_order(self, event):
        widgets = [self.depart_entry, self.dest_entry, self.date_entry, 
                   self.return_date_entry, self.seats_entry, self.search_button, 
                   self.home_button, self.login_button, self.clear_button
                   ]
        for w in widgets:
            w.lift()
    
    
    def search_flights(self):
        self.logged_in = self.verify_login()
        if self.logged_in:
            self.controller.search.set_search(
                self.controller.user.username,
                (self.depart_entry.get()).upper(),
                (self.dest_entry.get()).upper(),
                self.depart_date.get(),  
                self.seats_requested.get(),
                self.return_date.get()
            )
            if (datetime.datetime.strptime(self.depart_date.get(), '%m/%d/%Y').date() < 
                datetime.date.today() or 
                datetime.datetime.strptime(self.return_date.get(), '%m/%d/%Y').date() < 
                datetime.date.today() or
                datetime.datetime.strptime(self.return_date.get(), '%m/%d/%Y').date() < 
                datetime.datetime.strptime(self.depart_date.get(), '%m/%d/%Y').date()):
                    messagebox.showerror('Invalid Date', 'Invalid Date or Dates')
            else:                   
                #set flights lists for outbound and return flights  
                self.controller.flight.avail_flights = self.controller.search.get_flights_db()
                self.controller.flight.return_flights = self.controller.search.get_return_flights_db()     
                #check to see if any flights are available
                if (self.controller.flight.avail_flights == False
                    or self.controller.flight.return_flights == False
                ):
                    messagebox.showerror('No Flights', 'No flights were found with your requirements.')
                else:
                    self.show_avail_flights()
        else:
            messagebox.showerror('Not Logged In', 'User is not logged in.')
            self.show_login()
            
    
    def verify_login(self):
        if self.controller.user.username == '':
            return False
        else:
            return True
    
    
    def clear_text(self):
        self.depart_entry.delete(0, tk.END)
        self.dest_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.return_date_entry.delete(0, tk.END)
        self.seats_entry.delete(0, tk.END)
        