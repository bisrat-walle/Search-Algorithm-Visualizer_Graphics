from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
import time

class SplashUserInput(Tk):

    """
    
        The UserInput class is a child of tkinter.Tk class of tkinter module and it handles user input
    
    """

    def __init__(self):
    
        """
            This function is a constructor that initialized the class UserInput with the necessary attributes
        """
        print("Instantiating Algorithm Type Reciever Class")
        super().__init__()
        self.configure(bg="aqua")
        self.choosen = None
        self.resizable(False, False)
        self.visualize = False
        
        Frame(self,width=500,height=285,bg="#249794").place(x=0,y=0)
        
        def visualize():
        
        
            """
            
                This function is a callback function that handles the click event of the visualize button
            
            """
            label1 = Label(self, text="Loading ... ", fg="white", bg="#249794")
            label1.config(font=("Calibri (Body)", 10))
            label1.place(x=20, y=250)
            for i in range(100):
                self.progress.step(1)
                self.update_idletasks()
                time.sleep(0.015)
            self.choosen = algorithm.get()
            self.visualize = True
            self.destroy()
            
            
        self.title('Search Algorithm Visualizer') 
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 500
        window_height = 300
        self.geometry(f'{window_width}x{window_height}+{int((screen_width-window_width)/2)}+{int((screen_height-window_height)/2)}')
        
        Frame(self,width=500,height=285,bg="#249794").place(x=0,y=0)
        
        Frame(self,width=380,height=50,bg="white").place(x=65,y=110)
        font=('Calibri (Body)',15,'bold')
        app_title = Label(self, text='👋 Welocme to Search Algorithm Visualizer', font=font, bg="#249794")
        app_title.place(x=55, y=50)
        
        
        font=('Calibri (Body)',10,'bold')
        algorithm_type = ['Graph Search', 'Array Search']
        label1=Label(self,text="Choose the algorithm type", font=font, bg="white")
        label1.place(x=68, y=120)
        algorithm = ttk.Combobox(self,values=algorithm_type, state="readonly",
                         font = font)
        algorithm.place(x=268, y=120)
        algorithm.current(0)
        
        
        font=('Calibri (Body)',15,'bold')
        btn=Button(self, width=8,height=1, font=font, text='Visualize',border=0,fg='#249794',bg='white', command=visualize)
        btn.place(x=200, y=200)
        
        label=Label(self,text='Copyright © Visualizer Team 2022',fg='white',bg="#249794")
        font=('Calibri (Body)',10)
        label.config(font=font)
        label.place(x=290,y=255)
        
        style = ttk.Style()
        style.configure("aqua.Horizontal.TProgressbar", foreground='aqua', background='#4f4f4f')
        self.progress=Progressbar(self,style="aqua.Horizontal.TProgressbar",orient=HORIZONTAL,length=540,mode='determinate',)
        self.progress.place(x=-5, y=278)
        
        
        self.mainloop()
    
    def getInput(self):
        if self.visualize:
            return self.choosen
        return None