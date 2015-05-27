import Tkinter
import sys

class MenuBar(Tkinter.Menu):
    def __init__(self, parent):
        Tkinter.Menu.__init__(self, parent)
        fileMenu = Tkinter.Menu(self, tearoff=False)
        self.add_cascade(label="File",underline=0, menu=fileMenu)
        fileMenu.add_command(label="New File", underline=0, command=self.quit)        
        fileMenu.add_command(label="Open File", underline=0, command=self.quit)
        fileMenu.add_command(label="Save", underline=0,command=self.quit)
        fileMenu.add_command(label="Save As", underline=5,command=self.quit)          
        fileMenu.add_command(label="Exit", underline=0, command=self.quit)
        self.add_command(label="Run", underline=0, command=self.quit)
    def quit(self):
        sys.exit(0)

class App(Tkinter.Tk):
    def __init__(self):
        Tkinter.Tk.__init__(self)
        menubar = MenuBar(self)
        self.config(menu=menubar)

if __name__ == "__main__":
    app = App()
    app.title('Tanders Programming Language') 
    app.geometry("900x900")
    app.mainloop()