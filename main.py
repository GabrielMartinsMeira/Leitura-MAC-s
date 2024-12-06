import customtkinter as ctk
import nest_asyncio
import threading
nest_asyncio.apply()
import asyncio
from scripts.save_mac import * 

# class App(ctk.CTk):

#     def __init__(self, loop, interval=1/120):
#         super().__init__()
#         self.loop = loop
#         self.protocol("WM_DELETE_WINDOW", self.close)
#         self.tasks = []
#         self.tasks.append(loop.create_task(self.rotator(1/60, 2)))
#         self.tasks.append(loop.create_task(self.updater(interval)))

#     async def rotator(self, interval, d_per_tick):
#         self._set_appearance_mode("dark")
#         canvas = ctk.CTkCanvas(self, height=600, width=600)
#         canvas.pack()
#         deg = 0
#         color = 'black'
#         while await asyncio.sleep(interval, True):
#             canvas.itemconfigure(extent=deg, fill=color)

#     async def updater(self, interval):
#         while True:
#             self.update()
#             await asyncio.sleep(interval)
        
#     def close(self):
#         for task in self.tasks:
#             task.cancel()
#         self.loop.stop()
#         self.destroy()
    
# Configuration for main window 
def main(async_loop):
    main_window = ctk.CTk()
    ctk.set_appearance_mode("dark")
    main_window.title("Leitura MAC's")
    main_window.geometry("600x500") 
    main_window.configure(fg_color="#433A3A")
    main_window.resizable(False, False)

    # Variables
    

    # Text Varibles
    macs_frame = ctk.StringVar()
    products_number = ctk.StringVar()
    boxes_number = ctk.StringVar()

    # Frames
    mac_frame = ctk.CTkFrame(main_window, width= 560, height= 300, fg_color="#B37B0C", corner_radius=15)
    mac_frame.place(x=20, y=20)
    
    # Fixed Label's
    mac_label = ctk.CTkLabel(main_window, text="Insira o MAC")
    mac_label.place(x=20, y=320)

    mac_label_frame = ctk.CTkLabel(mac_frame, text="MAC's", font=("Roboto", 24))
    mac_label_frame.place(x=240, y=20)

    boxes_label_frame = ctk.CTkLabel(mac_frame, text="CAIXA(S):", font=("Roboto", 24))
    boxes_label_frame.place(x=20, y=20)

    products_label_frame = ctk.CTkLabel(mac_frame, text="Produto(s):", font=("Roboto", 24))
    products_label_frame.place(x=380, y=20)

    # Output Label's

    mac_response_frame = ctk.CTkLabel(mac_frame, textvariable=macs_frame, font=("Roboto", 18))
    mac_response_frame.place(x=20, y=50)
    
    boxes_response_frame = ctk.CTkLabel(mac_frame, textvariable=boxes_number, font=("Roboto", 24))
    boxes_response_frame.place(x=40, y=20)

    products_response_frame = ctk.CTkLabel(mac_frame, textvariable=products_number, font=("Roboto", 24))
    products_response_frame.place(x=510, y=20)

    # Info Entrys
    mac_entry = ctk.CTkEntry(main_window, placeholder_text="mac")
    mac_entry.place(x=20, y=360)

    # Window Buttons 
    button = ctk.CTkButton(main_window, text="")
    button.place(x=20,y=400)
    print(mac_quantity())
    products_number.set(mac_quantity())
    threading.Thread(target=start_async_loop, args=[mac_entry, macs_frame, boxes_number, products_number]).start()
    main_window.mainloop()

# Functions

def is_first_mac(mac_counter):
    return True if mac_counter == 0 else False

async def search_mac(mac_entry, macs_frame, boxes_number, products_number):
    while True:
        try:
            mac_counter = int(products_number.get())
            print(mac_entry.get())
            mac = mac_entry.get()
            first_mac = is_first_mac(mac_counter)
            response = write_mac(mac)
            if response == "OK":
                first_mac == False
                mac_counter += 1
                products_number.set(str(mac_counter))
                macs_frame.set(mac)
            else:
                mac_entry.set("")
            macs_frame.set(mac)
            print(response)
            await asyncio.sleep(2)
        except Exception as e:
            print("Error ", e)
            break

def start_async_loop(mac, macs_frame, boxes_number, products_number):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(search_mac(mac, macs_frame, boxes_number, products_number))

loop = asyncio.get_event_loop()
main(loop)