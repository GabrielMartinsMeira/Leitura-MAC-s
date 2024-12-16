import customtkinter as ctk
import threading
import asyncio
from PIL import Image
from time import sleep
from scripts.save_mac import * 
from scripts.convert_csv import convert_mac

# List for MAC labels
labels = []

# Images

#box_icon = ctk.CTkImage(Image.open(r"\images\box_icon"), size=(35, 35))

# Configuration for main window 
def main(async_loop):
    main_window = ctk.CTk()
    ctk.set_appearance_mode("dark")
    main_window.title("Leitura MAC's")
    main_window.geometry("600x500") 
    main_window.configure(fg_color="#433A3A")
    main_window.resizable(False, False)
    
    # Text Varibles
    macs_frame = ctk.StringVar()
    products_number = ctk.StringVar()
    boxes_number = ctk.StringVar()
    total_macs = ctk.StringVar()

    # Frames
    mac_frame = ctk.CTkFrame(main_window, width= 300, height= 300, fg_color="#003F58", corner_radius=15)
    mac_frame.place(x=130, y=60)
    mac_frame.propagate(False)
    
    # Fixed Label's
    mac_label_frame = ctk.CTkLabel(main_window, text="MAC's", font=("Roboto", 24))
    mac_label_frame.place(x=240, y=20)

    boxes_label_frame = ctk.CTkLabel(main_window, text="CAIXA(S):", font=("Roboto", 24))
    boxes_label_frame.place(x=20, y=20)

    products_label_frame = ctk.CTkLabel(main_window, text="Produto(s):", font=("Roboto", 24))
    products_label_frame.place(x=380, y=20)

    # Output Label's
    mac_response_frame = ctk.CTkLabel(main_window, textvariable=macs_frame, font=("Roboto", 18), anchor="center")
    mac_response_frame.place(x=215, y=400)
    
    boxes_response_frame = ctk.CTkLabel(main_window, textvariable=boxes_number, font=("Roboto", 24))
    boxes_response_frame.place(x=140, y=20)

    products_response_frame = ctk.CTkLabel(main_window, textvariable=products_number, font=("Roboto", 24))
    products_response_frame.place(x=510, y=20)

    # Info Entrys
    mac_entry = ctk.CTkEntry(main_window, placeholder_text="INSIRA O MAC")
    mac_entry.place(x=210, y=365)

    # Program Init
    for i in range(10):
        lbl = ctk.CTkLabel(mac_frame, text="")
        lbl.pack(pady=0, padx=0)
        labels.append(lbl)
    if mac_quantity() == None:
        is_first_mac = True
        products_number.set("0")
        boxes_number.set("0")
        pass
    else:
        is_first_mac = False
        boxes_number.set(check_boxes())
        write_10_macs(mac_frame, macs_frame)
        products_number.set(mac_quantity())
    threading.Thread(target=start_async_loop, args=[mac_entry, macs_frame, boxes_number, products_number, is_first_mac, mac_frame]).start()
    main_window.mainloop()

# Functions

def write_10_macs(mac_frame, mac_label):
    items = write_mac()
    if len(items) == 10:
        labels[9].configure(text="10 - " + items[9])
        mac_frame.configure(fg_color="#1A5E00")
        mac_label.set("CAIXA FINALIZADA")
        clean_message(mac_label)
        sleep(2)
        for i in range(len(items)):
            labels[i].configure(text="")
        mac_frame.configure(fg_color="#003F58")
    else:
        for i in range(len(items)):
            labels[i].configure(text=str(i+1) + " - " + items[i])

def check_boxes():
    check_mac = mac_quantity()
    return int(check_mac) // 10

def clean_message(text):
    sleep(1)
    text.set("")

# Async function to search mac entry in X seconds
async def search_mac(mac_entry, macs_frame, boxes_number, products_number, is_first_mac, mac_frame):
    while True:
        try:
            # A small fix for mac reading
            while mac_entry.get() == "":
                await asyncio.sleep(0.1)
            await asyncio.sleep(0.5)
            # Get the mac entry
            mac = mac_entry.get()
            # Checks if mac entry have some text
            if mac:
                # Tries to save the mac on the txt mac file
                response = save_mac(mac.strip(), is_first_mac)
                # Ckecks if the MAC was written and returned "OK"
                if response == "MAC ASSOCIADO!":
                    is_first_mac = False
                    if mac_quantity() >= 400:
                        convert_mac()
                    # Update the number of products
                    products_number.set(mac_quantity())
                    # Update the number of boxes
                    boxes_number.set(check_boxes())
                    # Add the mac to the frame and to the last 10 macs file
                    write_10_macs(mac_frame, macs_frame)
                    # Set the response in the screen
                    macs_frame.set(response)
                    # Clean the response after 2 seconds
                    clean_message(macs_frame)
                    # Delete the text in the MAC entry
                    mac_entry.delete(0, ctk.END)
                else: 
                    # Set the response in the screen
                    macs_frame.set(response)
                    # Clean the response after 2 second
                    clean_message(macs_frame)
                    # Delete the text in the MAC entry
                    mac_entry.delete(0, ctk.END)
                await asyncio.sleep(0.1)
        except Exception as e:
            print("Error Search Mac: ", e)
            break

# Function to start the async function search_mac
def start_async_loop(mac, macs_frame, boxes_number, products_number, is_first_mac, mac_frame):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(search_mac(mac, macs_frame, boxes_number, products_number, is_first_mac, mac_frame))

loop = asyncio.get_event_loop()
main(loop)