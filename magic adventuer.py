import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pyglet
import os
from PIL import Image, ImageTk

# ---------------------- SET UP -------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ROOMS = {
    "Spawn Point": {
        "title": "Spawn Point",
        "desc": "You seem to spawn in this place, you don't remember anything of the past or the outside world...",
        "options": [
            ("Door 1 to hallway", "Hallway"),
                    ],
        "items": [],
    },
    "Magic Room": {
        "title": "Magic Room",
        "desc": "A room full of magic and chaos, the radiation in there is unstable..",
        "options": [
            ("Door 1 to hallway", "Hallway"),
            ("Door 2 to closet", "Closet"),
        ],
        "items": [
            {"name": "Wand", "image" : os.path.join(BASE_DIR, "wand.jpg")},
            {"name": "Gems", "image": os.path.join(BASE_DIR, "gems.jpg")}, {"name": "Brewing Stand", "image": os.path.join(BASE_DIR, "brew")}, {"name": "Hint #3", "image": os.path.join(BASE_DIR, "hint.png")}],
    },
    "Closet": {
        "title": "Closet",
        "desc": "Just a boring closet",
        "options": [
            ("Go back to Magic Room", "Magic Room"),
        ],
        "items": [
            {"name": "Gems", "image": os.path.join(BASE_DIR, "gems.jpg")}, {"name": "Hint #2", "image": os.path.join(BASE_DIR, "hint.png")}
        ]

    },
    "Hallway": {
        "title": "The Halls",
        "desc": "A long, foggy hallway, with sparkles everywhere",
        "options": [
                ("Go to magic room", "Magic Room"), ("Go to garden", "Garden"), 
                ("Go to escape door", "Escape door")
        ],
        "items": [
            {"name": "Hint", "image": os.path.join(BASE_DIR, "hint.png")}
        ]
    },
    "Storage": {
        "title": "Storage room",
        "desc": "A small room, filled with valueble items.",
        "options": [
            ("Go to garden", "Garden")
            ],
        "items": [
    {"name": "Gems", "image": os.path.join(BASE_DIR, "gems.jpg")}
],
    },
    "Garden": {
        "title": "The Garden of Surprise",
        "desc": "A garden filled with perculiar plants, some are good, others are not..",
        "options": [("Door 1 to hallway", "Hallway"), ("Door 2 to storage", "Storage")],
        "items": [
            {"name": "Gems", "image": os.path.join(BASE_DIR, "gems.jpg")}, {"name": "Fluorescent plant seeds", "image": os.path.join(BASE_DIR, "fluor.png")}, 
            {"name" : "Ochre plant seeds", "image": os.path.join(BASE_DIR, "ochre.png")},{"name": "Luminescent plant seeds", "image": os.path.join(BASE_DIR, "lum.jpg")}, 
            {"name": "watering can", "image": os.path.join(BASE_DIR, "wateringcan.jpg")}, {"name": "Hint #4", "image": os.path.join(BASE_DIR, "hint.png")}
            
        ]
    },
    "Escape door": {
        "title": "The escape door",
        "desc": "The door to escape, but it's locked. Find the combination of plants using the hints around the map..",
        "options": [("Go back to hallway", "Hallway"), ("Use keypad", "Keypad")],
        "items": [],
    },
    "Keypad": {
        "title": "Keypad",
        "desc": "Enter the code from the hints around the map.",
        "options": [("Go back to exit door", "Escape door")],
        "items": [],
    },
    "Outside world": {
        "title": "Outside World",
        "desc": "You've done it, you're free!",
        "options": {},
        "items": [],
    },
}

current_room = "Spawn Point"
satchel = []
taken = set()

# berkshire
font_path = os.path.join(os.path.dirname(__file__), 'BerkshireSwash-Regular.ttf')
pyglet.font.add_file(str(font_path))
custom_font_title = "Berkshire Swash"

# waterbrush
desc_font = os.path.join(os.path.dirname(__file__), 'BerkshireSwash-Regular.ttf')
pyglet.font.add_file(str(desc_font))
custom_font_desc = "Water Brush"

pyglet.options["win32_gdi_font"] = True



# ------------------------ Game Logic --------------------------------
def update_inventory_ui():
    if satchel:
        inv_label.config(text="Satchel: " + ", ".join(satchel))
    else:
        inv_label.config(text="Satchel: (empty)")

def take_item_if_present(room_id):
    if ROOMS[room_id]["items"] is None:
        return

    for item in ROOMS[room_id]["items"]:
        name = item["name"]
        if name not in satchel:
            satchel.append(name)
            update_inventory_ui()

def clear(frame):
    for w in frame.winfo_children():
        w.destroy()


# def show_room(room_id):
#     global current_room
#     current_room=room_id

#     clear(item_label)
#     clear(choices_frame)
#     clear(inv_label)

#     render_items(ROOMS[current_room])

#     room = ROOMS[room_id]
#     title_label.config(text=room["title"])
#     desc_label.config(text=room["desc"], font=(custom_font_desc, 25))

#     for b in choices_frame.winfo_children():
#         b.destroy()

#     for label, next_room in room["options"]:
#         btn = tk.Button(
#             choices_frame,
#             text=label,
#             font=(custom_font_title, 15),
#             command=lambda r= next_room: show_room(r), # lambda shows function in one line
#             width = 32
#         )
#         btn.pack(pady=4)

#     if not room["items"] is None:
#         for item in room["items"]:
#             btn = tk.Button(
#                 choices_frame, text=item["name"], font=("Water Brush", 13),command=lambda r=current_room: take_item_if_present(r)

#             )
#         take_item_if_present(current_room)

def show_room(room_id):
    global current_room
    current_room = room_id

    # Clear the UI components before rendering the new room
    clear(item_label)         # Clear items label
    clear(choices_frame)      # Clear choices buttons
    clear(inv_label)          # Clear inventory label

    # Get the room data from the ROOMS dictionary
    room = ROOMS[room_id]

    # Update room title and description
    title_label.config(text=room["title"])
    desc_label.config(text=room["desc"], font=(custom_font_desc, 25))

    # Render the room options (buttons) before rendering items
    for b in choices_frame.winfo_children():
        b.destroy()  # Destroy previous buttons (if any)

    # Create new option buttons for the current room
    for label, next_room in room["options"]:
        btn = tk.Button(
            choices_frame,
            text=label,
            font=(custom_font_title, 15),
            command=lambda r=next_room: show_room(r),  # Command for navigating
            width=32
        )
        btn.pack(pady=4)

    # Render the items for the current room after options
    render_items(room)

def load_image(path, size=(72, 72)):
    try:
        img = Image.open(path)
        img = img.resize(size, Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)
        return tk_img
    except Exception:
        [ROOMS][current_room]["items"] = None
        return None

    
def pick_up(item_label):
    taken.add(item_label)
    satchel.append(item_label)
    show_room()

# def render_items(room):
#     # item_ids = room.get("items", [])

#     visible = [i for i in room.get("items", []) if i not in taken]

#     if not visible:
#         tk.Label(item_label, text="Nothing to see here.").pack(
#             anchor="center", padx=10, pady=10
#         )
#         return
    
#     row = tk.Frame(item_label).pack(
#         anchor="center", padx=10, pady=10  # anchor positions the text either north east south or west etc.
#     )

#     for i in visible:
#         img = load_image(i["image"])

#         if img:
#             b = tk.Button(
#                 row,
#                 image=img,
#                 command=lambda iid=visible[i]: pick_up(item_label),
#                 cursor="hand2",  # mouse
#                 bd=0,
#             )
#         else:
#             b = tk.Button(
#                 row,
#                 text=visible,
#                 command=lambda iid=visible[i]: pick_up(item_label),
#                 cursor="hand2",
#             )

#         b.pack(side="left", padx=8)

def render_items(room):
    # Get the list of items in the room, excluding those that are already taken
    visible = [i for i in room.get("items", []) if i["name"] not in taken]

    if not visible:
        # If no visible items, show a label saying "Nothing to see here."
        tk.Label(item_label, text="Nothing to see here.").pack(
            anchor="center", padx=10, pady=10
        )
        return
    
    # Create a frame to hold the item buttons
    row = tk.Frame(item_label)
    row.pack(anchor="center", padx=10, pady=10)

    # Loop through all visible items and create buttons for them
    for i in visible:
        img = load_image(i["image"])  # Use the image associated with the item

        if img:
            # If the image is available, create a button with the image
            b = tk.Button(
                row,
                image=img,
                command=lambda iid=i["name"]: pick_up(iid),  # Use the item's name in the lambda
                cursor="hand2",  # Change mouse cursor to hand
                bd=0,
            )
        else:
            # If no image is available, create a button with just the item name
            b = tk.Button(
                row,
                text=i["name"],  # Use the item's name as text on the button
                command=lambda iid=i["name"]: pick_up(iid),  # Use the item's name in the lambda
                cursor="hand2",
            )

        b.pack(side="left", padx=8)  # Pack the button inside the row

# def render_items(room):
#     # Check if the room has items and that 'taken' is a valid set
#     if room.get("items") is None:
#         return

#     visible = [i for i in room.get("items", []) if i["name"] not in taken]

#     if not visible:
#         tk.Label(item_label, text="Nothing to see here.").pack(
#             anchor="center", padx=10, pady=10
#         )
#         return

#     row = tk.Frame(item_label)
#     row.pack(anchor="center", padx=10, pady=10)

#     for item in visible:
#         img = load_image(item["image"])

#         if img:
#             b = tk.Button(
#                 row,
#                 image=img,
#                 command=lambda iid=item["name"]: pick_up(iid),
#                 cursor="hand2",  # mouse pointer change
#                 bd=0,
#             )
#         else:
#             b = tk.Button(
#                 row,
#                 text=item["name"],
#                 command=lambda iid=item["name"]: pick_up(iid),
#                 cursor="hand2",
#             )

#         b.pack(side="left", padx=8)


    
# def restart_game():
#     global current_room, satchel
#     current_room = "Spawn Point"

#     satchel = []

#     update_inventory_ui
#     show_room(current_room)

   

# ---------------------------------------------------- UI ---------------------------------------------

screen = tk.Tk()
screen.title('Magic Mansion of Surprise')
screen.geometry("1000x600")

exitbutton = tk.Button(text="exit game", font=("Berkshire Swash", 13), command=screen.destroy)
exitbutton.place(x=500, y=100)
exitbutton.pack(pady=3)

# restartbutton = tk.Button(text="restart", font=("Berkshire Swash", 13), command=screen.restart_game)
# restartbutton.pack(pady=3)



# pixel_font = tkfont.Font(family="Berk", size=20)
title_label = tk.Label(screen, text = "Spawn Point", font=(custom_font_title, 20))
title_label.pack(pady=20)

desc_label = tk.Label(
    screen,
    text="You seem to spawn in this place, you don't remember anything of the past or the outside world...",
    font=("Water Brush", 15),
    wraplength=600,
    justify="left",
)
desc_label.pack(pady=16)

inv_label = tk.LabelFrame(screen, text="Satchel: (empty)", font=("Berkshire Swash", 11))
inv_label.pack(pady=(0, 10))

item_label = tk.LabelFrame(screen, text="Items found in room", font=("Berkshire Swash", 11))
item_label.pack(pady=(0, 10))


choices_frame = tk.Frame(screen)
choices_frame.pack(pady= 8)

# function calls
show_room(current_room)
update_inventory_ui()

# def go_hallway():
#     title_label.config(text="The Halls")
#     desc_label.config(text="A long, foggy hallway, with sparkles everywhere")

# btn = tk.Button(screen, text="Go to hallway", command=go_hallway, width= 32)
# btn.pack(pady=6)

screen.mainloop()

