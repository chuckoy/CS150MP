import Tkinter
import sys
from Tkinter import *
from ScrolledText import *
import tkFileDialog
import tkMessageBox

class MenuBar(Tkinter.Menu):
    def __init__(self, parent,textPad):
        Tkinter.Menu.__init__(self, parent)
        self.textPad=textPad
        fileMenu = Tkinter.Menu(self, tearoff=False)
        self.add_cascade(label="File",underline=0, menu=fileMenu)
        fileMenu.add_command(label="New File", underline=0, command=self.quit)        
        fileMenu.add_command(label="Open File", underline=0, command=self.open_command)
        fileMenu.add_command(label="Save", underline=0,command=self.quit)
        fileMenu.add_command(label="Save As", underline=5,command=self.quit)          
        fileMenu.add_command(label="Exit", underline=0, command=self.quit)
        self.add_command(label="Run", underline=0, command=self.quit)

    def open_command(self):
        file = tkFileDialog.askopenfile(parent=self,mode='rb',title='Select a file')
        if file != None:
            #print "fucker"
            contents = file.read()
            self.textPad.insert('1.0',contents)
            #print contents
            file.close()
        

    def quit(self):
        sys.exit(0)
    
class App(Tkinter.Tk):
    def __init__(self):
        Tkinter.Tk.__init__(self)
        textPad=ScrolledText(master=self,wrap='word',width=120,height=20)
        interpreter=ScrolledText(master=self,wrap='word',width=120,height=20)
        menubar = MenuBar(self,textPad)
        
        self.config(menu=menubar)
        #textPad.grid(row=0,column=0)
        #interpreter.grid(row=1,column=0)
        textPad.pack(fill='both',expand=True,padx=3,pady=3)
        interpreter.pack(fill='both',expand=True,padx=3,pady=3)
if __name__ == "__main__":
    app = App()
    app.title('Tanders Programming Language') 
    app.geometry("900x900")
    app.mainloop()