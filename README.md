# Python Menu GUI

Hello! I have made a custom MenuGUI Library for customization, of course, you can always use `tk.Menu()` using Tkinter, but that lacks customization.
This library's main purpose is to give more personality to the menus. This library so far, cannot be used as a thing to create windows like **Tkinter**.

# How To Use

Currently, this only works with **2** things. Menubars, and Context Menus (when you right click and a menu appears).

First, you will need to get the file in this repository called `Pymenugui.py`. When you need it, put the file in the same directory as your script.

If you want to use it like `Pymenugui.MenuBar()`, use `import Pymenugui`

If you want to use it like `MenuBar()`, use  `from Pymenugui import MenuBar`.

# How can I use MenuBar()?

MenuBar requires **6 parameters**.

You will need to have Tkinter in your file.

First, make a tkinter window, using `root = tkinter.Tk()`. This will be the window that your menu bar is injected into.

You will also need 3 Theme variables, to make them, you can make constants called:

THEME_MENU (for your menu bg)
THEME_ACCENT (highlights)
THEME_TEXT (color of text)

These will need RGB Hex values ("#0a0a2e", "d000ff", etc.)

Next you will need your main font. You can call it in another variable called MAIN_FONT, containing something like:
`('Arial', 10)` (font, size)

Finally, you will need to pass in the commands you want (you can add submenus, just you cannot add a submenu inside of a submenu).

How to pass in the commands, is by making a new variable, and it must be a list. It will work like this:

```
menus = [ # button appearing on menu bar
  ('File', [
    ('Save', lambda: print('Save Pressed')), # command inside of menu
    ('Load', lambda: print('Load Pressed'))
  ]),
  ('Edit', [
    # more commands here
  ])
]
```

Now, to inject your menubar, use
`Pymenugui.MenuBar(tk_window, THEME_MENU, THEME_ACCENT, THEME_TEXT, MAIN_FONT, menus)`

After injecting it, use `tk_window.mainloop()` to run the window.

# How can I use ContextMenu()?

You will need the same variables as of **MenuBar()**

You will need to change the menus variable to be only commands.

You will also need to have a widget to pair it to (`tk.Frame()` and such)

And then use `Pymenugui.ContextMenu(tk_window, widget, THEME_MENU, THEME_TEXT, THEME_ACCENT, MAIN_FONT, menus)`

If you want to add a line in between commands, in your menus list, add a command saying `('SEPARATOR', None)`

# Is there an example?

You can find an example in `EXAMPLE.py` inside of this repository.
