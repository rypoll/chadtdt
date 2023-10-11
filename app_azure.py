"""
Example script for testing the Azure ttk theme
Author: rdbende
License: MIT license
Source: https://github.com/rdbende/ttk-widget-factory
"""

import os
import tkinter as tk
from tkinter import ttk
from tkinter import Tk, ttk, Canvas, Toplevel, Label, Frame
from helper_functions import detect_phone_number, contains_emoji, emoji_reducer, should_ask_question, find_and_replace_questions, count_A_lines, remove_question, save_profile, save_cold_opener, update_status_label, get_response, fix_text, save_personal_details, extract_text_from_file, get_text_between_tags




class App(ttk.Frame):
    BLUE = "#007fff"

    def __init__(self, parent):
        ttk.Frame.__init__(self)

        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # Create value lists
        self.option_menu_list = ["", "OptionMenu", "Option 1", "Option 2"]
        self.combo_lang_list = ["English", "Spanish"]
        self.readonly_combo_list = ["Readonly combobox", "Item 1", "Item 2"]

        # Create control variables
        self.var_0 = tk.BooleanVar()
        self.var_1 = tk.BooleanVar(value=True)
        self.var_2 = tk.BooleanVar()
        self.var_3 = tk.IntVar(value=2)
        self.var_4 = tk.StringVar(value=self.option_menu_list[1])
        self.var_5 = tk.DoubleVar(value=75.0)
        
        # Autoflirt variables
        # 1. Active mode
        self.toggle_var = tk.IntVar(value=0)
        #2. manual login 
        self.manual_login_var = tk.IntVar()
        #3. simple mode
        self.simple_mode_var = tk.IntVar() 
        #4. Language
        self.language_var = tk.StringVar()
        self.language_var.set("Select Language")



        # Create widgets :)
        self.setup_widgets()
    
    def show_tooltip(self, event, text):
        x = event.widget.winfo_rootx() + 25
        y = event.widget.winfo_rooty() + 25

        # Create tooltip
        self.tooltip = Toplevel(self.master)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = Label(self.tooltip, text=text, relief="solid", borderwidth=1, anchor='w', justify='left')
        label.pack()




    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


    def show_customisation_window(self):
        file_path = '01-processing-files/01-split-sys-msg-method/02-getting2know-sys-msg.txt'
        profile_text = get_text_between_tags(file_path, "# Profile of A:")
        skills_text = get_text_between_tags(file_path, "# \"A\"'s skills:")
        new_window = tk.Toplevel()
        new_window.title("Customise Profile")
        bg_color = self.master.cget("background")
        new_window.configure(bg=bg_color)
        
        # Vertical line to separate the two sections
        tk.Frame(new_window, width=1, bg="gray").grid(row=0, column=1, rowspan=7, sticky="ns")

        # Title for Profile
        title1 = tk.Label(new_window, text="1. Customize profile", font=("Arial", 12), anchor="w", bg=bg_color)
        title1.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Elements for Profile
        description_label1 = tk.Label(new_window, text="• Enter your profile in the text box below.\n• The model will use this to personalise your conversartions.\n• Talk in the second person e.g 'He is from Iceland'. \n• Use the below numbered list as a guide:\n\n1. Where you're from\n2. Age\n3. Past education/career info (short)\n4. Current job\n5. Hobbies\n6. Life Achievements\n7. Where you live now. \n8.What you're looking for on the app", anchor="w", bg=bg_color, justify=tk.LEFT)  # Your text here
        description_label1.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        text_entry1 = tk.Text(new_window, height=10, width=40, font=("Arial", 10),
                      bg="black",  # Background color
                      borderwidth=2,  # Border width
                      highlightbackground=self.BLUE,  # Border color when widget doesn't have focus
                      highlightcolor=self.BLUE,  # Border color when widget has focus
                      highlightthickness=2)  # Border thickness

        
        text_entry1.grid(row=2, column=0, padx=10, pady=10)
        text_entry1.insert(tk.END, profile_text)
        save_button1 = ttk.Button(new_window, text="Save Profile", command=lambda: save_profile(text_entry1, saved_label1, "# Profile of A:"))
        save_button1.grid(row=3, column=0)
        saved_label1 = tk.Label(new_window, text="", bg=bg_color)
        saved_label1.grid(row=4, column=0)
        
        # Title for Skills
        title2 = tk.Label(new_window, text="2. Customize your skills", font=("Arial", 12), anchor="w", bg=bg_color)
        title2.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        # Elements for Skills
        description_label2 = tk.Label(new_window, text="• Add your skills in Bullet point form \n• For example '* Great painter' is one bullet", anchor="w", bg=bg_color, justify=tk.LEFT)  # Your text here
        description_label2.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        text_entry2 = tk.Text(new_window, height=10, width=40, font=("Arial", 10),
                      bg="black",  # Background color
                      borderwidth=2,  # Border width
                      highlightbackground=self.BLUE,  # Border color when widget doesn't have focus
                      highlightcolor=self.BLUE,  # Border color when widget has focus
                      highlightthickness=2)  # Border thickness
        text_entry2.grid(row=2, column=2, padx=10, pady=10)
        text_entry2.insert(tk.END, skills_text)
        save_button2 = ttk.Button(new_window, text="Save Skills", command=lambda: save_profile(text_entry2, saved_label2, "# \"A\"'s skills:"))
        save_button2.grid(row=3, column=2)
        saved_label2 = tk.Label(new_window, text="", bg=bg_color)
        saved_label2.grid(row=4, column=2)
        
        
        # Second vertical line to separate the third section
        tk.Frame(new_window, width=1, bg="gray").grid(row=0, column=3, rowspan=7, sticky="ns")

        # Title for Personal Details
        title3 = tk.Label(new_window, text="3. Customize your personal details", font=("Arial", 12), anchor="w", bg=bg_color)
        title3.grid(row=0, column=4, padx=10, pady=0, sticky="w")

        # Elements for Personal Details
        # Create a frame to hold the labels and entries
        details_frame = tk.Frame(new_window, bg=bg_color)
        details_frame.grid(row=2, column=4, sticky="w", padx=10)

        # Text entry for Name
        name_label = tk.Label(details_frame, text="Name:", bg=bg_color)
        name_label.grid(row=0, column=0, sticky="w")
        name_entry = tk.Entry(details_frame, font=("Arial", 10), bg="black",  # Background color
                      borderwidth=2,  # Border width
                      highlightbackground=self.BLUE,  # Border color when widget doesn't have focus
                      highlightcolor=self.BLUE,  # Border color when widget has focus
                      highlightthickness=2)  # Border thickness
        name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Text entry for City
        city_label = tk.Label(details_frame, text="City:", bg=bg_color)
        city_label.grid(row=1, column=0, sticky="w")
        city_entry = tk.Entry(details_frame, font=("Arial", 10), bg="black",  # Background color
                      borderwidth=2,  # Border width
                      highlightbackground=self.BLUE,  # Border color when widget doesn't have focus
                      highlightcolor=self.BLUE,  # Border color when widget has focus
                      highlightthickness=2)  # Border thickness
        city_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Text entry for Area within the city
        area_label = tk.Label(details_frame, text="Area within the city you live:", bg=bg_color)
        area_label.grid(row=2, column=0, sticky="w")
        area_entry = tk.Entry(details_frame, font=("Arial", 10), bg="black",  # Background color
                      borderwidth=2,  # Border width
                      highlightbackground=self.BLUE,  # Border color when widget doesn't have focus
                      highlightcolor=self.BLUE,  # Border color when widget has focus
                      highlightthickness=2)  # Border thickness
        area_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        
        # Text entry for Area within the city
        activity_label = tk.Label(details_frame, text="An activity you do:", bg=bg_color)
        activity_label.grid(row=3, column=0, sticky="w")
        activity_entry = tk.Entry(details_frame, font=("Arial", 10), bg="black",  # Background color
                      borderwidth=2,  # Border width
                      highlightbackground=self.BLUE,  # Border color when widget doesn't have focus
                      highlightcolor=self.BLUE,  # Border color when widget has focus
                      highlightthickness=2)  # Border thickness
        activity_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        phone_label = tk.Label(details_frame, text="Your phone number:", bg=bg_color)
        phone_label.grid(row=4, column=0, sticky="w")
        phone_entry = tk.Entry(details_frame, font=("Arial", 10), bg="black",  # Background color
                      borderwidth=2,  # Border width
                      highlightbackground=self.BLUE,  # Border color when widget doesn't have focus
                      highlightcolor=self.BLUE,  # Border color when widget has focus
                      highlightthickness=2)  # Border thickness
        phone_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        
        
        name_entry.insert(0, extract_text_from_file("messages/02-cold-opener-simple-method-es.txt", "soy ", ","))
        city_entry.insert(0, extract_text_from_file("01-processing-files/02-simple-method/02a-question-tag-es.txt", "parte de ", " eres"))
        area_entry.insert(0, extract_text_from_file("01-processing-files/02-simple-method/02a-question-tag-es.txt", "Yo vivo en ", "."))
        activity_entry.insert(0, extract_text_from_file("01-processing-files/02-simple-method/02a-question-tag-es.txt", "gusta mucho", "."))
        phone_entry.insert(0, extract_text_from_file("01-processing-files/01-split-sys-msg-method/03-soft-close-mid-sys-msg-es.txt", "phone number is", "."))

        # Save button for Personal Details
        save_button3 = ttk.Button(
        new_window, 
        text="Save Personal Details (and All)", 
        command=lambda: (
            save_personal_details(name_entry, city_entry, area_entry, activity_entry, phone_entry, saved_label3),
            save_profile(text_entry2, saved_label2, "# \"A\"'s skills:"),
            save_profile(text_entry1, saved_label1, "# Profile of A:")
            )
        )

        save_button3.grid(row=3, column=4, pady=10)
        saved_label3 = tk.Label(new_window, text="", bg=bg_color)
        saved_label3.grid(row=4, column=4)
        for index in range(5):  # Adjust the range based on the number of rows and columns you have
            new_window.grid_rowconfigure(index=index, weight=1)
            new_window.grid_columnconfigure(index=index, weight=1)
        # Add Sizegrip
        sizegrip = ttk.Sizegrip(new_window)
        sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))
    
    def show_cold_customisation__window(self):
        #bg_color = "#F0F0F0"
        bg_color = self.master.cget("background")
        new_window = tk.Toplevel()
        new_window.title("Customise Cold Openers")
        new_window.configure(bg=bg_color)

        # Title for Cold Openers
        title1 = tk.Label(new_window, text="1. Customize Cold Openers", font=("Arial", 12), anchor="w", bg=bg_color)
        title1.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Elements for Cold Openers
        description_label1 = tk.Label(new_window, text="• Enter your cold openers below\n• Each new line should be a separate cold opener", anchor="w", bg=bg_color, justify=tk.LEFT)
        description_label1.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Dropdown for language selection
        language_var = tk.StringVar(value="English")
        language_label = tk.Label(new_window, text="Choose openers' language:", bg=bg_color)
        language_dropdown = ttk.OptionMenu(new_window, language_var, "English", "English", "Spanish")
        language_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        language_dropdown.grid(row=2, column=0, padx=200, pady=5, sticky="w")


        
        text_entry1 = tk.Text(new_window, height=10, width=40, font=("Arial", 10),
                      bg="black",  # Background color
                      borderwidth=2,  # Border width
                      highlightbackground=self.BLUE,  # Border color when widget doesn't have focus
                      highlightcolor=self.BLUE,  # Border color when widget has focus
                      highlightthickness=2)  # Border thickness
        text_entry1.grid(row=3, column=0, padx=10, pady=10)

        def load_content():
            file_name = 'messages/01-cold-openers.txt' if language_var.get() == 'English' else 'messages/01-cold-openers-es.txt'
            if os.path.exists(file_name):
                with open(file_name, 'r') as f:
                    text_entry1.delete(1.0, tk.END)  # Clear existing text
                    text_entry1.insert(tk.END, f.read())

        load_content()
        language_var.trace("w", lambda *args: load_content())  # Reload content when language changes
    

        # Save button, move it to row 4
        save_button1 = ttk.Button(new_window, text="Save Openers", command=lambda: save_cold_opener(text_entry1, saved_label1, language_var.get()  ))
        save_button1.grid(row=4, column=0)
            
        # Save label, move it to row 5
        saved_label1 = tk.Label(new_window, text="", bg=bg_color)
        saved_label1.grid(row=5, column=0)
        
    def setup_widgets(self):
            # Create a Frame for the Checkbuttons
            self.check_frame = ttk.LabelFrame(self, text="1. Preferences", padding=(20, 10))
            self.check_frame.grid(
                row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew"
            )

                    # Tooltip texts
            tooltip_texts = [
                "Tooltip for Active Mode",
                "Tooltip for First time use",
                "Tooltip for Simple Mode",
                "Tooltip for Select Opener Language",
                "Tooltip for Msg matched within n days",
                "Tooltip for Msg first n conv"
            ]

            # Checkbuttons and Labels
            for i, (text, tooltip_text) in enumerate(zip(
                ["Active Mode", "First time use", "Simple Mode", "Select Opener Language", "Msg matched within n days", "Msg first n conv"],
                tooltip_texts
            )):
                # Create a frame to hold the label and info icon
                label_frame = Frame(self.check_frame)
                label_frame.grid(row=i, column=0, padx=5, pady=10, sticky="nsew")

                label = ttk.Label(label_frame, text=text)
                label.pack(side="left")

                # i icon
                bg_color = self.master.cget("background")
                info_icon = Canvas(label_frame, width=20, height=20, bg=bg_color, highlightthickness=0)
                info_icon.pack(side="left")
                info_icon.create_oval(2, 2, 18, 18, outline="white", fill="")
                info_icon.create_text(10, 10, text="i", fill="white")
                info_icon.bind("<Enter>", lambda event, text=tooltip_text: self.show_tooltip(event, text))
                info_icon.bind("<Leave>", self.hide_tooltip)
            
            
            
            
            
            
            

            self.check_1 = ttk.Checkbutton(
                self.check_frame, variable=self.toggle_var, style="Switch.TCheckbutton"
            )
            self.check_1.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

            # self.label_for_check_2 = ttk.Label(self.check_frame, text="First time use")
            # self.label_for_check_2.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
            self.check_2 = ttk.Checkbutton(
                self.check_frame,  variable=self.manual_login_var, style="Switch.TCheckbutton"
            )
            self.check_2.grid(row=1, column=1, padx=5, pady=10, sticky="nsew")
            
            # self.label_for_check_3 = ttk.Label(self.check_frame, text="Simple Mode")
            # self.label_for_check_3.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
            self.check_3 = ttk.Checkbutton(
                self.check_frame, variable=self.simple_mode_var, style="Switch.TCheckbutton"
            )
            self.check_3.grid(row=2, column=1, padx=5, pady=10, sticky="nsew")
            
            # # Language
            # self.label_for_check_4 = ttk.Label(self.check_frame, text="Select Opener Language")
            # self.label_for_check_4.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")
            self.combobox_1 = ttk.Combobox(self.check_frame, state="readonly", values=self.combo_lang_list, textvariable=self.language_var, text="test")
            #self.combobox_1.current(0)
            self.combobox_1.insert(0, "Select Language")
            self.combobox_1.grid(row=3, column=1, padx=5, pady=10, sticky="nsew")
            
            # # Days limit
            # self.label_for_check_5 = ttk.Label(self.check_frame, text="Msg matched within n days")
            # self.label_for_check_5.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")
            self.days_entry = ttk.Spinbox(self.check_frame, width=5, from_=1, to=10000, increment=1)
            self.days_entry.insert(0, "30")
            self.days_entry.grid(row=4, column=1, padx=5, pady=10, sticky="nsew")
            
            # self.spinbox = ttk.Spinbox(self.widgets_frame, from_=0, to=100, increment=0.1)
            # self.spinbox.insert(0, "Spinbox")
            # self.spinbox.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
            

            # First n convs
            # self.label_for_check_6 = ttk.Label(self.check_frame, text="Msg first n conv")
            # self.label_for_check_6.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")
            self.conversations_entry = ttk.Spinbox(self.check_frame,  from_=1, to=10000, increment=1)
            self.conversations_entry.grid(row=5, column=1, padx=5, pady=10, sticky="nsew")  # Adjusted column
            self.conversations_entry.insert(0,"10")  # Default value
            




            # Separator
            self.separator = ttk.Separator(self)
            self.separator.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="ew")

            # Create a Frame for the Radiobuttons
            self.radio_frame = ttk.LabelFrame(self, text="2. Personalize Conversations", padding=(20, 10))
            self.radio_frame.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="nsew")
            self.radio_frame.grid_rowconfigure(0, weight=2)
            self.radio_frame.grid_columnconfigure(0, weight=2)
            self.radio_frame.grid_columnconfigure(1, weight=2)
            
            
            
            
            
            
            self.accentbutton_1 = ttk.Button(
                self.radio_frame, text="Customize Profile", command=self.show_customisation_window
            )
            self.accentbutton_1.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
            
            
            self.accentbutton_2 = ttk.Button(
                self.radio_frame, text="Customize Openers", command=self.show_cold_customisation__window
            )
            self.accentbutton_2.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

            # # Radiobuttons
            # self.radio_1 = ttk.Radiobutton(
            #     self.radio_frame, text="Unselected", variable=self.var_3, value=1
            # )
            # self.radio_1.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
            # self.radio_2 = ttk.Radiobutton(
            #     self.radio_frame, text="Selected", variable=self.var_3, value=2
            # )
            # self.radio_2.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
            # self.radio_4 = ttk.Radiobutton(
            #     self.radio_frame, text="Disabled", state="disabled"
            # )
            # self.radio_4.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

            # Create a Frame for input widgets
            self.widgets_frame = ttk.LabelFrame(self, text="3. Run", padding=(20, 10))
            # self.widgets_frame.grid(
            #     row=0, column=1, padx=10, pady=(30, 10), sticky="nsew", rowspan=3
            # )
            #self.widgets_frame.columnconfigure(index=0, weight=1)
            self.widgets_frame.grid(
                row=0, column=1, padx=(20, 10), pady=(20, 10),  sticky="nsew"
            )
            
            # Notebook
            self.notebook = ttk.Notebook(self.widgets_frame)  # Changed the parent to self.widgets_frame
            self.notebook.grid(row=0, column=0, sticky="nsew")


            # Tab #1
            self.tab_1 = ttk.Frame(self.notebook)
            for index in [0, 1]:
                self.tab_1.columnconfigure(index=index, weight=1)
                self.tab_1.rowconfigure(index=index, weight=1)
            self.notebook.add(self.tab_1, text="First messages")

            # ... (rest of your code for tabs and widgets inside tabs)

            # Tab #2
            self.tab_2 = ttk.Frame(self.notebook)
            self.notebook.add(self.tab_2, text="Chat")

            # Tab #3
            # self.tab_3 = ttk.Frame(self.notebook)
            # self.notebook.add(self.tab_3, text="Tab 3")
            
            
            

            # Entry
            # self.entry = ttk.Entry(self.widgets_frame)
            # self.entry.insert(0, "Entry")
            # self.entry.grid(row=0, column=0, padx=5, pady=(0, 10), sticky="ew")

            # # Spinbox
            # self.spinbox = ttk.Spinbox(self.widgets_frame, from_=0, to=100, increment=0.1)
            # self.spinbox.insert(0, "Spinbox")
            # self.spinbox.grid(row=1, column=0, padx=5, pady=10, sticky="ew")

            # # Combobox
            # self.combobox = ttk.Combobox(self.widgets_frame, values=self.combo_lang_list)
            # self.combobox.current(0)
            # self.combobox.grid(row=2, column=0, padx=5, pady=10, sticky="ew")

            # # Read-only combobox
            # self.readonly_combo = ttk.Combobox(
            #     self.widgets_frame, state="readonly", values=self.readonly_combo_list
            # )
            # self.readonly_combo.current(0)
            # self.readonly_combo.grid(row=3, column=0, padx=5, pady=10, sticky="ew")

            # # Menu for the Menubutton
            # self.menu = tk.Menu(self)
            # self.menu.add_command(label="Menu item 1")
            # self.menu.add_command(label="Menu item 2")
            # self.menu.add_separator()
            # self.menu.add_command(label="Menu item 3")
            # self.menu.add_command(label="Menu item 4")

            # # Menubutton
            # self.menubutton = ttk.Menubutton(
            #     self.widgets_frame, text="Menubutton", menu=self.menu, direction="below"
            # )
            # self.menubutton.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")

            # # OptionMenu
            # self.optionmenu = ttk.OptionMenu(
            #     self.widgets_frame, self.var_4, *self.option_menu_list
            # )
            # self.optionmenu.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")

            # # Button
            # self.button = ttk.Button(self.widgets_frame, text="Button")
            # self.button.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")

            # # Accentbutton
            # self.accentbutton = ttk.Button(
            #     self.widgets_frame, text="Accent button", style="Accent.TButton"
            # )
            # self.accentbutton.grid(row=7, column=0, padx=5, pady=10, sticky="nsew")

            # # Togglebutton
            # self.togglebutton = ttk.Checkbutton(
            #     self.widgets_frame, text="Toggle button", style="Toggle.TButton"
            # )
            # self.togglebutton.grid(row=8, column=0, padx=5, pady=10, sticky="nsew")

            # # Switch
            # self.switch = ttk.Checkbutton(
            #     self.widgets_frame, text="Switch", style="Switch.TCheckbutton"
            # )
            # self.switch.grid(row=9, column=0, padx=5, pady=10, sticky="nsew")

            # Panedwindow
            self.paned = ttk.PanedWindow(self)
            self.paned.grid(row=0, column=2, pady=(25, 5), sticky="nsew", rowspan=3)

            # Pane #1
            self.pane_1 = ttk.Frame(self.paned, padding=5)
            self.paned.add(self.pane_1, weight=1)

            # Scrollbar
            self.scrollbar = ttk.Scrollbar(self.pane_1)
            self.scrollbar.pack(side="right", fill="y")

            # Treeview
            self.treeview = ttk.Treeview(
                self.pane_1,
                selectmode="browse",
                yscrollcommand=self.scrollbar.set,
                columns=(1, 2),
                height=10,
            )
            self.treeview.pack(expand=True, fill="both")
            self.scrollbar.config(command=self.treeview.yview)

            # Treeview columns
            self.treeview.column("#0", anchor="w", width=120)
            self.treeview.column(1, anchor="w", width=120)
            self.treeview.column(2, anchor="w", width=120)

            # Treeview headings
            self.treeview.heading("#0", text="Column 1", anchor="center")
            self.treeview.heading(1, text="Column 2", anchor="center")
            self.treeview.heading(2, text="Column 3", anchor="center")

            # Define treeview data
            treeview_data = [
                ("", 1, "Parent", ("Item 1", "Value 1")),
                (1, 2, "Child", ("Subitem 1.1", "Value 1.1")),
                (1, 3, "Child", ("Subitem 1.2", "Value 1.2")),
                (1, 4, "Child", ("Subitem 1.3", "Value 1.3")),
                (1, 5, "Child", ("Subitem 1.4", "Value 1.4")),
                ("", 6, "Parent", ("Item 2", "Value 2")),
                (6, 7, "Child", ("Subitem 2.1", "Value 2.1")),
                (6, 8, "Sub-parent", ("Subitem 2.2", "Value 2.2")),
                (8, 9, "Child", ("Subitem 2.2.1", "Value 2.2.1")),
                (8, 10, "Child", ("Subitem 2.2.2", "Value 2.2.2")),
                (8, 11, "Child", ("Subitem 2.2.3", "Value 2.2.3")),
                (6, 12, "Child", ("Subitem 2.3", "Value 2.3")),
                (6, 13, "Child", ("Subitem 2.4", "Value 2.4")),
                ("", 14, "Parent", ("Item 3", "Value 3")),
                (14, 15, "Child", ("Subitem 3.1", "Value 3.1")),
                (14, 16, "Child", ("Subitem 3.2", "Value 3.2")),
                (14, 17, "Child", ("Subitem 3.3", "Value 3.3")),
                (14, 18, "Child", ("Subitem 3.4", "Value 3.4")),
                ("", 19, "Parent", ("Item 4", "Value 4")),
                (19, 20, "Child", ("Subitem 4.1", "Value 4.1")),
                (19, 21, "Sub-parent", ("Subitem 4.2", "Value 4.2")),
                (21, 22, "Child", ("Subitem 4.2.1", "Value 4.2.1")),
                (21, 23, "Child", ("Subitem 4.2.2", "Value 4.2.2")),
                (21, 24, "Child", ("Subitem 4.2.3", "Value 4.2.3")),
                (19, 25, "Child", ("Subitem 4.3", "Value 4.3")),
            ]

            # Insert treeview data
            for item in treeview_data:
                self.treeview.insert(
                    parent=item[0], index="end", iid=item[1], text=item[2], values=item[3]
                )
                if item[0] == "" or item[1] in {8, 21}:
                    self.treeview.item(item[1], open=True)  # Open parents

            # Select and scroll
            self.treeview.selection_set(10)
            self.treeview.see(7)

            # # Notebook, pane #2
            # self.pane_2 = ttk.Frame(self.paned, padding=5)
            # self.paned.add(self.pane_2, weight=3)

            # # Notebook, pane #2
            # self.notebook = ttk.Notebook(self.pane_2)
            # self.notebook.pack(fill="both", expand=True)

            # # Tab #1
            # self.tab_1 = ttk.Frame(self.notebook)
            # for index in [0, 1]:
            #     self.tab_1.columnconfigure(index=index, weight=1)
            #     self.tab_1.rowconfigure(index=index, weight=1)
            # self.notebook.add(self.tab_1, text="Tab 1")

            # # Scale
            # self.scale = ttk.Scale(
            #     self.tab_1,
            #     from_=100,
            #     to=0,
            #     variable=self.var_5,
            #     command=lambda event: self.var_5.set(self.scale.get()),
            # )
            # self.scale.grid(row=0, column=0, padx=(20, 10), pady=(20, 0), sticky="ew")

            # # Progressbar
            # self.progress = ttk.Progressbar(
            #     self.tab_1, value=0, variable=self.var_5, mode="determinate"
            # )
            # self.progress.grid(row=0, column=1, padx=(10, 20), pady=(20, 0), sticky="ew")

            # # Label
            # self.label = ttk.Label(
            #     self.tab_1,
            #     text="Azure theme for ttk",
            #     justify="center",
            #     font=("-size", 15, "-weight", "bold"),
            # )
            # self.label.grid(row=1, column=0, pady=10, columnspan=2)

            # # Tab #2
            # self.tab_2 = ttk.Frame(self.notebook)
            # self.notebook.add(self.tab_2, text="Tab 2")

            # # Tab #3
            # self.tab_3 = ttk.Frame(self.notebook)
            # self.notebook.add(self.tab_3, text="Tab 3")

            # Sizegrip
            self.sizegrip = ttk.Sizegrip(self)
            self.sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))
            



if __name__ == "__main__":
    root = tk.Tk()
    root.title("")

    # Simply set the theme
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")

    app = App(root)
    app.pack(fill="both", expand=True)

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

    root.mainloop()
