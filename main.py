from themes import *
from functions import *
from Auth import FirebaseAuthentication

from customtkinter import *
import tkinter as tk

class Root(CTk):
    def __init__(self, theme):
        CTk.__init__(self)
        
        self.theme = theme
        self.function_class = Functions()
        
        self.minsize(700, 350)
        self.maxsize(700, 350)
        self.config(bg=theme["bg_color"])
        self.winfo_toplevel().title("SnapShot")
        self.iconbitmap("Assets/logo.ico")
        
        self.top_level = None

        self.main_frame = StartMenu(self, theme, self.function_class)
        self.mainloop()
        
class StartMenu(CTkFrame):
    def __init__(self, root, theme, function_class):
        super().__init__(root)
        
        self.top_level = None
        self.login_menu = None
        self.get_once = False
        self.temp_holder = None
        self.user_id = None
        self.username = None
        
        self.firebase = FirebaseAuthentication()
        
        self.theme = theme
        self.function_class = function_class
        
        self.sender_labels, self.sender_values = self.function_class.createList("Lists\SenderList.txt")
        self.destination_labels, self.destination_values = self.function_class.createList("Lists\SubjectList.txt")
        self.platform_labels, self.platform_values = self.function_class.createList("Lists\PlatformList.txt")
        
        self.discord_local(root)
        self.load_widget_group_one(root)
        self.load_widget_group_two(root)
    
    def discord_local(self, root):
        self.discord_button = CTkButton(root, command=lambda:self.disable_enable("discord"), text="", image=CTkImage(light_image=Image.open(r"Assets/Discord.png"), size=(15, 13)), width=15, height=15, bg_color=self.theme["bg_color"], fg_color=self.theme["bg_color"])
        self.discord_button.grid(row=0, column=0, sticky=NW)
        
        self.local_button = CTkButton(root, command=lambda:self.disable_enable("local"), text="", image=CTkImage(light_image=Image.open(r"Assets/Local.png"), size=(15, 15)), width=15, height=15, bg_color=self.theme["bg_color"], fg_color=self.theme["bg_color"])
        self.local_button.grid(row=0, column=0, sticky=NW,pady=20)
        
    def load_widget_group_one(self, root):
        self.frame_one = CTkFrame(root, corner_radius=30, bg_color=self.theme["bg_color"])
        self.frame_one.grid(row=0, column=0, sticky=W, padx=30)
                
        row = 0 
        self.sender_label = CTkLabel(self.frame_one, text="Sender", text_color=self.theme["label_fg_color"])
        self.sender_label.grid(row=row, column=0, sticky=N)
        CTkLabel(self.frame_one, text="Topic", text_color=self.theme["label_fg_color"]).grid(row=row, column=1, sticky=N)
        
        row = 1
        self.sender_list_menu = CTkOptionMenu(self.frame_one, values=self.sender_labels, width=120)
        self.sender_list_menu.grid(row=row, column=0)
        
        self.subject_list_menu = CTkOptionMenu(self.frame_one, values=self.destination_labels, width=120)
        self.subject_list_menu.grid(row=row, column=1)
    
        row = 2
        CTkLabel(self.frame_one, text="").grid(row=row, column=0)
    
        row = 3
        CTkLabel(self.frame_one, text="Platform", text_color=self.theme["label_fg_color"]).grid(row=row, column=0, sticky=N)
        
        self.pause_label = CTkLabel(self.frame_one, text="Pause/Unpause", text_color=self.theme["label_fg_color"])
        self.pause_label.grid(row=row, column=1, sticky=N)
        
        row = 4
        self.platform_labels.insert(0, "Custom")
        self.platform_values.insert(0, [])
        self.platform_list_menu = CTkOptionMenu(self.frame_one, values=self.platform_labels, width=120)
        self.platform_list_menu.grid(row=row, column=0)
        
        self.pause_value = BooleanVar(value=False)
        self.pause_button = CTkButton(self.frame_one, border_width=2, text="Pause", command=lambda:self.function_class.pause(self.pause_button, self.pause_value))
        self.pause_button.grid(row=row, column=1)
        self.pause_button.configure(width=80)
        
        row = 5
        CTkLabel(self.frame_one, text="").grid(row=row, column=0)
        
        row = 6
        CTkLabel(self.frame_one, text="Starting Point", text_color=self.theme["label_fg_color"]).grid(row=row, column=0, sticky=N)
        
        CTkLabel(self.frame_one, text="Interval", text_color=self.theme["label_fg_color"]).grid(row=row, column=1, sticky=N)
        
        row = 7
        self.starting_point_value = StringVar(value="1")
        self.starting_point_entry = CTkEntry(self.frame_one, width=120, justify=CENTER, textvariable=self.starting_point_value)
        self.starting_point_entry.grid(row=row, column=0)
        
        self.interval_value = DoubleVar(value=0.30)
        CTkButton(self.frame_one, text="<", width=10, border_width=2, command=lambda:[self.function_class.add(self.interval_value, -.10, self.interval_label)]).grid(row=row, column=1, sticky=W)
        CTkButton(self.frame_one, text="<<", width=20, border_width=2, command=lambda:[self.function_class.add(self.interval_value, -1, self.interval_label)]).grid(row=row, column=1, sticky=W, padx=20)
        self.interval_label = CTkLabel(self.frame_one, text="%.2f" % self.interval_value.get(), text_color=self.theme["label_fg_color"])
        self.interval_label.grid(row=row, column=1, sticky=N)
        CTkButton(self.frame_one, text=">", width=10, border_width=2, command=lambda:[self.function_class.add(self.interval_value, .10, self.interval_label)]).grid(row=row, column=1, sticky=E)
        CTkButton(self.frame_one, text=">>", width=20, border_width=2, command=lambda:[self.function_class.add(self.interval_value, 1, self.interval_label)]).grid(row=row, column=1, sticky=E, padx=20)
        
        row = 8
        CTkLabel(self.frame_one, text="").grid(row=row, column=0)
        
        row = 9
        CTkLabel(self.frame_one, text="").grid(row=row, column=0)
        
        row = 10
        CTkLabel(self.frame_one, text="").grid(row=row, column=0)
        
        row = 11
        self.start_button = CTkButton(self.frame_one, text="Start", width=80, border_width=2, command=lambda: [self.function_class.prep_detection(self.firebase),\
                                                                                                     self.start_button.configure(text="Start") if self.start_button.cget("text") == "Stop" else self.start_button.configure(text="Stop")])
        self.start_detection(root)
        self.things()
        
        self.start_button.grid(row=row, column=0, sticky=N)
        CTkButton(self.frame_one, text="✖", width=10, height=10, font=CTkFont(size=5),border_width=2, command=self.delete_previous).grid(row=row, column=1, sticky=NW)
        CTkButton(self.frame_one, text="↶", width=10, height=10, font=CTkFont(size=6),border_width=2, command=self.replace_current).grid(row=row, column=1, sticky=SW)
        CTkButton(self.frame_one, text="📷", width=80, border_width=2, command=self.manual_screenshot).grid(row=row, column=1, sticky=N)
        
    def load_widget_group_two(self, root):
        self.frame_two = CTkFrame(root, corner_radius=30, bg_color=self.theme["bg_color"], fg_color=self.theme["bg_color"])
        self.frame_two.configure(width=root.winfo_width()*2.1, height=root.winfo_height()*1.7)
        self.frame_two.place(relx=0.4)
        self.frame_two.grid_propagate(False)
        
        self.pop_out_button = CTkButton(self.frame_two, text="⬆", width=20, height=20, border_width=2, fg_color=self.theme["bg_color"], command=lambda:[self.pop_out(root, self.firebase),
                                                                                                                                                        self.pop_out_button.configure(text="⬇") if self.pop_out_button.cget("text") == "⬆" else self.pop_out_button.configure(text="⬆")])
        self.pop_out_button.place(relx=0.035, rely=0.04, anchor=CENTER)
        
        self.confidence_value = DoubleVar(value=0.80)
        CTkButton(self.frame_two, text="<<<", width=20, border_width=2, fg_color=self.theme["bg_color"], command=lambda:self.function_class.add(self.confidence_value, -.10, self.confidence_label)).place(relx=0.33, rely=0.04, anchor=CENTER)
        CTkButton(self.frame_two, text="<<", width=20, border_width=2, fg_color=self.theme["bg_color"], command=lambda:self.function_class.add(self.confidence_value, -.05, self.confidence_label)).place(relx=0.255, rely=0.04, anchor=CENTER)
        CTkButton(self.frame_two, text="<", width=20, border_width=2, fg_color=self.theme["bg_color"], command=lambda:self.function_class.add(self.confidence_value, -.01, self.confidence_label)).place(relx=0.196, rely=0.04, anchor=CENTER)
        self.confidence_label = CTkLabel(self.frame_two, text="Confidence: %.2f" % self.confidence_value.get())
        self.confidence_label.place(relx=0.5, rely=0.04, anchor=CENTER)
        CTkButton(self.frame_two, text=">>>", width=20, border_width=2, fg_color=self.theme["bg_color"], command=lambda:self.function_class.add(self.confidence_value, .10, self.confidence_label)).place(relx=0.67, rely=0.04, anchor=CENTER)
        CTkButton(self.frame_two, text=">>", width=20, border_width=2, fg_color=self.theme["bg_color"], command=lambda:self.function_class.add(self.confidence_value, .05, self.confidence_label)).place(relx=0.74, rely=0.04, anchor=CENTER)
        CTkButton(self.frame_two, text=">", width=20, border_width=2, fg_color=self.theme["bg_color"], command=lambda:self.function_class.add(self.confidence_value, .01, self.confidence_label)).place(relx=0.8, rely=0.04, anchor=CENTER)
        
        self.region_selected = CTkLabel(self.frame_two, text="No Region Selected")
        self.region_selected.place(relx=0.5, rely=.89, anchor=CENTER)
        
        self.select_region = CTkButton(self.frame_two, text="+", width=10, height=10, font=CTkFont(size=10), border_width=2, fg_color=self.theme["bg_color"])
        self.select_region.place(relx=0.894, rely=.885, anchor=CENTER)

        self.select_region.bind("<ButtonRelease>", self.trigger)
        
        self.notes_variable = StringVar()
        self.notes_entry = CTkEntry(self.frame_two, width=300, textvariable=self.notes_variable)
        self.notes_entry.place(relx=0.46, rely=0.96, anchor=CENTER)
        self.notes_send = CTkButton(self.frame_two, command=lambda:[self.function_class.send_note(self.notes_variable.get(), self), self.notes_variable.set("")],\
            text="➡", width=20, border_width=2, fg_color=self.theme["bg_color"])
        self.notes_send.place(relx=0.84, rely=0.96, anchor=CENTER)
        
        self.image = CTkImage(light_image=Image.open(r"Assets/white.png"), size=(root.winfo_width()*1.7, root.winfo_height()*1.2))
        self.image_container = CTkLabel(self.frame_two, image=self.image, text="")
        self.image_container.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        self.login = CTkButton(self.frame_two, text="", width=20, height=20, border_width=2, fg_color=self.theme["bg_color"], image=CTkImage(light_image=Image.open(r"Assets/database.png"), size=(10, 15)), \
            command=lambda:[self.open_login_window(root)])
        self.login.place(relx=0.955, rely=0.1, anchor=CENTER)
        
        CTkLabel(self.frame_two, text="Image\nNo.", fg_color=self.theme["bg_color"], font=CTkFont(size=10)).place(relx=0.955, rely=0.4, anchor=CENTER)
        
        self.image_no = CTkLabel(self.frame_two, text="0", fg_color=self.theme["bg_color"], font=CTkFont(size=20))
        self.image_no.place(relx=0.955, rely=0.5, anchor=CENTER)
        
        self.image_no_value = IntVar(value=0)
        CTkButton(self.frame_two, text="-5", fg_color=self.theme["bg_color"], width=8, height=8, font=CTkFont(size=8), border_width=2, command=lambda:self.function_class.add(self.image_no_value, -5, self.image_no, is_float=False)).place(relx=0.935, rely=0.57, anchor=CENTER)
        CTkButton(self.frame_two, text="+5", fg_color=self.theme["bg_color"], width=8, height=8, font=CTkFont(size=8), border_width=2, command=lambda:self.function_class.add(self.image_no_value, 5, self.image_no, is_float=False)).place(relx=0.975, rely=0.57, anchor=CENTER)
        CTkButton(self.frame_two, text="-1", fg_color=self.theme["bg_color"], width=8, height=8, font=CTkFont(size=8), border_width=2, command=lambda:self.function_class.add(self.image_no_value, -1, self.image_no, is_float=False)).place(relx=0.935, rely=0.62, anchor=CENTER)
        CTkButton(self.frame_two, text="+1", fg_color=self.theme["bg_color"], width=8, height=8, font=CTkFont(size=8), border_width=2, command=lambda:self.function_class.add(self.image_no_value, 1, self.image_no, is_float=False)).place(relx=0.975, rely=0.62, anchor=CENTER)

    def sync_buttons(self):
        self.start_button.configure(text="Start" if self.start_button.cget("text") == "Stop" else "Stop")
    
    def open_login_window(self, root):
        if self.login_menu == None:
            self.login_menu = LoginToFirebase(CTkToplevel(root), self, self.theme, self.firebase, self.function_class)
        else:
            self.login_menu.modified_root.destroy()
            self.login_menu = None

    def set_login_status(self, status, username = None):
        if status == "check":
            return self.user_id, self.username
        elif status != None:
            self.user_id = status
            self.username = username
        elif status == None:
            self.user_id = None
            self.username = None
    
    def tksleep(self, t):
        ms = int(t*1000)
        root = tk._get_default_root()
        var = tk.IntVar(root)
        root.after(ms, lambda: var.set(1))
        root.wait_variable(var)
    
    def disable_enable(self, which):
        if which == "local":
            self.sender_label.configure(state="disabled")
            self.sender_list_menu.configure(state="disabled")
            self.notes_entry.configure(state="disabled")
            self.notes_send.configure(state="disabled")
            self.function_class.change_method("local")
            
        if which == "discord":
            self.sender_label.configure(state="normal")
            self.sender_list_menu.configure(state="normal")
            self.notes_entry.configure(state="normal")
            self.notes_send.configure(state="normal")
            self.function_class.change_method("discord")
    
    def things(self):
        if self.top_level != None:
            self.start_button.configure(state="disabled")
            self.pause_button.configure(state="disabled")
            self.pause_label.configure(state="disabled")
            pconfidence = self.top_level.pop_out_values()
            if not self.get_once:
                self.get_once = True
                self.temp_holder = self.confidence_value.get()
            self.confidence_value.set(pconfidence)
            self.top_level.change_no(self.image_no_value.get()-1 if self.image_no_value.get() != 0 else 0)
        else:
            self.start_button.configure(state="normal")
            self.pause_button.configure(state="normal")
            self.pause_label.configure(state="normal")
            self.get_once = False
            self.confidence_value.set(self.temp_holder) if self.temp_holder != None else None
        
        if self.start_button.cget("text") == "Stop":
            self.discord_button.configure(state="disabled")
            self.local_button.configure(state="disabled")
        else:
            self.discord_button.configure(state="normal")
            self.local_button.configure(state="normal")
        
        self.after(500, self.things)
    
    def start_detection(self, root):
        if self.start_button.cget("text") == "Stop":
            self.image_no_value.set(self.function_class.start_detection(self))
            self.image_no.configure(text=str(self.image_no_value.get()-1))
        self.after(int(self.interval_value.get() * 1000), lambda:[self.start_detection(root)])
    
    def pop_out(self, root, firebase):
        if self.top_level == None:   
            self.top_level = PopOut(CTkToplevel(root), self, self.theme, self.function_class,\
                self.start_button.cget("text"), self.pause_value.get(), self.confidence_value.get(),\
                firebase)
        else:
            self.top_level.modified_root.destroy()
            self.top_level = None
    
    def manual_screenshot(self):
        self.image_no_value.set(self.function_class.manual_screenshot(self))
        self.image_no.configure(text=str(self.image_no_value.get()-1))
    
    def delete_previous(self):
        self.image_no_value.set(self.function_class.delete_previous(self))
        self.image_no.configure(text=str(int(self.image_no_value.get())-1))
    
    def replace_current(self):
        self.image_no_value.set(self.function_class.replace_current(self))
        self.image_no.configure(text=str(int(self.image_no_value.get())-1))
    
    def trigger(self, _):
        listener = mouse.Listener(on_click=lambda x, y, button, pressed: self.function_class.select_region(x, y, button, pressed, self.region_selected, self.image, self.image_container))
        listener.start()
    
    def change_values(self):
        sender = self.sender_values[self.sender_labels.index(f"{self.sender_list_menu.get()}")]
        subject_label = self.subject_list_menu.get()
        subject = self.destination_values[self.destination_labels.index(f"{self.subject_list_menu.get()}")]
        platform = self.platform_values[self.platform_labels.index(f"{self.platform_list_menu.get()}")]
        
        return  self.image, self.image_container, \
                float(self.confidence_value.get()),\
                sender, subject_label, subject, platform,\
                int(self.starting_point_value.get())
                

class PopOut(CTkFrame):
    def __init__(self, root, main_window, theme, function_class, start_button_text, pause_value, confidence_value, firebase):
        super().__init__(root)
        
        self.main_window = main_window
        self.theme = theme
        self.function_class = function_class
                
        self.modified_root = root
        self.modified_root.maxsize(70, 300)
        self.modified_root.minsize(70, 300)
        self.modified_root.resizable(0, 0)
        self.modified_root.overrideredirect(1)
        self.modified_root.attributes("-transparentcolor", "grey15")
        
        self.pop_out = CTkFrame(self.modified_root, width=70, height=300, corner_radius=50, bg_color="grey15", fg_color=self.theme["bg_color"])
        self.pop_out.grid(row=0)
        self.pop_out.bind("<ButtonPress-1>", self.start_move)
        self.pop_out.bind("<B1-Motion>", self.move_pop_out)
    
        self.move_button = CTkFrame(self.pop_out, width=15, height=15, corner_radius=30, bg_color="grey15", fg_color="white")
        self.move_button.place(x=0, y=0)
        self.move_button.bind("<ButtonPress-1>", self.start_move)
        self.move_button.bind("<B1-Motion>", self.move_pop_out)
        
        self.pause_value = pause_value
        self.pause_button = CTkButton(self.pop_out, text="⏸" if pause_value == False else "⏯", width=35, height=35, corner_radius=10, bg_color=self.theme["bg_color"],\
            command=lambda:[self.function_class.pause(self.pause_button, self.pause_value, pop_out=True)])
        self.pause_button.place(relx=0.5, rely=0.1, anchor=CENTER)
        self.pause_button.grid_propagate(False)
        
        self.image_no = CTkLabel(self.pop_out, text="0", fg_color=self.theme["bg_color"], font=CTkFont(size=20))
        self.image_no.place(relx=0.5, rely=0.27, anchor=CENTER)
        
        CTkButton(self.pop_out, text=">>", width=17, height=17, command=lambda:self.function_class.add(self.confidence_value, .05, self.confidence_label)).place(relx=0.508, rely=0.56)
        CTkButton(self.pop_out, text=">", width=17, height=17, command=lambda:self.function_class.add(self.confidence_value, .01, self.confidence_label)).place(relx=0.52, rely=0.39)
        
        self.confidence_value = DoubleVar(value=confidence_value)
        self.confidence_label = CTkLabel(self.pop_out, text="%.2f" % self.confidence_value.get())
        self.confidence_label.place(relx=0.34, rely=0.46)
        
        CTkButton(self.pop_out, text="<<", width=17, height=17, command=lambda:self.function_class.add(self.confidence_value, -.05, self.confidence_label)).place(relx=0.092, rely=0.56)
        CTkButton(self.pop_out, text="<", width=17, height=17, command=lambda:self.function_class.add(self.confidence_value, -.01, self.confidence_label)).place(relx=0.22, rely=0.39)
        
        self.manual_screenshot = CTkButton(self.pop_out, text="📷", width=35, height=35, corner_radius=10, bg_color=self.theme["bg_color"],\
            command=lambda:self.main_window.manual_screenshot())
        self.manual_screenshot.place(relx=0.55, rely=0.75, anchor=CENTER)
        self.manual_screenshot.grid_propagate(False)
        
        CTkButton(self.pop_out, text="✖", width=14, height=14, font=CTkFont(size=6), command=main_window.delete_previous).place(relx=0.01, rely=0.70)
        CTkButton(self.pop_out, text="↶", width=14, height=14, font=CTkFont(size=6), command=main_window.replace_current).place(relx=0.01, rely=0.75)
        
        self.start_button = CTkButton(self.pop_out, text="", width=35, height=35, corner_radius=10, bg_color=self.theme["bg_color"], fg_color="green" if start_button_text == "Start" else "red",\
            command=lambda:[self.function_class.prep_detection(firebase), main_window.sync_buttons(), self.start_button.configure(fg_color="green" if self.start_button.cget("fg_color") == "red" else "red")])
        self.start_button.place(relx=0.5, rely=0.9, anchor=CENTER)
        self.start_button.grid_propagate(False)
    
    def pop_out_values(self):
        return  self.confidence_value.get()
    
    def start_move(self, event):
        self.x = event.x
        self.y = event.y
    
    def change_no(self, num):
        self.image_no.configure(text=str(num))
    
    def move_pop_out(self, event):
        x = self.modified_root.winfo_x() - self.x + event.x
        y = self.modified_root.winfo_y() - self.y + event.y
        self.modified_root.geometry(f"+{x}+{y}")

class LoginToFirebase(CTkFrame):
    def __init__(self, root, main_window, theme, firebase, function_class):
        super().__init__(root)
        
        self.modified_root = root
        self.modified_root.maxsize(500, 250)
        self.modified_root.minsize(500, 250)
        self.winfo_toplevel().title("SnapShot Login")
        self.modified_root.attributes('-topmost',True)
        
        self.error_message_exists = False
        self.username = None
        self.welcome = False
        
        self.main_frame = CTkFrame(self.modified_root, width=500, height=250, bg_color=theme["bg_color"], fg_color=theme["bg_color"])
        self.main_frame.grid(row=0)
        
        check_status, username = main_window.set_login_status("check")
        self.username = username
        
        if check_status == None:
            self.login_frame_create(theme, firebase, main_window, root, function_class)
        elif check_status != None:
            self.welcome_screen(theme, firebase, main_window, root, function_class)
        
        print(main_window.set_login_status("check"))
    
    def login_frame_create(self, theme, firebase, main_window, root, function_class):
        CTkLabel(self.main_frame, text="SnapShot", text_color="light blue", font=CTkFont(family="Arial", size=40, weight="bold")).place(relx=0.19, rely=0.1)
        CTkLabel(self.main_frame, text="Login", text_color=theme["label_fg_color"], font=CTkFont(family="Arial", size=40, weight="bold")).place(relx=0.58, rely=0.1)
        
        self.canvas = tk.Canvas(self.main_frame, width=400, height=5, bg="gray", highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.35, anchor=CENTER)
        
        self.login_frame = CTkFrame(self.main_frame, width=300, height=120, bg_color=theme["bg_color"], fg_color=theme["bg_color"], border_width=3, border_color="light blue")
        self.login_frame.place(relx=0.5, rely=0.65, anchor=CENTER)
        
        self.email_variable = StringVar(value="Email Address")
        self.email_entry = CTkEntry(self.login_frame, width=200, height=30, textvariable=self.email_variable)
        self.email_entry.bind("<FocusIn>", lambda e: self.clear("email"))
        self.email_entry.bind("<FocusOut>", lambda e: self.return_value("email"))
        self.email_entry.place(relx=0.5, rely=0.23, anchor=CENTER)
        
        self.password_variable = StringVar(value="Password")
        self.password_entry = CTkEntry(self.login_frame, width=200, height=30, textvariable=self.password_variable, show="")
        self.password_entry.bind("<FocusIn>", lambda e: self.clear("password"))
        self.password_entry.bind("<FocusOut>", lambda e: self.return_value("password"))
        self.password_entry.place(relx=0.5, rely=0.53, anchor=CENTER)
        
        self.login_button = CTkButton(self.login_frame, text="Login", width=80, height=15,\
            command=lambda:self.login(firebase, main_window, root, theme, function_class))
        self.login_button.place(relx=0.5, rely=0.8, anchor=CENTER)
    
    def welcome_screen(self, theme, firebase, main_window, root, function_class):
        CTkLabel(self.main_frame, text="Welcome,", text_color=theme["label_fg_color"], font=CTkFont(family="Arial", size=40, weight="bold")).place(relx=0.5, rely=0.1, anchor=CENTER)
        CTkLabel(self.main_frame, text=f"{self.username}", text_color=theme["label_fg_color"], font=CTkFont(family="Arial", size=20, weight="bold")).place(relx=0.5, rely=0.3, anchor=CENTER)
        
        self.latest_file = CTkLabel(self.main_frame, text=f"Latest file: None", text_color=theme["label_fg_color"], font=CTkFont(family="Arial", size=15, weight="bold"))
        self.latest_file.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        CTkButton(self.main_frame, text="Logout", fg_color="red", hover_color="maroon", width=80, height=30, command=lambda:self.logout(theme, firebase, main_window, root, function_class)).place(relx=0.9, rely=0.1, anchor=CENTER)
        CTkButton(self.main_frame, text="Upload", width=80, height=30, command=lambda:self.upload_files(firebase, function_class, main_window)).place(relx=0.5, rely=0.8, anchor=CENTER)
        self.change_latest_file(function_class)
    
    def upload_files(self, firebase, function_class, main_window):
        error_message = None
        success_message = None
        
        uid, username = main_window.set_login_status("check")
        if function_class.change_latest_file() != None:
            if error_message != None:
                error_message.destroy()
            try:
                firebase.create_new_album(uid, function_class.change_latest_file())
                firebase.upload_folder_to_storage(function_class.change_latest_file(), uid)
                success_message = CTkLabel(self.modified_root, text="File uploaded successfully!", text_color="green", fg_color="black", font=CTkFont(size=10))
                success_message.place(relx=0.5, rely=.95, anchor=CENTER)
            except:
                if success_message != None:
                    success_message.destroy()
                if error_message == None:
                    error_message = CTkLabel(self.modified_root, text="Error uploading file!", text_color="red", fg_color="black", font=CTkFont(size=10))
                    error_message.place(relx=0.5, rely=.95, anchor=CENTER)
        else:
            if success_message != None:
                success_message.destroy()
            if error_message == None:
                error_message = CTkLabel(self.modified_root, text="No file to upload!", text_color="red", fg_color="black", font=CTkFont(size=10))
                error_message.place(relx=0.5, rely=.95, anchor=CENTER)
    
    def change_latest_file(self, function_class):
        try:
            self.latest_file.configure(text=f"Latest file: {function_class.change_latest_file()}")
            self.after(500, lambda:[self.change_latest_file(function_class)])
        except:
            pass

    def login(self, firebase, main_window, root, theme, function_class):
        check_status, username = firebase.sign_in_with_email(self.email_variable.get(), self.password_variable.get())
        if check_status == None:
            if not self.error_message_exists:
                self.error_message_exists = True
                self.error_message = CTkLabel(self.modified_root, text="Invalid Email or Password. No account or forgot password? Click", text_color="red", fg_color="black", font=CTkFont(size=10))
                self.redirect = CTkLabel(self.modified_root, text="Here", fg_color = "black", text_color="white", font=CTkFont(size=10, underline=True))

                self.error_message.place(relx=0.5, rely=.95, anchor=CENTER)
                self.redirect.place(relx=0.81, rely=.95, anchor=CENTER)
            print("error signing in")
        else:
            if self.error_message_exists:
                self.error_message_exists = False
                self.error_message.destroy()
                self.redirect.destroy()
            main_window.set_login_status(check_status, username)
            self.username = username
            self.clear_widgets()
            self.welcome = True
            self.welcome_screen(theme, firebase, main_window, root, function_class)
            print(f"{username} has signed in")
            
    def clear_widgets(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def clear(self, which):
        if which == "email" and self.email_variable.get() == "Email Address":
            self.email_variable.set("")
        if which == "password" and self.password_variable.get() == "Password":
            self.password_variable.set("")
            self.password_entry.configure(show="*")
    
    def return_value(self, which):
        if which == "email" and self.email_variable.get() == "":
            self.email_variable.set("Email Address")
        if which == "password" and self.password_variable.get() == "":
            self.password_variable.set("Password")
            self.password_entry.configure(show="")
            
    def logout(self, theme, firebase, main_window, root, function_class):
        main_window.set_login_status(None)
        self.welcome = False
        self.username = None
        self.clear_widgets()
        self.login_frame_create(theme, firebase, main_window, root, function_class)
Root(DARK)