import customtkinter as ctk
import threading
import asyncio
from scripts.save_mac import * 

# List for MAC labels
labels = []

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
    mac_response_frame.place(x=140, y=400)
    
    boxes_response_frame = ctk.CTkLabel(main_window, textvariable=boxes_number, font=("Roboto", 24))
    boxes_response_frame.place(x=40, y=20)

    products_response_frame = ctk.CTkLabel(main_window, textvariable=products_number, font=("Roboto", 24))
    products_response_frame.place(x=510, y=20)

    # Info Entrys
    mac_entry = ctk.CTkEntry(main_window, placeholder_text="INSIRA O MAC")
    mac_entry.place(x=210, y=365)

    # Program Init
    for i in range(10):
        lbl = ctk.CTkLabel(mac_frame, text=i)
        lbl.pack(pady=0, padx=0)
        labels.append(lbl)
    #print(labels)
    if mac_quantity() == None:
        is_first_mac = True
        products_number.set("0")
        pass
    else:
        is_first_mac = False
        write_10_macs(mac_frame)
        products_number.set(mac_quantity())
    threading.Thread(target=start_async_loop, args=[mac_entry, macs_frame, boxes_number, products_number, is_first_mac, mac_frame]).start()
    main_window.mainloop()

# Functions

def write_10_macs(mac_frame):
    items = write_mac()
    for i in range(len(items)):
        labels[i].configure(text=items[i])
    # for item in items:
    #     ctk.CTkLabel(mac_frame, text=item.upper()).pack(pady=0, padx=0)

# Async function to search mac entry in X seconds
async def search_mac(mac_entry, macs_frame, boxes_number, products_number, is_first_mac, mac_frame):
    while True:
        try:
            # Get the mac entry
            mac = mac_entry.get()
            # Checks if mac entry have some text
            if mac:
                #print("MAC LIDO")
                # Tries to save the mac on the txt mac file
                response = save_mac(mac, is_first_mac)
                #print(response)
                # Ckecks if the MAC was written and returned "OK"
                if response == "OK":
                    is_first_mac = False
                    # Update the number of products
                    products_number.set(mac_quantity())
                    # Add the mac to the frame and to the last 10 macs file
                    write_10_macs(mac_frame)

                else: 
                    #print("MAC error")
                    macs_frame.set(response)
                await asyncio.sleep(1)
            await asyncio.sleep(1)
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