# GUI for PrainYuck
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import bfparser as bf


class Window(Frame):

    def __init__(self, master=Tk()):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

        # Set minimum size of window
        master.update()
        master.minsize(400, 400)

    # Creation of init_window
    def init_window(self):
        # Changing the title of our master widget
        self.master.title("Untitled - Prain Yuck")
        self.fname = self.master.title
        # Allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # Create text area
        self.textarea = Text(self.master)

        # Create menu bar
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # File menu
        filemenu = Menu(menu)
        menu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='New')
        filemenu.add_command(label='Open...', command=self.openFile)
        filemenu.add_command(label='Save')
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.master.quit)

        # Edit menu
        editmenu = Menu(menu)
        menu.add_cascade(label='Edit', menu=editmenu)
        editmenu.add_command(label="Cut", command=self.cut)
        editmenu.add_command(label="Copy", command=self.copy)
        editmenu.add_command(label="Paste", command=self.paste)

        # Execute button
        menu.add_command(Button(self.master, text="Exe", command=self.execute))

    def create_popup(self, mess, err=True):
        pop = self.master.Toplevel()
        pop_title = 'Error' if err else 'Warning'
        pop.title(pop_title)
        showinfo(pop_title, mess)
        # Close button
        b = Button(pop, text='Acknowledged', command=pop.destroy)
        b.grid(row=1, column=0)

    def cut(self):
        self.textarea.event_generate("<<Cut>>")

    def copy(self):
        self.textarea.event_generate("<<Copy>>")

    def paste(self):
        self.textarea.event_generate("<<Paste>>")

    def openFile(self):
        if self.fname != "":
            # Try to open the file
            # set the window title
            self.master.title(os.path.basename(self.fname))
            self.textarea.delete(1.0, END)
            file = open(self.__file, "r")
            self.textarea.insert(1.0, file.read())
            file.close()

    def saveFile(self):
        if self.fname != "" and exists(self.fname):
            try:
                fout = open(self.fname, "w+")
                fout.write(self.textarea.get("1.0", END))
                fout.close()
            except Exception e:
                self.create_popup(mess='Failed to save file.')

    def execute(self):
        prg = self.textarea.get("1.0", END)
        if bf.syncheck(prg):
            bf.evaluate(prg)

    def cmpl(self):
        return

# Creates root Window


win = Window()
print(win)
mainloop()
