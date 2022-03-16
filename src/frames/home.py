import tkinter as tk
from tkinter import ttk


class Home(tk.Frame):
    def __init__(self, parent, controller, show_register, 
                 show_login, show_search, show_res, show_update):
        super().__init__(parent)
        
        self.controller = controller
        self.show_res = show_res
        self.show_register = show_register
        self.show_search = show_search
        self.show_login = show_login
        self.show_update = show_update
        
        """Header Section"""
        header_container = ttk.Frame(
            self, height=60,
        )
        header_container.grid(row=0, column=0, sticky='NSEW', padx=10, pady=20)
        header_container.columnconfigure(0, weight=1)
        
        header_label1 = ttk.Label(
            header_container,
            text='Airline Search',
        )
        header_label1.config(font=('Calibri bold', 52))
        header_label1.place(relx=0.5, rely=0.5, anchor='center')
        
        header_container2 = ttk.Frame(self, height=40)
        header_container2.grid(row=1, column=0, sticky='NSEW', padx=10)
        header_container2.columnconfigure(0, weight=1)
       
        header_label2 = ttk.Label(
            header_container2,
            text='Home',
            justify='center',
        )
        header_label2.config(font=('Calibri bold', 48))
        header_label2.place(relx=0.5, rely=0.5, anchor='center')
        
        """Button Section"""
        button_container = ttk.Frame(self, height=100)
        button_container.grid(row=2, column=0, sticky='NSEW', padx=(10, 10), pady=(80, 0))
        
        self.login_button = ttk.Button(
            button_container,
            text='Login',
            width=15,
            command=show_login,
            style = 'CustomButton.TButton',
        )
        self.login_button.grid(row=0, column=0, sticky='WS', padx=(10, 10), pady=10)
        self.login_button.bind('<Return>', self.login_handler)
        self.login_button.bind('<Tab>', self.tab_order)
        
        self.search_button = ttk.Button(
            button_container,
            text='Search Flights',
            width=15,
            command=show_search,
            style = 'CustomButton.TButton',
        )
        self.search_button.grid(row=0, column=1, sticky='E', padx=10, pady=10)
        self.search_button.bind('<Return>', self.search_handler)
        
        self.register_button = ttk.Button(
            button_container,
            text='Register',
            width=15,
            command=show_register,
            style = 'CustomButton.TButton',
        )
        self.register_button.grid(row=1, column=0, sticky='W', padx=10, pady=10)
        self.register_button.bind('<Return>', self.register_handler)
        
        self.res_button = ttk.Button(
            button_container,
            text='Show Reservations',
            width=15,
            command=self.show_res,
            style = 'CustomButton.TButton',
        )
        self.res_button.grid(row=1, column=1, sticky='E', padx=10, pady=10)
        self.res_button.bind('<Return>', self.res_handler)
        
        self.update_button = ttk.Button(
            button_container,
            text='Update User',
            width=15,
            command=self.show_update,
            style = 'CustomButton.TButton',
        )
        self.update_button.grid(row=2, column=0, sticky='W', padx=10, pady=10)
        self.update_button.bind('<Return>', self.update_handler)
        self.update_button.bind('<Return>', self.update_handler)

        
    def postupdate(self):
        self.login_button.focus()
        
           
    def login_handler(self, event):
        self.show_login()
        
        
    def search_handler(self, event):
        self.show_search()
        
        
    def register_handler(self, event):
        self.show_register()
        
        
    def res_handler(self, event):
        self.reserved_flights()
        
        
    def update_handler(self, event):
        self.show_update()
        
        
    
    def tab_order(self, event):
        widgets = [self.login_button, self.search_button, self.register_button, 
                   self.res_button, self.update_button
                   ]
        for w in widgets:
            w.lift()
    
        
    def tab_order_rev(self, event):
        widgets = [self.update_button, self.res_button, 
                   self.register_button, self.search_button, self.login_button
                   ]
        for w in widgets:
            w.lift()

        


