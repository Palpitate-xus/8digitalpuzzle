for i in range(9):
    print("block%s = tk.Button(mainWindow,text=\"%s\", font=20, width=10, height=4)"%(str(i), str(i)))
    print("block%s.place(x=25, y=25)"%str(i))
