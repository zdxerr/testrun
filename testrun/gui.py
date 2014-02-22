from tkinter import *
from tkinter import ttk

# def calculate(*args):
#     try:
#         value = float(feet.get())
#         meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
#     except ValueError:
#         pass
    
# root = Tk()
# root.title("Teststep")

# mainframe = ttk.Frame(root, padding="3 3 12 12")
# mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
# mainframe.columnconfigure(0, weight=1)
# mainframe.rowconfigure(0, weight=1)

# feet = StringVar()
# meters = StringVar()

# feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
# feet_entry.grid(column=2, row=1, sticky=(W, E))

# ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
# ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

# ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
# ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
# ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

# for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

# feet_entry.focus()
# root.bind('<Return>', calculate)

# root.mainloop()
import tkinter

class HyperlinkManager:

    def __init__(self, text):
        self.text = text

        self.text.tag_config("hyper", foreground="blue", underline=1)

        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)

        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return

class App:
    def __init__(self, root):
        self.root = root

        frame = Frame(root, bd=2, relief=SUNKEN)

        xscrollbar = Scrollbar(frame, orient=HORIZONTAL)
        xscrollbar.pack(side=BOTTOM, fill=X)

        yscrollbar = Scrollbar(frame)
        yscrollbar.pack(side=RIGHT, fill=Y)


        text = tkinter.Text(frame, width=40, height=10, 
                            font=("Ubuntu", 13),
                            wrap=NONE,
                            xscrollcommand=xscrollbar.set,
                            yscrollcommand=yscrollbar.set)
        text.pack()
        frame.pack()

        xscrollbar.config(command=text.xview)
        yscrollbar.config(command=text.yview)

        hyperlink = HyperlinkManager(text)

        text.insert(INSERT, "this is a ")
        text.insert(INSERT, "link", hyperlink.add(self.click))
        text.insert(INSERT, "\n\n")

        text.tag_config("code", font=("SourceCodePro", 13))
        text.tag_config("bold", font=("Ubuntu", 13, "bold"))
        text.tag_config("italic", font=("Ubuntu", 13, "italic"))
        text.insert(END, "HELLO\n\n", ("bold"))
        text.insert(END, "HELLO\n\n", ("italic"))
        text.insert(END, "BOTH\n\n", ("bold", "italic"))

        code_string = """# For loop on a list
>>> list = [2, 4, 6, 8]
>>> sum = 0
>>> for num in list:
>>>     sum = sum + num
>>> print("The sum is:", sum)
The sum is: 20"""
        text.insert(END, code_string, ("code"))

        for text in ("link1", "link2", "link3"):
            link = tkinter.Label(text=text, foreground="#0000ff")
            link.bind("<1>", lambda event, text=text: \
                          self.click_link(event, text))
            link.pack()

    def click(self):
        print("CLICK!")

    def click_link(self, event, text):
        print("you clicked '%s'" % text)

root=tkinter.Tk()
app = App(root)
root.mainloop()
