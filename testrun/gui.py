"""
"""

from pprint import pprint

import tkinter as tk

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
        for tag in self.text.tag_names(tk.CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return


class ScrolledText(tk.Text):
    def __init__(self, master, name, **kwargs):
        self.frame = tk.LabelFrame(master, text=name, borderwidth=0)

        x_scrollbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        y_scrollbar = tk.Scrollbar(self.frame)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        super(ScrolledText, self).__init__(self.frame, 
                         xscrollcommand=x_scrollbar.set, 
                         yscrollcommand=y_scrollbar.set,
                         **kwargs)

        x_scrollbar.config(command=self.xview)
        y_scrollbar.config(command=self.yview)

        self.pack(expand=True, fill=tk.BOTH)

        self.links = HyperlinkManager(self)



    def pack(self, *args, **kwargs):
        super(ScrolledText, self).pack(expand=True, fill=tk.BOTH)
        self.frame.pack(*args, **kwargs)

def click(self):
    print("CLICK!")

def add_text_example(question):
    question.insert(tk.INSERT, "this is a ")
    question.insert(tk.INSERT, "link", question.links.add(click))
    question.insert(tk.INSERT, "\n\n")

    question.tag_config("code", font=("Consolas", 13), background='lightgray')
    question.tag_config("bold", font=("Ubuntu", 13, "bold"))
    question.tag_config("italic", font=("Ubuntu", 13, "italic"))
    question.insert(tk.END, "HELLO\n\n", ("bold"))
    question.insert(tk.END, "HELLO\n\n", ("italic"))
    question.insert(tk.END, "BOTH\n\n", ("bold", "italic"))

    question.tag_config('block1', lmargin1=15)
    question.tag_config('block2', lmargin1=25)
    question.tag_config('block3', lmargin1=35)

    question.insert(tk.END, "line1\n", ("block1"))
    question.insert(tk.END, "line2\n", ("block2"))
    question.insert(tk.END, "line3\n", ("block3"))


    code_string = '\n'.join([
        '# For loop on a list',
        '>>> list = [2, 4, 6, 8]',
        '>>> sum = 0',
        '>>> for num in list:',
        '>>>     sum = sum + num',
        '>>> print("The sum is:", sum)',
        'The sum is: 20',
        ])
    question.insert(tk.END, code_string, ("code"))

    question.config(state=tk.DISABLED)

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)

        # always on top
        self.wm_attributes("-topmost", 1)

        self.title("Teststep")

        paned = tk.PanedWindow(self, orient=tk.VERTICAL, sashpad=3, 
                               sashwidth=3, sashrelief=tk.RAISED)
        paned.pack(expand=True, fill=tk.BOTH, pady=3)
        pprint(paned.keys())

        task = ScrolledText(paned, 'Task', width=80, font=("Calibri", 14), 
                                wrap=tk.NONE)
        paned.add(task.frame)
        # task.pack(expand=True, fill=tk.BOTH)

        add_text_example(task)
        
        comment = ScrolledText(self, 'Comment', width=80, height=5, font=("Calibri", 14), wrap=tk.NONE)
        paned.add(comment.frame)

        frame_buttons = tk.Frame(self, pady=3)

        pprint(frame_buttons.keys())

        button_passed = tk.Button(frame_buttons, text="Passed", height=1, command=click)
        button_passed.pack(expand=True, fill=tk.X, side=tk.LEFT, padx=3)
        button_failed = tk.Button(frame_buttons, text="Failed", width=12, height=1, command=click)
        button_failed.pack(expand=True, fill=tk.X, side=tk.LEFT, padx=3)
        button_blocked = tk.Button(frame_buttons, text="Blocked", width=12, height=1, command=click)
        button_blocked.pack(expand=True, fill=tk.X, side=tk.LEFT, padx=3)


        frame_buttons.pack(expand=True, fill=tk.X)

    

    def click_link(self, event, text):
        print("you clicked '%s'" % text)


def question(func):
    print(func)
    print(func.__doc__)
    def inner(*args, **kwargs): #1
        print("Arguments were: %s, %s" % (args, kwargs))
        return func(*args, **kwargs) #2
    return inner


@question
def set_task_configuration(test):
    """
    Set the **configuration** to _something_.
    """
    pass


if __name__ == '__main__':
    # root=tkinter.Tk()
    app = App()
    app.mainloop()



