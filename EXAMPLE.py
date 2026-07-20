from Pymenugui import MenuBar, ContextMenu # Both classes
import tkinter as tk
import sys # To close the app

THEME_BG = "#0a0a2e"
THEME_MENU = "#0c0c4f"
THEME_ACCENT = "#d000ff"
THEME_TEXT = "#ffffff"
MAIN_FONT = ('Arial', 10)

root = tk.Tk()
root.attributes('-fullscreen', True) # Makes the window fullscreen

menus = [
  ('File', [
    ('Save', lambda: print('Save Pressed')),
    ('Load', lambda: print('Load Pressed')),
    ('Close', lambda: sys.exit())
  ]),
  ('Edit', [
    ('Select All', lambda: print('SelectAll Pressed'))
  ])
]

MenuBar(root, THEME_MENU, THEME_ACCENT, THEME_TEXT, MAIN_FONT, menus) # Injects Menu Bar

bigframe = tk.Frame(root, bg=THEME_BG) # A frame as big as the window as a widget for the Context Menu
bigframe.pack(fill=tk.BOTH, expand=True)
bigframe.lower()

contextmenucommands = [
  ('Test one', lambda: print("Test1 clicked")),
  ('Test two', lambda: print("Test2 clicked")),
  ('SEPARATOR', None),
  ('Test three', lambda: print("Test3 clicked"))
]

ContextMenu(root, bigframe, THEME_MENU, THEME_TEXT, THEME_ACCENT, MAIN_FONT, contextmenucommands) # Injects context menu

root.mainloop()
