import tkinter as tk

class ContextMenu:
    def __init__(self, root, bind_target, menutheme, texttheme, accenttheme, font, commands):
        self.root = root
        self.bind_target = bind_target  
        self.menutheme = menutheme
        self.texttheme = texttheme
        self.accenttheme = accenttheme
        self.font = font
        self.commands = commands
        
        self.active_popup = None

        self.bind_target.bind("<Button-3>", self.show_popup)
        self.bind_target.bind("<Button-2>", self.show_popup)
        
        self.root.bind("<Button-1>", self.close_popup_on_click, add="+")

    def show_popup(self, event):
        if self.active_popup:
            self.destroy_popup()

        active_window = self.bind_target.winfo_toplevel()

        x = event.x_root - active_window.winfo_rootx()
        y = event.y_root - active_window.winfo_rooty()

        geom_y = int(active_window.geometry().split('+')[2])
        title_bar_offset = active_window.winfo_y() - geom_y

        if title_bar_offset > 0:
            y -= title_bar_offset

        self.active_popup = tk.Frame(
            active_window, 
            bg=self.menutheme, 
            bd=2, 
            relief='solid', 
            highlightbackground=self.accenttheme
        )

        if isinstance(self.bind_target, tk.Canvas):
            x = event.x
            y = event.y
            self.bind_target.create_window(x, y, window=self.active_popup, anchor=tk.NW, tags="context_menu_window")
        else:
            self.active_popup.place(x=x, y=y)
            self.active_popup.lift()

        for item in self.commands:
            label_text, func = item
            
            if label_text == "SEPARATOR":
                divider = tk.Frame(self.active_popup, bg=self.accenttheme, height=1)
                divider.pack(fill=tk.X, padx=5, pady=4)
            else:
                opt_btn = tk.Label(
                    self.active_popup, 
                    text=label_text, 
                    bg=self.menutheme, 
                    fg=self.texttheme, 
                    font=self.font, 
                    padx=25, 
                    pady=6, 
                    cursor='hand2', 
                    anchor='w'
                )
                opt_btn.pack(fill=tk.X)

                opt_btn.bind('<Enter>', lambda e, b=opt_btn: b.config(bg=self.accenttheme))
                opt_btn.bind('<Leave>', lambda e, b=opt_btn: b.config(bg=self.menutheme))

                def make_click_handler(action_func=func):
                    return lambda e: self.execute_and_close(action_func)

                opt_btn.bind('<Button-1>', make_click_handler())

    def execute_and_close(self, func):
        if func:
            func()
        self.destroy_popup()

    def destroy_popup(self):
        if self.active_popup:
            self.active_popup.destroy()
            self.active_popup = None
        if isinstance(self.bind_target, tk.Canvas):
            self.bind_target.delete("context_menu_window")

    def close_popup_on_click(self, event):
        if not self.active_popup:
            return

        click_x = event.x_root
        click_y = event.y_root

        pop_x = self.active_popup.winfo_rootx()
        pop_y = self.active_popup.winfo_rooty()
        pop_w = self.active_popup.winfo_width()
        pop_h = self.active_popup.winfo_height()

        in_popup = (
            pop_x <= click_x < pop_x + pop_w and
            pop_y <= click_y < pop_y + pop_h
        )

        if not in_popup:
            self.destroy_popup()

class MenuBar:
    def __init__(self, root, menutheme, accenttheme, texttheme, font, menu):
        self.root = root
        self.menutheme = menutheme
        self.accenttheme = accenttheme
        self.texttheme = texttheme
        self.font = font
        self.menu = menu

        self.active_menu = None
        self.active_label = None
        self.active_submenu = None

        self.root.bind('<Button-1>', self.close_menu_on_click)

        self.setup_custom_menu()
    
    def setup_custom_menu(self):
        self.menu_bar = tk.Frame(self.root, bg=self.menutheme, height=40)
        self.menu_bar.pack(side=tk.TOP, fill=tk.X)
        self.menu_bar.lift()
        self.menu_bar.pack_propagate(False)

        for label, commands in self.menu:
            btn = tk.Label(self.menu_bar, text=label, bg=self.menutheme, fg=self.texttheme, font=self.font, padx=20, pady=10, cursor='hand2')
            btn.pack(side=tk.LEFT)

            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=self.accenttheme))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg=self.menutheme))

            btn.bind('<Button-1>', lambda e, lbl=label, cmds=commands: self.toggle_menu(lbl, cmds))

    def toggle_menu(self, label_text, commands):
        if self.active_label and self.active_label.cget('text') == label_text and self.active_menu:
            self.active_menu.destroy()
            if self.active_submenu:
                self.active_submenu.destroy()
                self.active_submenu = None
            self.active_menu = None
            self.active_label = None
            return
        
        if self.active_menu:
            self.active_menu.destroy()
        
        if self.active_submenu:
            self.active_submenu.destroy()
            self.active_submenu = None

        clicked_btn = None
        for widget in self.menu_bar.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget('text') == label_text:
                clicked_btn = widget
                break

        if not clicked_btn:
            return
        
        self.root.update_idletasks()
        
        x = clicked_btn.winfo_rootx() - self.root.winfo_rootx()
        y = (clicked_btn.winfo_rooty() + clicked_btn.winfo_height()) - self.root.winfo_rooty()

        self.active_menu = tk.Frame(self.root, bg=self.menutheme, bd=2, relief='solid', highlightbackground=self.menutheme)
        self.active_menu.place(x=x, y=y)
        self.active_label = clicked_btn

        for s_widget in self.active_menu.winfo_children():
            if isinstance(s_widget, tk.Label) and s_widget.cget('text') == label_text:
                clicked_btn = s_widget

        for item in commands:
            if isinstance(item, tuple) and len(item) == 2 and isinstance(item[1], (list, tuple)):
                sub_label, sub_commands = item
                textshow = sub_label + '   ▶'

                sub_btn = tk.Label(self.active_menu, text=textshow, bg=self.menutheme, fg=self.texttheme, font=self.font, padx=20, pady=5, cursor='hand2', anchor='w')
                sub_btn.pack(fill=tk.X)

                sub_btn.bind('<Enter>', lambda e, b=sub_btn: b.config(bg=self.accenttheme))
                sub_btn.bind('<Leave>', lambda e, b=sub_btn: b.config(bg=self.menutheme))

                def open_submenu(sub_cmds=sub_commands, parent_btn=sub_btn):
                    new_x = parent_btn.winfo_rootx() + parent_btn.winfo_width()
                    new_y = parent_btn.winfo_rooty()

                    self.active_submenu = tk.Frame(self.root, bg=self.menutheme, bd=2, relief='solid', highlightbackground=self.menutheme)
                    self.active_submenu.place(x=new_x, y=new_y)

                    for s_label, s_func in sub_cmds:
                        s_btn = tk.Label(self.active_submenu, text=s_label, bg=self.menutheme, fg=self.texttheme, font=self.font, padx=20, pady=5, cursor='hand2', anchor='w')
                        s_btn.pack(fill=tk.X)

                        s_btn.bind('<Enter>', lambda e, b=s_btn: b.config(bg=self.accenttheme))
                        s_btn.bind('<Leave>', lambda e, b=s_btn: b.config(bg=self.menutheme))

                        def on_s_click(func=s_func, frame=self.active_submenu):
                            func()
                            frame.destroy()

                        s_btn.bind('<Button-1>', lambda e, f=on_s_click: f())

                sub_btn.bind('<Button-1>', lambda e, f=open_submenu: f())
            else:
                opt_text, opt_func = item
                opt_btn = tk.Label(self.active_menu, text=opt_text, bg=self.menutheme, fg=self.texttheme, font=self.font, padx=20, pady=5, cursor='hand2', anchor='w')
                opt_btn.pack(fill=tk.X)

                opt_btn.bind('<Enter>', lambda e, b=opt_btn: b.config(bg=self.accenttheme))
                opt_btn.bind('<Leave>', lambda e, b=opt_btn: b.config(bg=self.menutheme))

                def on_click(func=opt_func):
                    func()
                    if self.active_menu:
                        self.active_menu.destroy()
                        if self.active_submenu:
                            self.active_submenu.destroy()
                            self.active_submenu = None
                        self.active_menu = None
                        self.active_label = None

                opt_btn.bind('<Button-1>', lambda e, f=on_click: f())

    def close_menu_on_click(self, event):
        if not self.active_menu:
            return

        click_x = event.x_root
        click_y = event.y_root

        menu_bar_x = self.menu_bar.winfo_rootx()
        menu_bar_y = self.menu_bar.winfo_rooty()
        menu_bar_w = self.menu_bar.winfo_width()
        menu_bar_h = self.menu_bar.winfo_height()

        if menu_bar_w == 0 or menu_bar_h == 0:
            return

        in_menu_bar = (
            menu_bar_x <= click_x < menu_bar_x + menu_bar_w and
            menu_bar_y <= click_y < menu_bar_y + menu_bar_h
        )

        menu_x = self.active_menu.winfo_rootx()
        menu_y = self.active_menu.winfo_rooty()
        menu_w = self.active_menu.winfo_width()
        menu_h = self.active_menu.winfo_height()

        if menu_w == 0 or menu_h == 0:
            return

        in_active_menu = (
            menu_x <= click_x < menu_x + menu_w and
            menu_y <= click_y < menu_y + menu_h
        )

        if not in_menu_bar and not in_active_menu:
            self.active_menu.destroy()
            self.active_menu = None
            self.active_label = None
