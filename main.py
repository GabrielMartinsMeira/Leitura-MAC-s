import customtkinter as ctk
import threading
import asyncio
import os.path
from PIL import Image
from time import sleep
from scripts.save_mac import mac_quantity, clean_last_10_macs, write_last_10_macs, save_mac, get_path
from scripts.config_screen import open_config_window, get_lenght_mac

# Mainpath to the software, to allow work in any directory and OS
MAINPATH = os.path.join(os.path.dirname(os.path.abspath("main.py")))

# List for MAC labels
labels = []

# Images
box_icon = ctk.CTkImage(Image.open(os.path.join(MAINPATH, "images", "box_icon.png")), size=(35, 35))
router_icon = ctk.CTkImage(Image.open(os.path.join(MAINPATH, "images", "router_icon.png")), size=(35, 35))
config_icon = ctk.CTkImage(Image.open(os.path.join(MAINPATH, "images", "engrenagem_icon.png")), size=(35, 35))

# The main function
def main(async_loop):
    global main_window
    lenght_mac = get_lenght_mac()
    # Configuration for main window 
    main_window = ctk.CTk()
    ctk.set_appearance_mode("dark")
    main_window.title("Leitura MAC's")
    main_window.geometry("600x500") 
    main_window.configure(fg_color="#433A3A")
    main_window.resizable(False, False)
    
    # CTK Varibles
    mac_label = ctk.StringVar()
    products_number = ctk.StringVar()
    boxes_number = ctk.StringVar()

    # Frames
    mac_frame = ctk.CTkFrame(main_window, width= 300, height= 300, fg_color="#003F58", corner_radius=15)
    mac_frame.place(x=130, y=60)
    mac_frame.propagate(False)
    
    # Fixed Label's
    mac_label_frame = ctk.CTkLabel(main_window, text="MAC's", font=("Roboto", 24))
    mac_label_frame.place(x=240, y=20)

    # Output Label's
    mac_response_frame = ctk.CTkLabel(main_window, textvariable=mac_label, font=("Roboto", 18))
    mac_response_frame.place(x=215, y=400)
    
    boxes_response_frame = ctk.CTkLabel(main_window, textvariable=boxes_number, font=("Roboto", 24))
    boxes_response_frame.place(x=60, y=20)

    products_response_frame = ctk.CTkLabel(main_window, textvariable=products_number, font=("Roboto", 24))
    products_response_frame.place(x=510, y=20)

    # Info Entrys
    mac_entry = ctk.CTkEntry(main_window, placeholder_text="INSIRA O MAC")
    mac_entry.place(x=210, y=370)

    # Images
    box_icon_image = ctk.CTkLabel(main_window, text="", image=box_icon)
    box_icon_image.place(x=20, y=20)

    router_icon_image = ctk.CTkLabel(main_window, text="", image=router_icon)
    router_icon_image.place(x=460, y=16)

    # Buttons
    open_last_txt = ctk.CTkButton(main_window, text="ABRIR ARQUIVO MACS", command=open_last_mac_file)
    open_last_txt.place(x=210, y=460)
    
    open_config = ctk.CTkButton(main_window, text="", image=config_icon, height=10, width=20, border_width=0, fg_color="#433A3A", bg_color="#433A3A", command=open_config_window)
    open_config.place(x=0, y=460)

    # Program Init
    # Create the labels on the frame for the last 10 macs
    for lbl in range(10):
        lbl = ctk.CTkLabel(mac_frame, text="")
        lbl.pack(pady=0, padx=0)
        labels.append(lbl)
    # Checks if there no macs written
    if mac_quantity() == None:
        is_first_mac = True
        clean_last_10_macs()
        products_number.set("0")
        boxes_number.set("0")
        pass
    else:
        is_first_mac = False
        # Writes the number of boxes already made
        boxes_number.set(check_boxes())
        # Writes the last 10 macs, if theres any macs
        write_10_macs(mac_frame, mac_label, lenght_mac)
        # Writes the number of products already made
        products_number.set(mac_quantity())
    # Start the thread to the async loop and pass all vars
    threading.Thread(target=start_async_loop, args=[mac_entry, mac_label, boxes_number, products_number, is_first_mac, mac_frame]).start()
    main_window.protocol("WM_DELETE_WINDOW", close_window)
    main_window.mainloop()

# Functions
def close_window():
    global main_window
    main_window.destroy()
    main_window = None 
    os._exit(0)

def open_last_mac_file():
    # A small fix to get path, the function get_path() return 2 var, but we only need one of these vars, so whe dump the other
    dump_macs, path = get_path()
    # Open the last txt mac file
    os.startfile(path)

# Function that write the 10 macs on a frame in the main window
def write_10_macs(mac_frame, mac_label, lenght_mac):
    # Get the macs from the last_10_macs file and put them on a list
    macs = write_last_10_macs()
    # Checks if the lenght of the macs is equal or greater than 10 
    if len(macs) >= 10:
        # Write the last MAC
        labels[9].configure(text="10 - " + macs[9])
        check_max_response = check_max_macs(mac_frame, mac_label, lenght_mac)
        if check_max_response == False:
            # Change the frame color to green 
            mac_frame.configure(fg_color="#1A5E00")
            # Writes "CAIXA FINALIZADA"  
            mac_label.set("CAIXA FINALIZADA")
            sleep(2)
            # Clean the previous label
            clean_message(mac_label) 
            # Set back the deafault color of the frame 
            mac_frame.configure(fg_color="#003F58")
        # Clean all MACS labels
        for i in range(len(macs)):
            labels[i].configure(text="")
        # Return the macs list
        return macs
    else:
        # Write the macs located on the last_10_macs file
        for i in range(len(macs)):
            labels[i].configure(text=str(i+1) + " - " + macs[i])
        # Return the macs list
        check_max_macs(mac_frame, mac_label, lenght_mac)
        return macs

def check_max_macs(mac_frame, mac_label, lenght_mac):
    if mac_quantity() >= int(lenght_mac):
            mac_label.set("Pallet Finalizado")
            mac_frame.configure(fg_color="#1BC900")
            sleep(2)
            clean_message(mac_label)
            mac_frame.configure(fg_color="#003F58")
            return True
    else:
        return False

# Function to check the total of boxes
def check_boxes():
    # Get all the macs written
    all_mac = mac_quantity()
    # Return the number of boxes doing a integer division of all the macs by the number of products in each box (10)
    return int(all_mac) // 10

# Function to clean any label
def clean_message(text):
    sleep(1)
    text.set("")

# Async function to search mac entry in X seconds
async def search_mac(mac_entry, mac_label, boxes_number, products_number, is_first_mac, mac_frame):
    while True:
        try:
            lenght_mac = get_lenght_mac()
            # A quick fix for mac reading problem when has no input
            while mac_entry.get() == "":
                await asyncio.sleep(0.2)
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
                    # Update the number of products
                    products_number.set(mac_quantity())
                    # Update the number of boxes
                    boxes_number.set(check_boxes())
                    # Add the mac to the frame and to the last 10 macs file
                    macs = write_10_macs(mac_frame, mac_label, lenght_mac)
                    # A quick fix to a response problem when finished all 10 macs
                    if len(macs) >= 10:
                        pass
                    else:
                        # Set the response in the screen
                        mac_label.set(response)
                    # Delete the text in the MAC entry
                    mac_entry.delete(0, ctk.END)
                    # Clean the response after 1 seconds
                    clean_message(mac_label)
                    
                else: 
                    mac_frame.configure(fg_color="#910505")
                    # Set the response in the screen
                    mac_label.set(response)
                    # Delete the text in the MAC entry
                    mac_entry.delete(0, ctk.END)
                    # Clean the response after 1 second
                    clean_message(mac_label)
                    mac_frame.configure(fg_color="#003F58")
                await asyncio.sleep(0.2)
        except Exception as e:
            print("Error Search Mac: ", e)
            #loop.stop()
            break

# Function to start the async function search_mac
def start_async_loop(mac, mac_label, boxes_number, products_number, is_first_mac, mac_frame):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(search_mac(mac, mac_label, boxes_number, products_number, is_first_mac, mac_frame))

loop = asyncio.get_event_loop()
main(loop)