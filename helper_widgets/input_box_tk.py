from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.ttk import Progressbar
import time



class UserInput(Tk):

    """
    
        The UserInput class is a child of tkinter.Tk class of tkinter module and it handles user input
    
    """

    def __init__(self):
    
        """
            This function is a constructor that initialized the class UserInput with the necessary attributes
        """
    
        print("Instantiating User Input Reciever Class")
        super().__init__()
        self.configure(bg="aqua")
        self.target = None
        self.fun_2 = None
        self.resizable(False, False)
        
        Frame(self,width=400,height=150,bg="#249794").place(x=0,y=0)
        
        def search():
        
        
            """
            
                This function is a callback function that handles the click event of the search button
            
            """
        
            
            self.destroy()
        
        def cancel():
        
        
            """
            
                This function is a callback function that handles the click event of the cancel button
            
            """
        
            
            self.destroy()
            
            
        self.title('Algorithm ') 
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 400
        window_height = 150
        self.geometry(f'{window_width}x{window_height}+{int((screen_width-window_width)/2)}+{int((screen_height-window_height)/2)}')
        
        Frame(self,width=500,height=285,bg="#249794").place(x=0,y=0)
        
        Frame(self,width=330,height=25,bg="white").place(x=33,y=45)
        font=('Calibri (Body)',15,'bold')
        app_title = Label(self, text='Algorithm: BFS', font=font, bg="#249794")
        app_title.place(x=110, y=10)
        
        inputtxt = tk.Text(self,
                   height = 1,
                   width = 10)
        
        font=('Calibri (Body)',10,'bold')
        label1=Label(self,text="Enter the number to be searched: ", font=font, bg="white")
        label1.place(x=35, y=45)
        inputtxt.place(x=270, y=47)
        
        
        font=('Calibri (Body)',15,'bold')
        btn=Button(self, width=6,height=1, font=font, text='Search',border=0,fg='#249794',bg='white', command=search)
        btn.place(x=200, y=90)
        
        btn=Button(self, width=6,height=1, font=font, text='Cancel',border=0,fg='#249794',bg='white', command=cancel)
        btn.place(x=100, y=90)
        
        self.mainloop()
        
    
    def get_user_input(self):
        
        """
            
            This function or method returns the index of the two functions choosen by the user
        
        """
    
        return self.fun_1, self.fun_2

UserInput()