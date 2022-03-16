import tkinter as tk
from tkinter import ttk

from src.frames.home import Home
from src.frames.register import Register
from src.frames.login import Login
from src.frames.search import SearchFlights
from src.frames.avail_flights import AvailFlights
from src.frames.show_res import ShowRes
from src.frames.update_user import UpdateUser

from src.classes.user import User
from src.classes.search import Search
from src.classes.reservation import Reservation
from src.classes.flight import Flight

tree_heading_back = 'steel blue3'
tree_heading_fore = 'gray86'
button_pressed_back = 'steel blue4'
button_active_back = 'steel blue1'
button_pressed_fore = 'white'
background = 'gray93'
text = 'gray21'
button_back = 'light sky blue1'


class AirlineReservation(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        global user
        self.user = User()
        global search
        self.search = Search()
        global res 
        self.res = Reservation()
        global flight 
        self.flight = Flight()
        
        self.title('Airline Reservations')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TFrame', 
                        background=background,
                        )
        style.configure('TLabel', 
                        background=background,
                        font=('Calibri', 18),
                        foreground=text, 
                        )
        style.configure('TButton',
                        foreground=text,
                        background=button_back,
                        font=('Calibri', 16),
                        )
        style.configure('Header.TLabel', 
                        font=('Calibri bold', 32),
                        foreground=text,
                        )
        style.configure('TEntry', 
                        foreground=text,
                        )
        style.configure('Treeview.Heading', 
                        font=('Calibri', 16), 
                        background=tree_heading_back,    
                        foreground=text, 
                        padding='0 10 0 30',
                        borderwidth=1,
                        )        
        style.configure('Treeview', 
                             font=('Calibri', 16), 
                             rowheight=40,
                             fieldbackground= background,
                             foreground=text,
                             )
        style.map('CustomButton.TButton',
                    foreground=[('pressed', button_pressed_fore)],
                    background=[('pressed', button_pressed_back), 
                                ('active', button_active_back),
                                ('focus', button_active_back)],
                )
        
        self['background'] = 'light gray'
        
        container = ttk.Frame(self)
        container.grid()
        container.columnconfigure(0, weight=1)
        
        self.frames = {}
        
        """Raise Frames Section"""
        home_frame = Home(container, self, 
                          lambda: self.show_frame(Register), 
                          lambda: self.show_frame(Login), 
                          lambda: self.show_frame(SearchFlights),
                          lambda: self.show_frame(ShowRes),
                          lambda: self.show_frame(UpdateUser),
                        )
        home_frame.grid(row=0, column=0, sticky='NSEW')
        
        register_frame = Register(container, self, 
                                  lambda: self.show_frame(Home), 
                                  lambda: self.show_frame(Login),
                                  lambda: self.show_frame(UpdateUser),
                                )
        register_frame.grid(row=0, column=0, sticky='NSEW')
        
        login_frame = Login(container, self, 
                            lambda: self.show_frame(Home), 
                            lambda: self.show_frame(Register),
                            lambda: self.show_frame(Login)
                            )
        login_frame.grid(row=0, column=0, sticky='NSEW')
         
        search_frame = SearchFlights(container, self, 
                              lambda: self.show_frame(Home), 
                              lambda: self.show_frame(Login),
                              lambda: self.show_frame(AvailFlights),
                              lambda: self.show_frame(SearchFlights),
                            )
        search_frame.grid(row=0, column=0, sticky='NSEW')
        
        avail_flights_frame = AvailFlights(container,self,
                                    lambda: self.show_frame(Home),
                                    lambda: self.show_frame(SearchFlights),
                                    lambda: self.show_frame(ShowRes),
                                )
        avail_flights_frame.grid(row=0, column=0, sticky='NSEW')
        
        show_res_frame = ShowRes(container,self,
                                 lambda: self.show_frame(Home),
                                 lambda: self.show_frame(SearchFlights),
                                 lambda: self.show_frame(Login), 
                                 )
        show_res_frame.grid(row=0, column=0, sticky='NSEW')
        
        update_user_frame = UpdateUser(container,self,
                                       lambda: self.show_frame(Home),
                                       lambda: self.show_frame(Login),
                                       )
        update_user_frame.grid(row=0, column=0, sticky='NSEW')
        
        self.frames[Home] = home_frame
        self.frames[Register] = register_frame
        self.frames[Login] = login_frame
        self.frames[SearchFlights] = search_frame
        self.frames[AvailFlights] = avail_flights_frame
        self.frames[ShowRes] = show_res_frame
        self.frames[UpdateUser] = update_user_frame
        
        self.show_frame(Home)

        
    def show_frame(self, container):
        frame = self.frames[container]
        # set specific frame geometry for specific frames
        # postupdate() calls focus() in individual frames
        if frame == self.frames[Home]:
            self.geometry('400x400')
            frame.tkraise()
            frame.postupdate()
        elif frame == self.frames[Login]:
            self.geometry('440x400')
            frame.tkraise()
            frame.postupdate()
        elif frame == self.frames[Register]:
            self.geometry('410x480')
            frame.tkraise()
            frame.postupdate()
        elif frame == self.frames[SearchFlights]:
            self.geometry('440x450')
            frame.tkraise()
            frame.postupdate()
        elif frame == self.frames[AvailFlights]:
            self.geometry('1020x700')
            frame.tkraise()
            frame.postupdate()
        elif frame == self.frames[ShowRes]:
            self.geometry('1200x700')
            frame.tkraise()
            frame.postupdate()
        elif frame == self.frames[UpdateUser]:
            self.geometry('410x480')
            frame.tkraise()
            frame.postupdate()
        else:
            pass

        
app = AirlineReservation()
app.mainloop()