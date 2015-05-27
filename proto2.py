import Tkinter
import sys

class MenuBar(Tkinter.Menu):
    def __init__(self, parent):
        Tkinter.Menu.__init__(self, parent)

        fileMenu = Tkinter.Menu(self, tearoff=False)
        self.add_cascade(label="File",underline=0, menu=fileMenu)
        fileMenu.add_command(label="Exit", underline=1, command=self.quit)

    def quit(self):
        sys.exit(0)

class App(Tkinter.Tk):
    def __init__(self):
        Tkinter.Tk.__init__(self)
        menubar = MenuBar(self)
        self.config(menu=menubar)

if __name__ == "__main__":
    app=App()
    app.mainloop()