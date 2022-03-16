import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from src.classes.user import User


class Login(tk.Frame):
    def __init__(self, parent, controller, show_home, show_register, show_login):
        super().__init__(parent)        
        
        self.controller = controller
        self.show_home = show_home
        self.show_register = show_register
        self.show_login = show_login
        
        self.username= tk.StringVar()
        self.password= tk.StringVar()
        
        """Header Section"""
        
        self.header_container = ttk.Frame(self, height=80)
        self.header_container.grid(row=0, column=0, padx=10, pady=10, sticky='NSEW')
        self.header_container.columnconfigure(0, weight=1)
        
        self.header_label = ttk.Label(
            self.header_container,
            text='Login',
            style='Header.TLabel'
        )
        self.header_label.place(relx=0.5, rely=0.5, anchor='center')
        
        """Entry Section"""
        
        self.entry_container = ttk.Frame(self, height=40)
        self.entry_container.grid(row=1, column=0, padx=10, pady=10, sticky='NSEW')
        self.entry_container.columnconfigure(0, weight=1)
        
        self.username_label = ttk.Label(
            self.entry_container,
            text='Username',
        )
        self.username_label.grid(row=0, column=0, padx=10, pady=10, sticky='W')
        
        self.username_entry = ttk.Entry(
            self.entry_container,
            textvariable=self.username,
            font=('Calibri', 16),
        )
        self.username_entry.grid(row=0, column=1, padx=10, pady=10, sticky='W')
        self.username_entry.bind('<Tab>', self.tab_order)
        
        self.password_label = ttk.Label(
            self.entry_container,
            text='Password',
        )
        self.password_label.grid(row=1, column=0, padx=10, pady=10, sticky='W')
        
        self.password_entry = ttk.Entry(
            self.entry_container,
            textvariable=self.password,
            show='*',
            font=('Calibri', 16),
        )
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky='W')
        
        """Button Section"""
                
        self.login_button = ttk.Button(
            self.entry_container,
            text='Login',
            command=self.login_user,
            width=15,
            style='CustomButton.TButton'
        )
        self.login_button.grid(row=2, column=0, padx=10, pady=20, sticky='W')
        self.login_button.bind('<Return>', self.login_handler)
        
        self.home_button = ttk.Button(
            self.entry_container,
            text='Home',
            command=show_home,
            width=15,
            style='CustomButton.TButton'
        )
        self.home_button.grid(row=2, column=1, padx=10, pady=20, sticky='E')
        self.home_button.bind('<Return>', self.home_handler)
                
        self.register_button = ttk.Button(
            self.entry_container,
            text='Register',
            command=show_register,
            width=15,
            style='CustomButton.TButton'
        )
        self.register_button.grid(row=3, column=0, padx=10, pady=12, sticky='W')
        self.register_button.bind('<Return>', self.register_handler)
        
        self.logout_button = ttk.Button(
            self.entry_container,
            text='Log Out',
            command=self.logout_user,
            width=15,
            style='CustomButton.TButton'
        )
        self.logout_button.grid(row=3, column=1, padx=10, pady=12, sticky='E')
        self.logout_button.bind('<Return>', self.logout_handler)
        self.logout_button.bind('<Tab>', self.tab_order_rev)
        
    def postupdate(self):
        self.username_entry.focus()

    
    def login_handler(self, event):
        self.login_user()
        
        
    def logout_handler(self, event):
        self.logout_user()
    
    
    def register_handler(self, event):
        self.show_register()
        
        
    def home_handler(self, event):
        self.show_home()
        
    
    def tab_order(self, event):
        widgets = [self.username_entry, self.password_entry, self.login_button, self.home_button,
                   self.register_button, self.logout_button
                   ]
        for w in widgets:
            w.lift()
    
      
    def tab_order_rev(self, event): 
        widgets = [self.logout_button, self.register_button, self.home_button, 
                   self.login_button, self.password_entry, self.username_entry
                   ]
        for w in widgets:
            w.lift()        
            
    
    def login_user(self):
        verify_data = self.verify_entry()
        if verify_data:
            user_login = self.controller.user.login(
                self.username_entry.get(), 
                self.password_entry.get()
            )
            if user_login:
                messagebox.showinfo('Logged In', 'You are logged in.')
                self.clear_text()
                self.show_home()
            else:
                messagebox.showerror('No Match','Username and Password do not match.')
        
    def verify_entry(self):
        if (
            self.username.get() == '' or
            self.password.get() == ''
        ):
            messagebox.showerror('Field Error', 'All Fields Are Required')
        else:
            return True
    
    
    def clear_text(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        
    
    def logout_user(self):
        if self.controller.user.username != '':
            self.controller.user.logout(
                self.controller.search,
                self.controller.res,
                self.controller.flight,
            )
            messagebox.showinfo('Logged Out', 'You have been logged out.')
            self.show_home()
        else:
            messagebox.showerror('Not Logged In', 'No one is logged in.')