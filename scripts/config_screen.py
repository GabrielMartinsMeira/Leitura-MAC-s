import customtkinter as ctk
import os.path

# Mainpath to the software, to allow work in any directory and OS
MAINPATH = os.path.join(os.path.dirname(os.path.abspath("config_screen.py")))

config_window = None

def on_close_config():
    global config_window
    config_window.destroy()
    config_window = None

def get_infos():
    with open(os.path.join(MAINPATH, "config", "saved_configs.txt"), "r") as f:
        data = [line.strip() for line in f]
        info_list = []
        for items in data:
            info_parts = items.split(":")
            info_list.append(info_parts[1])
        lenght_mac = info_list.pop(0)
        username = info_list.pop(0)
        password = info_list.pop(0)
        return lenght_mac, username, password
    
def get_lenght_mac():
    with open(os.path.join(MAINPATH, "config", "saved_configs.txt"), "r") as f:
        data = [line.strip() for line in f]
        info_list = []
        for items in data:
            info_parts = items.split(":")
            info_list.append(info_parts[1])
        lenght_mac = info_list.pop(0)
        return lenght_mac

def open_config_window():
    global config_window
    if config_window is None or not config_window.winfo_exists():
        # Configuration on config_window
        config_window = ctk.CTk()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        config_window.title("Configurações")
        config_window.geometry("600x400") 
        config_window.configure(fg_color='#433A3A')
        config_window.resizable(False, False)

        # CTK Variables
        lenght_mac_response = ctk.StringVar()

        # Functions
        def change_lenght_macs():
            try:
                if isinstance(int(lenght_mac_entry.get()), int) == True:
                    lenght_mac, username, password = get_infos()
                    print("TRUE")
                    lenght_mac_response.set("Largura modificada")
                    with open(os.path.join(MAINPATH, "config", "saved_configs.txt"), "w") as f:
                        lenght_mac = lenght_mac_entry.get()
                        f.write("TOTAL_MACS:" + lenght_mac + "\nUSER:" + username + "\nPASS:" + password)
                else:
                    print("FALSE")
                    lenght_mac_response.set("Escreva um numero")
            except Exception as e:
                lenght_mac_response.set("Entrada Invalida, escreva um número!")
                print("Error ", e)
        # Fixed Labels
        lenght_mac_label = ctk.CTkLabel(config_window, textvariable=lenght_mac_response)
        lenght_mac_label.place(x=100, y=100)

        # Entrys
        lenght_mac_entry = ctk.CTkEntry(config_window, placeholder_text="Insira Largura")
        lenght_mac_entry.place(x=20, y=20)

        # Buttons
        change_lenght_mac = ctk.CTkButton(config_window, text="Mudar Quantidade MAC", command=change_lenght_macs)
        change_lenght_mac.place(x=20, y=60)

        config_window.protocol("WM_DELETE_WINDOW", on_close_config)
        config_window.mainloop()
    else: 
        config_window.lift()