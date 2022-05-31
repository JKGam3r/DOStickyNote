# Application's purpose is used for quick, short notes
# "Frontend Development - the code in this file will be tested with continuous run-throughs, NOT from the 'StickyNoteTester.py file'

# Taskbar application image

import tkinter
from tkinter import *
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfile
from tkinter import messagebox

import warnings

import os

import time

from squareRoot17ToolTip import *
from StickyNoteLogic import *

from PIL import Image, ImageTk

# True if default text displayed, False if it is not
default_text_visible = True

# The font type for the text area
font_name = "Times"

# The size of the font
font_size = 12

'''
Color scheme
'''
# The current color being displayed for the sticky note
current_color = "YELLOW"

# All of the different colors
COLORS = [
            "YELLOW",
            "BLACK",
            "WHITE",
            "GREEN",
            "PINK",
            "PURPLE",
            "BLUE"
]

# Used for mapping a color to its position in the list
COLOR_INDEXES = {
            "YELLOW": 0,
            "BLACK": 1,
            "WHITE": 2,
            "GREEN": 3,
            "PINK": 4,
            "PURPLE": 5,
            "BLUE": 6
}

# Colors for the "sticky" top part of the sticky note
TOP_COLORS = {
            "YELLOW": "#FFF0AB",
            "BLACK": "#000000",
            "WHITE": "#D6D6D6",
            "GREEN": "#77BE6A",
            "PINK": "#D5AAC1",
            "PURPLE": "#AD88C6",
            "BLUE": "#9CC1D9"
}

# The color of the body (text area) of the sticky note
BODY_COLORS = {
            "YELLOW": "#FFF5CB",
            "BLACK": "#2A2A2A",
            "WHITE": "#FFFFFF",
            "GREEN": "#89E877",
            "PINK": "#F2D2E3",
            "PURPLE": "#CDA2EA",
            "BLUE": "#C1DFF3"
}

# The colors for the text in the sticky note
TEXT_COLORS = {
            "YELLOW": "black",
            "BLACK": "white",
            "WHITE": "black",
            "GREEN": "black",
            "PINK": "black",
            "PURPLE": "white",
            "BLUE": "black"
}

# Space for the title bar
TITLE_BAR_HEIGHT = 30

# Amount of space the text area takes up (dimensions relative to window)
TEXT_AREA_WIDTH_FACTOR = 0.95
TEXT_AREA_HEIGHT_FACTOR = 0.8

# Text shown when user has not typed anything
PLACE_HOLDER_TEXT = "Start typing here..."

# Create the root window
root = Tk();

# Set root properties
root.geometry("300x300")
root.eval('tk::PlaceWindow . center')
root.configure(bg=BODY_COLORS[current_color])

# "Frameless window"
root.overrideredirect(True)

# Used for .exe file
# https://pythonprogramming.altervista.org/auto-py-to-exe-only-one-file-with-images-for-our-python-apps/
def resource_path2(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Creates a custom title bar along with all of the buttons and functionality associated with it
class CustomTitleBar:
    # Constructor
    def __init__(self, root, title, height, text_area):
        # The instantiated window from above
        self.root = root

        # The name of this new title bar
        self.title = title

        # How tall (height) the new title bar should be
        self.height = height

        # Location of mouse on x-axis
        self.mouse_x = 0

        # Location of mouse on y-axis
        self.mouse_y = 0

        # Place all components on this frame
        self.title_bar = Frame(self.root, bg=TOP_COLORS[current_color], relief="raised", bd=0)

        # The area where the user will type text
        self.text_area = text_area

        # The height of the three-dot option's settings box
        self.add_opt_height = 150

        # The button currently representing the color of the sticky note
        self.currently_selected_color_button = None

        # True if 'Save-As' (first time saving already occurred), False if not
        self.saved_already = False

        # Location where file is saved
        self.save_directory = None

        # The pre-set types of files that this document can be saved as
        self.files = [
                 ('DO Sticky Note', '*.syn'),
                 ('Text Document', '*.txt'),
                 ('All Files', '*.*')]

        # An array of all the color buttons
        self.color_buttons = []

        # Create a title for the new title bar
        self.title_label = Label(self.title_bar, text=self.title, bg=TOP_COLORS[current_color], fg="black")

        # Create a close button on the title bar
        self.close_button = Button(self.title_bar, text="   ✕   ", bg=TOP_COLORS[current_color], fg="black", relief="raised",
                              command=self.display_warning_message)

        # Create a button responsible for additional options
        self.three_dot_button = Button(self.title_bar, text=" • • • ", bg=TOP_COLORS[current_color], fg="black",
                                  relief="raised", command=self.display_three_dot_options)

        # Create a button responsible for keeping this application on top of all others
        path = resource_path2("StickyNoteOnTopIcon.png")
        im = Image.open(path)
        imRz = None

        # Depreciation warning unnecessary - program will not use other version of imports
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            imRz = im.resize((16, 32), Image.ANTIALIAS)

        ph = ImageTk.PhotoImage(imRz)
        self.on_top_button = Button(self.title_bar, bg="darkgray", image=ph,
                                  relief="raised", command=self.on_top_functionality)
        self.on_top_button.image = ph

        # True if this application should stay on top, False if it does not matter
        self.stay_on_top = True
        self.on_top_button.config(bg="white")
        self.root.attributes('-topmost', self.stay_on_top)

        # Used for additional options if the user clicks the three dots
        self.three_dot_frame = Frame(self.root, bg="black")
        self.add_three_dot_buttons()

    # Get mouse (x, y) location to keep track of coordinates right before user tries dragging application
    def move_pos(self, e):
        self.mouse_x = e.x
        self.mouse_y = e.y

    # Allows the user to move the application
    def move_app(self, e):
        self.root.geometry(f'+{e.x_root - self.mouse_x}+{e.y_root - self.mouse_y}')

    # Displays a message box informing the user that unsaved data will be lost
    def display_warning_message(self):
        # True if user confirms wanting to close, False if not
        close_app = messagebox.askokcancel("Are You Sure?", "All unsaved data will be lost.  Continue?")

        if close_app:
            self.root.quit()

    # Changes the color of the sticky note
    def change_note_color(self, h):
        global current_color

        # Remove marker from old button
        self.currently_selected_color_button.config(text="")

        # Set new button text and set variable to this current button
        h[0].config(text="⚪")
        self.currently_selected_color_button = h[0]

        # And now change the color of the 'current_color' variable
        current_color = COLORS[h[4]]

        # Now change the color of the sticky note by changing each component individually
        self.root.config(bg=h[1])
        text_area_text = h[3]

        if(default_text_visible):
            text_area_text = "darkgray"
        self.text_area.config(bg=h[1], fg=text_area_text, insertbackground=h[3])

        self.title_bar.config(bg=h[2])
        self.title_label.config(bg=h[2], fg=h[3])
        self.close_button.config(bg=h[2], fg=h[3])
        self.three_dot_button.config(bg=h[2], fg=h[3])

        text_modification.update_colors()

    # Retrieves the sticky note with formatting (if applicable)
    def get_sticky_note(self, file):
        extension = os.path.splitext(file.name)[1]

        # Open the contents of the new file and write them into the program's text area
        with open(file.name, 'r') as f:
            if extension == '.syn': # .syn file is formatted a specific way
                # Split into appropriate parts
                parts = f.read().split('\n')

                # Include the correct color scheme
                global default_text_visible
                default_text_visible = False
                self.change_note_color(
                    [self.color_buttons[COLOR_INDEXES[parts[2]]], BODY_COLORS[parts[2]], TOP_COLORS[parts[2]],
                     TEXT_COLORS[parts[2]], COLOR_INDEXES[parts[2]]])
                self.text_area.config(state=NORMAL)
                self.text_area.delete("1.0", END)
                self.text_area.config(fg=TEXT_COLORS[parts[2]])

                # Step 0: Separate between plain text and tagged text, along with adding in plain text
                self.text_area.insert("1.0", parts[0])

                # Step 1: Remove square brackets ('[' and ']')
                og_string = parts[1]
                file_string = og_string[1 : len(og_string)-1]

                # Step 2: Split into an array of strings
                raw_array = file_string.split('), ')

                # Step 3: Remove unnecessary characters from each string
                # Note that int i used instead of iterating over actual strings to change contents of the array
                for i in range(len(raw_array)):
                    # Remove closing parenthesis
                    if raw_array[i][0] == '(':
                        raw_array[i] = raw_array[i][1 : len(raw_array[i])-1]

                # Step 4: Make an array of arrays
                attr_array = []
                for s in raw_array:
                    whole_string = s
                    if s[0] == '\'':
                        whole_string = s[1 : len(s)]
                    tuple = whole_string.split('\', ')
                    attr_array.append(tuple)

                # Step 5: Remove any extra apostrophes
                for t in attr_array:
                    for i in range(len(t)):
                        if t[i][0] == '\'':
                            t[i] = t[i][1 : len(t[i])]
                        if t[i][len(t[i])-1] == '\'':
                            t[i] = t[i][0 : len(t[i])-1]

                '''
                Now construct the text in the text area
                    * 0th index --> key1 (type)
                    * 1st index --> value1 (description/ tag
                    * 2nd index --> index1 (position)
                '''
                typ_em = None
                mod_text = None
                text_length = 0
                text_modification.bold_id = 0
                text_modification.italics_id = 0
                text_modification.underline_id = 0
                text_modification.normal_id = 0
                for t in attr_array:
                    # End of tag for formatted text; cover appropriate text with said formatting
                    if t[0] == 'tagoff':
                        # Start of tag present, now we have the end, so start formatting
                        if typ_em is not None:
                            typ_em_attr = ""
                            if typ_em[1][0] == 'b':
                                typ_em_attr = " bold"
                                text_modification.bold_id += 1
                            elif typ_em[1][0] == 'i':
                                typ_em_attr = " italic"
                                text_modification.italics_id += 1
                            elif typ_em[1][0] == 'u':
                                typ_em_attr = " underline"
                                text_modification.underline_id += 1
                            elif typ_em[1][0] == 'n':
                                typ_em_attr = ""
                                text_modification.normal_id += 1

                            self.text_area.tag_add(typ_em[1], typ_em[2], t[2])
                            self.text_area.tag_configure(typ_em[1], font=f'{font_name} {font_size}{typ_em_attr}')
                            # Reset tag start
                            typ_em = None
                    elif t[0] == 'tagon':
                        typ_em = t

                # A 'tagon' may not have an associated 'tagoff' if the formatting extends to the very end
                # of the text string, so make sure if this happens, the appropriate formatting is added
                if typ_em is not None:
                    typ_em_attr = ""
                    if typ_em[1][0] == 'b':
                        typ_em_attr = " bold"
                        text_modification.bold_id += 1
                    elif typ_em[1][0] == 'i':
                        typ_em_attr = " italic"
                        text_modification.italics_id += 1
                    elif typ_em[1][0] == 'u':
                        typ_em_attr = " underline"
                        text_modification.underline_id += 1
                    elif typ_em[1][0] == 'n':
                        typ_em_attr = ""
                        text_modification.normal_id += 1

                    self.text_area.tag_add(typ_em[1], typ_em[2], END)
                    self.text_area.tag_configure(typ_em[1], font=f'{font_name} {font_size}{typ_em_attr}')

            else: # All other files
                text_area.config(state=NORMAL, fg=TEXT_COLORS[current_color])
                text_area.delete("1.0", END)
                text_area.insert(INSERT, f.read())

    # Opens another file; note that this action will save all updated text to the same file
    def open_button_functionality(self):
        file = self.upload_button_functionality()

        if file == None:
            return

        # We are opening and modifying a file, therefore, saving can be done
        self.saved_already = True
        self.save_directory = file.name

    # Uploads another file; note that this action copies the contents of the given file, but does NOT modify them
    def upload_button_functionality(self):
        # Create the file
        file = askopenfile(filetypes=self.files, defaultextension=self.files)

        # User may have exited; in general, directory was not found
        if file == None:
            return

        self.get_sticky_note(file)

        return file # returned for the open_button_functionality() method

    # Acts as 'Save' and 'Save As' to store the text contents of a file
    def save_button_functionality(self):
        if not self.saved_already:
            # Create the file
            file = asksaveasfile(filetypes=self.files, defaultextension=self.files)

            # User may have exited; in general, directory was not found
            if file == None:
                return

            # Write the contents to the file
            with open(file.name, 'w') as f:
                f.write(self.text_area.get("1.0", "end-1c") + "\n") # plain text
                f.write(str(self.text_area.dump("1.0", "end-1c")) + "\n") # formatting
                f.write(current_color) # sticky note color scheme

            self.saved_already = True
            self.save_directory = file.name

        else:
            with open(self.save_directory, 'w') as f:
                f.write(self.text_area.get("1.0", "end-1c") + "\n") # plain text
                f.write(str(self.text_area.dump("1.0", "end-1c")) + "\n") # formatting
                f.write(current_color)  # sticky note color scheme

    # Makes all of the buttons found on the three-dot frame
    def add_three_dot_buttons(self):
        # Store number of colors
        num_colors = len(BODY_COLORS)

        # Store x-position and dimension
        self.root.update()
        x_pos = 0
        b_width = self.root.winfo_width() / num_colors

        # Height of color buttons, y-position of open/ upload/ save buttons
        layer_border = self.add_opt_height / 2
        tuck = 1; # buttons visible even when "hidden," use this variable to completely hide them when necessary
        btn_num = 0 # Index of each button
        # Add in each color as a button
        for body_hex, top_hex, text_hex in zip(BODY_COLORS.values(), TOP_COLORS.values(), TEXT_COLORS.values()):
            b = Button(self.three_dot_frame, bg=body_hex)
            self.color_buttons.append(b)
            b.config(command=lambda h=[b, body_hex, top_hex, text_hex, btn_num]: self.change_note_color(h))
            btn_num += 1

            # Immediately set current color button
            if self.currently_selected_color_button == None:
                self.currently_selected_color_button = b
                b.config(text="⚪")

            b.place(x=x_pos, y=tuck, width=b_width, height=layer_border)
            x_pos += b_width

        # Now add in the open, upload, and save buttons
        ds_width = self.root.winfo_width() / 3 # Width (and x-pos) of open, upload and save buttons
        open_button = Button(self.three_dot_frame, text="Open Note", command=self.open_button_functionality)
        open_button.place(x=0, y=layer_border + tuck, width=ds_width, height=layer_border - tuck)
        upload_button = Button(self.three_dot_frame, text="Upload Note", command=self.upload_button_functionality)
        upload_button.place(x=ds_width, y=layer_border+tuck, width=ds_width, height=layer_border-tuck)
        save_button = Button(self.three_dot_frame, text="Save Note", command=self.save_button_functionality)
        save_button.place(x=ds_width*2, y=layer_border+tuck, width=ds_width, height=layer_border-tuck)

    # Shows the additional options in the three-dot menu
    def display_three_dot_options(self):
        position_text_area(self.add_opt_height)
        self.three_dot_frame.place(x=0, y=0, relwidth=1, height=self.add_opt_height)

    # Will either make sure this application stays on top of all other programs, or it will act normally
    def on_top_functionality(self):
        if self.stay_on_top:
            self.stay_on_top = False
            self.on_top_button.config(bg="darkgray")
        else:
            self.stay_on_top = True
            self.on_top_button.config(bg="white")

        self.root.attributes('-topmost', self.stay_on_top)

    # Creates the fake title bar
    def create_title_bar(self):
        self.title_bar.place(x=0, y=0, relwidth=1, height=self.height)

        # Bind the title bar
        self.title_bar.bind("<Motion>", self.move_pos)
        self.title_bar.bind("<B1-Motion>", self.move_app)

        # Pack all the components
        self.title_label.pack(side=LEFT, pady=2)
        self.close_button.pack(side=RIGHT, pady=4)
        self.three_dot_button.pack(side=RIGHT, pady=4)
        self.on_top_button.pack(side=RIGHT, pady=4)

        create_tool_tip(self.on_top_button, "Keeps this sticky note on top of all applications when turned on.")
        create_tool_tip(self.three_dot_button, "Allows access to changing the color of the sticky note and other opening/ saving files.")
        create_tool_tip(self.close_button, "Closes the application.")

# Used for modifying the text (such as changing text casing and alignment)
class TextModification:
    # Constructor
    def __init__(self, root, text_area, y_pos, relwidth, height):
        # The main window
        self.root = root

        # The text area in which the user types in
        self.text_area = text_area

        # The frame upon which the text modification components will set
        self.mod_frame = Frame(root, bg=BODY_COLORS[current_color])

        # CAPS button - capitalizes all highlighted text
        self.caps_button = Button(self.mod_frame, text="CAPS", command=self.cap_chars,
                                  bg=BODY_COLORS[current_color], fg=TEXT_COLORS[current_color])

        # lower button - makes all highlighted characters lower case
        self.lower_button = Button(self.mod_frame, text="lower", command=self.low_chars,
                                   bg=BODY_COLORS[current_color], fg=TEXT_COLORS[current_color])

        # Bold button - makes selected text bold
        self.bold_button = Button(self.mod_frame, text=" B ", font="Times 9 bold", command=self.bold_chars,
                             bg=BODY_COLORS[current_color], fg=TEXT_COLORS[current_color])
        # Used in tags to keep track of which modification is being made to the text area
        self.bold_id = 0

        # Italics button - makes selected text italics
        self.italics_button = Button(self.mod_frame, text=" I ", font="Times 9 italic", command=self.italicize_chars,
                             bg=BODY_COLORS[current_color], fg=TEXT_COLORS[current_color])
        # Used in tags to keep track of which modification is being made to the text area
        self.italics_id = 0

        # Underline button - makes selected text underlined
        self.underline_button = Button(self.mod_frame, text=" U ", font="Times 9 underline", command=self.underline_chars,
                             bg=BODY_COLORS[current_color], fg=TEXT_COLORS[current_color])
        # Used in tags to keep track of which modification is being made to the text area
        self.underline_id = 0

        # Normal button - makes selected text regular text
        self.normal_button = Button(self.mod_frame, text=" N ", font="Times 9", command=self.normal_chars,
                             bg=BODY_COLORS[current_color], fg=TEXT_COLORS[current_color])
        # Used in tags to keep track of which modification is being made to the text area
        self.normal_id = 0

        # The y-position of the frame
        self.y_pos = y_pos

        # The (relative) width of the frame
        self.relwidth = relwidth

        # The height of the frame
        self.height = height

    # Changes selected text to reflect all capital letters
    def cap_chars(self):
        if self.text_area.tag_ranges(tkinter.SEL):
            # Convert all characters to capitals
            s = capitalize_all_characters(self.text_area.get(tkinter.SEL_FIRST, tkinter.SEL_LAST))

            # Replace the text
            self.text_area.delete(tkinter.SEL_FIRST, tkinter.SEL_LAST)
            caret_pos = self.text_area.index(tkinter.INSERT)
            self.text_area.insert(caret_pos, s)

    # Changes selected text to reflect all lower case letters
    def low_chars(self):
        if self.text_area.tag_ranges(tkinter.SEL):
            # Convert all characters to lower case
            s = lowercase_all_characters(self.text_area.get(tkinter.SEL_FIRST, tkinter.SEL_LAST))

            # Replace the text
            self.text_area.delete(tkinter.SEL_FIRST, tkinter.SEL_LAST)
            caret_pos = self.text_area.index(tkinter.INSERT)
            self.text_area.insert(caret_pos, s)

    # Changes selected text to reflect all bold characters
    def bold_chars(self):
        if self.text_area.tag_ranges(tkinter.SEL):
            # Make all selected characters bold
            self.text_area.tag_add('bold_' + str(self.bold_id), SEL_FIRST, SEL_LAST)
            self.text_area.tag_configure('bold_' + str(self.bold_id), font=f'{font_name} {font_size} bold')
            self.bold_id += 1

    # Changes selected text to reflect all italicized characters
    def italicize_chars(self):
        if self.text_area.tag_ranges(tkinter.SEL):
            # Make all selected characters italicized
            self.text_area.tag_add('italics_' + str(self.italics_id), SEL_FIRST, SEL_LAST)
            self.text_area.tag_configure('italics_' + str(self.italics_id), font=f'{font_name} {font_size} italic')
            self.italics_id += 1

    # Changes selected text to reflect all underlined characters
    def underline_chars(self):
        if self.text_area.tag_ranges(tkinter.SEL):
            # Make all selected characters underlined
            self.text_area.tag_add('underline_' + str(self.underline_id), SEL_FIRST, SEL_LAST)
            self.text_area.tag_configure('underline_' + str(self.underline_id), font=f'{font_name} {font_size} underline')
            self.underline_id += 1

    # Changes selected text to reflect all underlined characters
    def normal_chars(self):
        if self.text_area.tag_ranges(tkinter.SEL):
            # Make all selected characters normal
            self.text_area.tag_add('normal_' + str(self.normal_id), SEL_FIRST, SEL_LAST)
            self.text_area.tag_configure('normal_' + str(self.normal_id), font=f'{font_name} {font_size}')
            self.normal_id += 1

    # Creates the bar at the bottom of the GUI with all of the necessary components
    def create_mod_bar(self):
        self.mod_frame.place(x=0, y=self.y_pos, relwidth=self.relwidth, height=self.height)

        self.caps_button.pack(side=LEFT)
        self.lower_button.pack(side=LEFT)

        self.normal_button.pack(side=RIGHT)
        self.underline_button.pack(side=RIGHT)
        self.italics_button.pack(side=RIGHT)
        self.bold_button.pack(side=RIGHT)

        create_tool_tip(self.caps_button, "Capitalizes all selected characters in the text area.")
        create_tool_tip(self.lower_button, "Makes all selected characters in the text area lower case.")
        create_tool_tip(self.bold_button, "Makes all selected characters in the text area bold.")
        create_tool_tip(self.italics_button, "Makes all selected characters in the text area italicized.")
        create_tool_tip(self.underline_button, "Makes all selected characters in the text area underlined.")
        create_tool_tip(self.normal_button, "Removes all bold, italics, and underlining from selected text in the text area.")

    # Updates the colors of all of the components
    def update_colors(self):
        self.mod_frame.config(bg=BODY_COLORS[current_color])
        self.caps_button.config(bg=BODY_COLORS[current_color], fg=TEXT_COLORS[current_color])
        self.lower_button.config(bg=BODY_COLORS[current_color], fg=TEXT_COLORS[current_color])
        self.bold_button.config(bg=BODY_COLORS[current_color], fg=TEXT_COLORS[current_color])
        self.italics_button.config(bg=BODY_COLORS[current_color], fg=TEXT_COLORS[current_color])
        self.underline_button.config(bg=BODY_COLORS[current_color], fg=TEXT_COLORS[current_color])
        self.normal_button.config(bg=BODY_COLORS[current_color], fg=TEXT_COLORS[current_color])

        # We need to update all of the text associated with each tag
        for i in range(self.bold_id):
            self.text_area.tag_configure('bold_' + str(i), foreground=TEXT_COLORS[current_color])
        for i in range(self.italics_id):
            self.text_area.tag_configure('italics_' + str(i), foreground=TEXT_COLORS[current_color])
        for i in range(self.underline_id):
            self.text_area.tag_configure('underline_' + str(i), foreground=TEXT_COLORS[current_color])
        for i in range(self.normal_id):
            self.text_area.tag_configure('normal_' + str(i), foreground=TEXT_COLORS[current_color])

# Create the text area in which the user will be able to type
text_area = Text(root, bg=BODY_COLORS[current_color], font=f'{font_name} {font_size}')

# Create the scroll bar in which the user will be able to scroll
scroll_bar = Scrollbar(root)
root.update() # so that we can get the updated width() of the window
scroll_bar.place(x=root.winfo_width()*TEXT_AREA_WIDTH_FACTOR, y=TITLE_BAR_HEIGHT, relwidth=1-TEXT_AREA_WIDTH_FACTOR, relheight=TEXT_AREA_HEIGHT_FACTOR)

# Place the text modification panel onto the GUI
text_modification = TextModification(root, text_area, TITLE_BAR_HEIGHT+(root.winfo_height()*TEXT_AREA_HEIGHT_FACTOR),
                                     TEXT_AREA_WIDTH_FACTOR, root.winfo_height() - (TITLE_BAR_HEIGHT+(root.winfo_height()*TEXT_AREA_HEIGHT_FACTOR)))

# Call the method responsible for adding in the new title bar
custom_title_bar = CustomTitleBar(root, "Sticky Note", TITLE_BAR_HEIGHT, text_area)

# Positions the text_area where needed according to a y-position
def position_text_area(e=None, y_pos=TITLE_BAR_HEIGHT):
    custom_title_bar.three_dot_frame.place(x=0, y=0, relwidth=1, height=0)
    text_area.place(x=0, y=y_pos, relwidth=TEXT_AREA_WIDTH_FACTOR, relheight=TEXT_AREA_HEIGHT_FACTOR)

# Set the initial position of the text area
position_text_area()

# Make the new title bar
custom_title_bar.create_title_bar()

# Used to get out of three-dot options frame
text_area.bind("<Button-1>", position_text_area)

# Attach the text area to the scroll bar/ configure
text_area.config(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=text_area.yview)

text_modification.create_mod_bar()

# Removes the temporary text of the text area when necessary
def remove_temp_text(e):
    text_area.config(state=NORMAL)
    current_text = text_area.get("1.0", "end-1c")

    # A key was pressed/ something was typed
    if current_text == PLACE_HOLDER_TEXT:
        global default_text_visible
        default_text_visible = False

        text_area.configure(fg=TEXT_COLORS[current_color])
        text_area.delete("1.0", END)

# Adds the place holder text back in when no characters are present
def add_temp_text(e):
    current_text = text_area.get("1.0", "end-1c")
    if len(current_text) <= 1: # one character will be present if this statement is true
        global default_text_visible
        default_text_visible = True

        text_area.configure(fg="darkgray")
        text_area.delete("1.0", END) # remove only character
        text_area.insert(INSERT, PLACE_HOLDER_TEXT)
        text_area.config(state=DISABLED)

# Controls the text displayed when the user has nothing typed in the sticky note
def control_ph_text(text_area):
    text_area.insert(INSERT, PLACE_HOLDER_TEXT)
    text_area.configure(fg="darkgray")
    text_area.config(state=DISABLED)
    text_area.bind("<Key>", remove_temp_text)
    text_area.bind("<BackSpace>", add_temp_text)

# Call the function above to make sure the appropriate text is displayed at all times
control_ph_text(text_area)

# Run continuous loop
root.mainloop()