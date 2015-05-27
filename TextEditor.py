from Tkinter import *
#standard

class textEditor:	
	def __init__(self, master):#master=root or main window
		# **** Main Menu *****
		menu =  Menu(master)

		root.config(menu=menu)#configure menu

		subMenu = Menu(menu)#submenu.. what appears after clicking file
		menu.add_cascade(label="file",menu=subMenu)#add drop drown ... file button, drop down is subMenu
		subMenu.add_command(label="New Project...",command=self.doNothing)
		subMenu.add_command(label="New...",command=self.doNothing)
		subMenu.add_separator() #create line to separate one group of item from another
		subMenu.add_command(label="Exit",command=self.doNothing)

		editMenu = Menu(menu)
		menu.add_cascade(label="Edit", menu=editMenu)
		editMenu.add_command(label="Redo",command=self.doNothing)

		# ***** The Toolbar ****

		toolbar = Frame(root,bg="blue")

		insertButt = Button(toolbar,text="Insert Image",command=self.doNothing)
		insertButt.pack(side=LEFT,padx=2, pady=2)

		printButt = Button(toolbar,text="Print",command=self.doNothing)
		printButt.pack(side=LEFT,padx=2, pady=2)

		toolbar.pack(side=TOP, fill=X)

		# **** Status Bar *****
		status = Label(root,text="Preparing to do nothing...", bd=1, relief=SUNKEN, anchor=W)#bd->boarder, relief->how o you want this item to appear
		status.pack(side=BOTTOM,fill=X)
	def doNothing():
		print "ok ok ok I won't"

	def printMessage(self):
		print "Wow, this actually worked!"

root = Tk()
t = textEditor(root)
root.mainloop()
