import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        #setting title
        root.title("SearchBar")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLineEdit_144=tk.Entry(root)
        GLineEdit_144["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_144["font"] = ft
        GLineEdit_144["fg"] = "#333333"
        GLineEdit_144["justify"] = "center"
        GLineEdit_144["text"] = "Entry"
        GLineEdit_144.place(x=150,y=200,width=323,height=45)
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

