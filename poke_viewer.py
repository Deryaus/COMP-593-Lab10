import poke_api

from tkinter import *
from tkinter import ttk
import ctypes, os


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
root.minsize(500, 500)
root.iconbitmap('Poke-Ball.ico')
# TODO: Put code here


# Set the window icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('COMP593.PokeImageViewer')
icon_path = os.path.join(script_dir, 'Poke-Ball.ico')
root.iconbitmap(icon_path)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


# Create the Frame
frame = ttk.Frame(root)
frame.grid(row=0, column=0, padx=(10), pady=10, sticky=NSEW)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)


img_poke = PhotoImage(file='pokeball.png')
lbl_poke_img = ttk.Label(frame, image=img_poke)
lbl_poke_img.grid(row=0, column=0)

pokemon_name_list = poke_api.get_pokemon_names()
cbox_poke_names = ttk.Combobox(frame, values=pokemon_name_list, state='readonly')
cbox_poke_names.set("Select A pokemon")
cbox_poke_names.grid(padx=10, pady=10)


def handle_poke_sel(event):
    # get the name of the selected pokemon
    pokemon_name = cbox_poke_names.get()
    # Download and save the artwork for the selected pokemon
    image_path = poke_api.download_pokemon_artwork(pokemon_name, image_cache_dir )

    # Display the pokemon artwork
    if image_path is not None:
        img_poke['file'] = image_path

    
cbox_poke_names.bind('<<ComboboxSelected>>', handle_poke_sel)

btn_set_desktop = ttk.Button(frame, text='Set as desktop Image')
btn_set_desktop.grid(row=2, column=0, padx=10, pady=10)
















root.mainloop()
