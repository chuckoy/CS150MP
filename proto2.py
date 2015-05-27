import Tkinter
import sys
from Tkinter import *
from ScrolledText import *
import tkFileDialog
import tkMessageBox
import os

class MenuBar(Tkinter.Menu):
    def __init__(self, parent,textPad):
        Tkinter.Menu.__init__(self, parent)
        self.textPad=textPad
        self.file= ""
        fileMenu = Tkinter.Menu(self, tearoff=False)
        self.add_cascade(label="File",underline=0, menu=fileMenu)
        fileMenu.add_command(label="New File", underline=0, command=self.new_command)        
        fileMenu.add_command(label="Open File", underline=0, command=self.open_command)
        fileMenu.add_command(label="Save", underline=0,command=self.save_command)
        fileMenu.add_command(label="Save As", underline=5,command=self.saveas_command)          
        fileMenu.add_command(label="Exit", underline=0, command=self.quit)
        self.add_command(label="Run", underline=0, command=self.quit)

    def new_command(self):
        if len(str(self.textPad.get(1.0, END)))>1:
            answer=tkMessageBox.askyesno('Save File!','Do you want to save file?')
            if answer == True:
                self.save_command()
        self.textPad.delete('1.0', END)
        self.file=""
    
    def open_command(self):
        self.file = tkFileDialog.askopenfile(parent=self,mode='rb',title='Select a file')
        if self.file != None:
            #print "fucker"
            contents = self.file.read()
            self.textPad.insert('1.0',contents)
            #print contents
            self.file.close()

    def saveas_command(self):
        self.file = tkFileDialog.asksaveasfile(mode='w', defaultextension=".txt")
        if self.file is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        save_file = str(self.textPad.get(1.0, END)) # starts from `1.0`, not `0.0`
        self.file.write(save_file)
        self.file.close()

    def save_command(self):
        if self.file == "":
            self.saveas_command()
        else:
            g = str(self.file).split(" ")
            h = g[2].split("\'")
            filename =  h[1]

            file = open(filename, 'w')
            save_file = str(self.textPad.get(1.0, END))
            file.write(save_file)
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