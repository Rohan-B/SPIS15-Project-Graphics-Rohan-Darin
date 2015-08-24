from stegdonebeta import*

import Tkinter as Tk

class App(object):
    def __init__(self):
        self.root = Tk.Tk()
        self.root.wm_title("Embed")
        self.label = Tk.Label(self.root, text="enter the name of ur picture")
        self.label.pack()

        self.picture1name = StringVar()
        Tk.Entry(self.root, textvariable=self.picture1name).pack()

        self.picture2name = StringVar()
        Tk.Entry(self.root, textvariable=self.picture2name).pack()

        self.buttontext = Tk.StringVar()
        self.buttontext.set("Embed")
        Tk.Button(self.root, textvariable=self.buttontext, command=embedD(self.picture1name,self.picture2name)).pack()
        
        
        self.label = Tk.Label(self.root, text="")
        self.label.pack()

        self.root.mainloop()

    def clicked1(self):
        weight_in_kg = self.weight_in_kg.get()
        self.label.configure(text=weight_in_kg)

    def button_click(self, e):
        pass

App()
