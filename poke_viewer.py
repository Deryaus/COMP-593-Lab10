from tkinter import *
from tkinter import ttk
import ctypes, os, image_lib, poke_api

# Get the path of the script and its parent directory
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
image_cache_dir = os.path.join(script_dir, 'images')

# Make the image cache folder if it doesn't already exist.
if not os.path.isdir(image_cache_dir):
    os.makedirs(image_cache_dir)

# Create the main window
root = Tk()
root.title("Pokemon Image Viewer")
root.minsize(600, 700)

# Set the window icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('COMP593.PokeImageViewer')
#icon_path = os.path.join(script_dir, 'Poke-Ball.ico')
root.withdraw()
root.iconbitmap(os.path.join(script_dir, 'Poke-Ball.ico'))
root.deiconify()

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Create the Frame
frame = ttk.Frame(root)
frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

# Add the image to the frame
img_poke = PhotoImage(file=os.path.join(script_dir, 'pokeball.png'))
lbl_poke_img = ttk.Label(frame, image=img_poke)
lbl_poke_img.grid(row=0, column=0)

# Add the pokemon names to the combobox
pokemon_name_list = sorted(poke_api.get_pokemon_names())
cbox_poke_names = ttk.Combobox(frame, values=pokemon_name_list, state='readonly')
cbox_poke_names.set("Select A pokemon")
cbox_poke_names.grid(padx=10, pady=10)

def handle_poke_sel(event):
    # get the name of the selected pokemon
    pokemon_name = cbox_poke_names.get()
    global image_path
    # Download and save the artwork for the selected pokemon
    image_path = poke_api.download_pokemon_artwork(pokemon_name, image_cache_dir)
    # Enable the set as desktop button
    if cbox_poke_names.current() != -1:
        btn_set_desktop.config(state=NORMAL)

    # Display the pokemon artwork
    if image_path is not None:
        img_poke['file'] = image_path
# Bind handle event to Combobox        
cbox_poke_names.bind('<<ComboboxSelected>>', handle_poke_sel)

# Create button handle for set as desktop
def handle_set_desktop():
    global image_path
    image_lib.set_desktop_background_image(image_path)

# Create set as destkop button
btn_set_desktop = ttk.Button(frame, text='Set as desktop Image', command=handle_set_desktop, state=DISABLED)
btn_set_desktop.grid(row=2, column=0, padx=10, pady=10)

# loop until window closes
root.mainloop()
