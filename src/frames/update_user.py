import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from src.classes.user import User


class UpdateUser(tk.Frame):
    def __init__(self, parent, controller, show_home, show_login): 
        super().__init__(parent)
        
        style = ttk.Style()
        style.theme_use('clam')

        self.show_home = show_home
        self.show_login = show_login
        self.controller = controller
        
        self.password = tk.StringVar()
        self.verify_password = tk.StringVar()
        self.f_name = tk.StringVar()
        self.l_name = tk.StringVar()
        self.verify_pass = tk.StringVar()
        
        """Header"""
        self.header_container = ttk.Frame(self, height=80)
        self.header_container.grid(row=0, column=0, padx=10, pady=10, sticky='NSWE')
        self.header_container.columnconfigure(0, weight=1)
        
        self.header_label = ttk.Label(
            self.header_container,
            text='Update User',
            style='Header.TLabel'
        )
        self.header_label.place(relx=0.5, rely=0.5, anchor='center')
        
        """Text entry section"""
        self.entry_container = ttk.Frame(self, height=80)
        self.entry_container.grid(row=1, column=0, columnspan=2, padx=10, pady=(20, 40), sticky='NSWE')
        self.entry_container.columnconfigure(0, weight=1)
        
        self.password_label = ttk.Label(
            self.entry_container,
            text='Password'
        )
        self.password_label.grid(row=0, column=0, padx=10, pady=10, sticky='W')
        
        self.password_entry = ttk.Entry(
            self.entry_container,
            textvariable=self.password,
            show='*',
            font=('Calibri', 16),
        )
        self.password_entry.grid(row=0, column=1, padx=10, pady=10)
        self.password_entry.bind('<Tab>', self.tab_order)
        
        self.verify_password_label = ttk.Label(
            self.entry_container,
            text='Verify Password',
        )
        self.verify_password_label.grid(row=1, column=0, padx=10, pady=10, sticky='W')
        
        self.verify_password_entry = ttk.Entry(
            self.entry_container,
            textvariable=self.verify_password,
            show='*',
            font=('Calibri', 16),
        )
        self.verify_password_entry.grid(row=1, column=1, padx=10, pady=10)
               
        self.f_name_label = ttk.Label(
            self.entry_container,
            text='First Name',
        )
        self.f_name_label.grid(row=2, column=0, padx=10, pady=10, sticky='W')
        
        self.f_name_entry = ttk.Entry(
            self.entry_container,
            textvariable=self.f_name,
            font=('Calibri', 16),
        )
        self.f_name_entry.grid(row=2, column=1, padx=10, pady=10)
               
        self.l_name_label = ttk.Label(
            self.entry_container,
            text='Last Name',
        )
        self.l_name_label.grid(row=3, column=0, padx=10, pady=10, sticky='W')
        
        self.l_name_entry = ttk.Entry(
            self.entry_container,
            textvariable=self.l_name,
            font=('Calibri', 16),
        )
        self.l_name_entry.grid(row=3, column=1, padx=10, pady=10)
               
               
        """Buttons Section"""
        
        self.home_button = ttk.Button(
            self.entry_container,
            text='Home',
            command=show_home,
            style='CustomButton.TButton',
        )
        self.home_button.grid(row=4, column=0, padx=10, pady=30, sticky='W')
        self.home_button.bind('<Return>', self.home_handler)
        
        self.login_button = ttk.Button(
            self.entry_container,
            text='Login',
            command=show_login,
            style='CustomButton.TButton',
        )
        self.login_button.grid(row=4, column=1, padx=10, pady=10, sticky='E')
        self.login_button.bind('<Return>', self.login_handler)
        
        self.update_button = ttk.Button(
            self.entry_container,
            text='Update User',
            command=self.update_user,
            style='CustomButton.TButton',
        )
        self.update_button.grid(row=6, column=0, padx=10, pady=10, sticky='W')
        self.update_button.bind('<Return>', self.update_handler)
        
        self.delete_button = ttk.Button(
            self.entry_container,
            text='Delete User',
            command=self.delete_user,
            style='CustomButton.TButton',
        )
        self.delete_button.grid(row=6, column=1, padx=10, pady=10, sticky='E')
        self.delete_button.bind('<Return>', self.delete_handler)
        self.delete_button.bind('<Tab>', self.tab_order_rev)


    
    def postupdate(self):
        self.password_entry.focus()
    
    
    def update_handler(self, event):
        self.update_user()
        
        
    def home_handler(self, event):
        self.show_home()
        
        
    def login_handler(self, event):
        self.show_login()
        
        
    def delete_handler(self, event):
        self.delete_user()
        
        
    def tab_order(self, event):
        widgets = [self.password_entry, self.verify_password_entry,
                   self.f_name_entry, self.l_name_entry, self.home_button,
                   self.login_button, self.update_button, self.delete_button
                ]
        for w in widgets:
            w.lift()
            
            
    def tab_order_rev(self, event):
        widgets = [self.delete_button, self.update_button, self.login_button, 
                   self.home_button, self.l_name_entry, self.f_name_entry, 
                   self.verify_password_entry, self.password_entry
                   ]
        for w in widgets:
            w.lift()
        
    
    def update_user(self):
        self.verify_pass = self.verify_pass_match()
        self.verify_input = self.verify_entry()
        if self.verify_input:
            if self.verify_pass:
                if self.controller.user.username == '':
                    messagebox.showerror('Not Logged In', 'You must be logged in to update your account')
                    self. show_login()
                else:
                    cancel = messagebox.askyesno('Update', 'Are you sure you want to update your account?')
                    if cancel == False:
                        pass
                    else:
                        update = self.controller.user.update_user(
                                self.controller.user.username,
                                self.password_entry.get(),
                                self.f_name_entry.get(),
                                self.l_name_entry.get()
                                )
                        if update == False:
                            messagebox.showinfo('DB Problem', 'There was a problem updating the database')
                        else:
                            messagebox.showinfo('Updated', 'Your data has been updated.')
                            self.clear_text()
                            self.show_home()
            else:
                messagebox.showerror('Password Warning', 'Passwords do not match.')
        else:
            messagebox.showerror('Input Warning', 'All fields are required.')
        
        
    def verify_pass_match(self):
        if self.password.get() == self.verify_password.get():
            return True
        else:
            return False
        
        
    def verify_entry(self):
        if (
            self.password.get() == '' or
            self.verify_password.get() == '' or
            self.f_name.get() == '' or
            self.l_name.get() == ''
        ):
            return False
        else:
            return True
        
        
    def delete_user(self):
        logged_in = self.verify_login()
        if logged_in == False:
            messagebox.showerror('Not Logged In', 'You must be logged in to delete your account')
            self. show_login()
        else:
            cancel = messagebox.askyesno('Cancel', 'Are you sure you want to delete your account?\nAll reservations will be deleted.')
            if cancel == False:
                pass
            else:
                delete = self.controller.user.delete_user(self.controller.user.username)
                if delete == False:
                    messagebox.showinfo('DB Problem', 'There was a problem updating the database')
                else:
                    messagebox.showinfo('Deleted', 'We are sorry to see you go!\nYour account has been deleted.')
                    self.clear_text()
                    self.show_home()

        
    def clear_text(self):
        self.password_entry.delete(0, tk.END)
        self.verify_password_entry.delete(0, tk.END)
        self.f_name_entry.delete(0, tk.END)
        self.l_name_entry.delete(0, tk.END)
        
        
    def verify_login(self):
        if self.controller.user.username == '':
            return False
        else:
            return True