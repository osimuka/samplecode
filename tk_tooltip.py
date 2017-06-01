try:
    # for Python2
    import Tkinter as tk
except ImportError:
    # for Python3
    import tkinter as tk

# for tk exception message handle
error = tk.TclError


class ToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info',
                 bg="#FFFFFF",
                 fg="#000000",
                 abg="#FFFFFF",
                 tag=None):
        self.waittime = 500    # miliseconds
        self.wraplength = 180  # pixels
        self.widget = widget
        self.text = text
        self.tag = tag
        self.fg = fg
        self.bg = bg
        self.abg = abg  # active background color for buttons and costume widgets
        self.index = None
        if tag:
            self.widget.tag_bind(tag, "<Enter>", self.enter)
            self.widget.tag_bind(tag, "<Leave>", self.leave)
            self.widget.tag_bind(tag, "<ButtonPress>", self.button_press)
        else:
            self.widget.bind("<Enter>", self.enter)
            self.widget.bind("<Leave>", self.leave)
            self.widget.bind("<ButtonPress>", self.button_press)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        color = self.abg
        self.abg = self.widget["background"]
        if self.widget.cget("state") == "disabled":
            return
        if self.tag:
            self.index = self.widget.index("@%s,%s" % (event.x, event.y))
        # when the object doesn't attribute 'activebackground'
        try:
            self.widget.configure(background=color, activebackground=color)
        except error:
            self.widget.configure(background=color)
        finally:
            self.schedule()

    def leave(self, event=None):
        color = self.abg
        self.abg = self.widget["background"]
        try:
            self.widget.configure(background=color, activebackground=color)
        # when the object doesn't attribute 'activebackground'
        except error:
            self.widget.configure(background=color)
        finally:
            self.unschedule()
            self.hidetip()

    def button_press(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        try:
            if self.index:
                x, y, cx, cy = self.widget.bbox(self.index)
            else:
                x, y, cx, cy = self.widget.bbox("insert")
        except:
            pass
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(
            self.tw,
            text=self.text,
            justify='left',
            background=self.bg,
            foreground=self.fg,
            relief='solid',
            borderwidth=0,
            wraplength=self.wraplength
        )
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    ent = tk.Entry(root)
    txt = tk.Text(root, borderwidth=2, relief="sunken")
    ent.pack(side=tk.TOP, padx=5, pady=5)
    txt.pack(side=tk.TOP, padx=5, pady=5)
    txt.insert(tk.END, "Tagged Text\n", "footag")
    txt.insert(tk.END, "Untagged Text\n")
    ToolTip(ent, text="This is an entry widget.", bg="red", fg="white")
    ToolTip(txt, text="This is a text widget.", tag="footag")
    root.mainloop()
