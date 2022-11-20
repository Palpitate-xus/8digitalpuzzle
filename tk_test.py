import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import traceback
import time

current_date = time.strftime("%Y-%m-%d", time.localtime())

mainWindow = tk.Tk()
mainWindow.title("8 digital puzzle")
mainWindow.withdraw()
mainWindow.update()
winWidth = 400
winHeight = 400
screenWidth = mainWindow.winfo_screenwidth()
screenHeight = mainWindow.winfo_screenheight()
x = int((screenWidth - winWidth) / 2)
y = int((screenHeight - winHeight) / 2)
mainWindow.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
mainWindow.deiconify()

block0 = tk.Button(mainWindow,text="0", font=20, width=10, height=4)
block0.place(x=25, y=25)
block1 = tk.Button(mainWindow,text="1", font=20, width=10, height=4)
block1.place(x=150, y=25)
block2 = tk.Button(mainWindow,text="2", font=20, width=10, height=4)
block2.place(x=275, y=25)
block3 = tk.Button(mainWindow,text="3", font=20, width=10, height=4)
block3.place(x=25, y=150)
block4 = tk.Button(mainWindow,text="4", font=20, width=10, height=4)
block4.place(x=150, y=150)
block5 = tk.Button(mainWindow,text="5", font=20, width=10, height=4)
block5.place(x=275, y=150)
block6 = tk.Button(mainWindow,text="6", font=20, width=10, height=4)
block6.place(x=25, y=275)
block7 = tk.Button(mainWindow,text="7", font=20, width=10, height=4)
block7.place(x=150, y=275)
block8 = tk.Button(mainWindow,text="8", font=20, width=10, height=4)
block8.place(x=275, y=275)

mainWindow.mainloop()