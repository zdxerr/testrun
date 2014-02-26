"""
"""

from pprint import pprint

import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk


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

class ImageManager:
    def __init__(self, text):
        self.text = text
        self.images = {}

    def add(self, file):
        image = self.images[file] = ImageTk.PhotoImage(Image.open(file))
        return image


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
        self.images = ImageManager(self)



    def pack(self, *args, **kwargs):
        super(ScrolledText, self).pack(expand=True, fill=tk.BOTH)
        self.frame.pack(*args, **kwargs)

def click():
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



    question.image_create(tk.END, image=question.images.add('flowers.jpg'))

    question.insert(tk.END, "\nline1\n", ("block1"))
    question.insert(tk.END, "line2\n", ("block2"))
    question.insert(tk.END, "line3\n\n", ("block3"))


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

class ProgressBar(tk.Canvas):
    def __init__(self, master, values=[0], **kwargs):
        super(ProgressBar, self).__init__(master, **kwargs)

        self.values = values
        self.colors = ['#96c6e2', '#2b8cc4']
        self.text = ''
        self.text_color = '#003a69'
        self.text_color_active = '#000000'

        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        print('YOHO', event)
        print('RESIZE_PB', event.type, event.height, event.width)

        px_per_row = event.height / len(self.values)

        # px_per_row = event.height / rows
        print('px_per_row', px_per_row)
        # print('rows', rows)

        for index, value in enumerate(self.values):
            print('value * event.width', value * event.width)
            self.create_rectangle(0, index * px_per_row, 
                                  value * event.width, (index + 1) * px_per_row, 
                                  fill=self.colors[index], outline='')
        # progress_bar.create_rectangle(0, 8, 170, 16, fill="#2b8cc4", outline='')

        self.create_text((5, event.height / 2), anchor=tk.W, fill='#003a69', activefill='#000000', font=("Calibri", 9), text=self.text)


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)

        # always on top
        self.wm_attributes("-topmost", 1)
        # transparency
        self.attributes("-alpha", 0.85)

        self.title("Teststep")
        self.iconbitmap("icons\\accept.ico")

        status_frame = ttk.Frame(self)

        status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        ttk.Sizegrip(status_frame).pack(side=tk.RIGHT)

        measureSystem = tk.StringVar()


        def changed():
            print('OHO!', measureSystem.get())


        check = ttk.Checkbutton(status_frame, text='Always on top', 
                                command=changed, variable=measureSystem, 
                                onvalue='metric', offvalue='imperial')
        check.pack(side=tk.RIGHT)

        # progress_bar = tk.Canvas(status_frame, height=16) 
        progress_bar = ProgressBar(status_frame, values=[0.93, 0.75], height=0)
        progress_bar.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)

        # def resize_pb(event):
        #     print('YOHO', event)
        #     print('RESIZE_PB', event.type, event.height, event.width)

        # progress_bar.bind("<Configure>", resize_pb)

        # progress_bar.create_rectangle(0, 0, 50, 8, fill="#96c6e2", outline='')
        # progress_bar.create_rectangle(0, 8, 170, 16, fill="#2b8cc4", outline='')
        # progress_bar.create_text((5, 2), anchor=tk.NW, fill='#003a69', activefill='#000000', font=("Calibri", 9), text="Hello World!")

        frame_buttons = tk.Frame(self, pady=3)

        button_passed = tk.Button(frame_buttons, text="Passed", height=1, command=self.click)
        button_passed.pack(expand=True, fill=tk.X, side=tk.LEFT, padx=3)
        button_failed = tk.Button(frame_buttons, text="Failed", width=12, height=1, command=self.click)
        button_failed.pack(expand=True, fill=tk.X, side=tk.LEFT, padx=3)
        button_blocked = tk.Button(frame_buttons, text="Blocked", width=12, height=1, command=self.click)
        button_blocked.pack(expand=True, fill=tk.X, side=tk.LEFT, padx=3)

        frame_buttons.pack(side=tk.BOTTOM, expand=True, fill=tk.X)

        pb = ttk.Progressbar(self, orient=tk.HORIZONTAL, 
                             mode='determinate')
        pb.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)

        paned = tk.PanedWindow(self, orient=tk.VERTICAL, sashpad=3, 
                               sashwidth=3, sashrelief=tk.RAISED)
        paned.pack(expand=True, fill=tk.BOTH, pady=3)
        # pprint(paned.keys())

        task = ScrolledText(paned, 'Task', width=80, font=("Calibri", 14), 
                            wrap=tk.NONE)
        paned.add(task.frame)
        # task.pack(expand=True, fill=tk.BOTH)

        add_text_example(task)
        
        comment = ScrolledText(self, 'Comment', width=80, height=5, font=("Calibri", 14), wrap=tk.NONE)
        paned.add(comment.frame)


        def ignore(event):
            print('YOHO', event)
            # pprint(dir(event))
            # print(event.type, event.height)
            print(event.widget.sash_coord(0))
            # print(event.delta)
            # event.widget.sash_place(0, 1, int(event.height / 2))

        paned.bind("<Configure>", ignore)

        
    

    def click(self):
        import os
        import random
        icons = [os.path.join('icons', f) 
                 for f in os.listdir('icons') 
                 if f.endswith('.ico')]
        print("you clicked")
        self.iconbitmap(random.choice(icons))


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



