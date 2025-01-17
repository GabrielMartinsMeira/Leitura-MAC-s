from datetime import date
import os.path

# Mainpath to the software, to allow work in any directory and OS
MAINPATH = os.path.join(os.path.dirname(os.path.abspath("save_mac.py")))

# Function to write the txt with MACS
def save_mac(mac, is_first_mac): 
    try:
        lenght_mac = get_lenght_mac()
        # Verify if the MAC input has 12 characters
        if len(mac) == 12:
            # If is the first MAC, it will create a new txt file with the current date
            if is_first_mac == True: 
                new_mac_file()
            # Get the path to the last txt mac file
            path = get_path(); items = get_macs()
            # Check if the new MAC isn't in the last txt mac file 
            if not mac in items:
                if len(items) >= int(lenght_mac):
                    from scripts.convert_csv import convert_mac
                    convert_mac()
                    new_mac_file()
                    path = get_path()
                    items = get_macs()
                # Add the mac to the list
                items.append(mac)
                # Write all the macs in the list into the txt mac file
                with open(path, "w") as mac_file:
                    mac_file.write("\n".join(items))
                last_10_macs(mac)
                return "MAC Associado" 
            else:
                return "MAC Repetido"

        else:
            return "Leitura Incorreta\n Não é um MAC valido"
    except Exception as e:
        print("Error ", e)

# Get all the data from the config save txt file and return it 
def get_infos():
    with open(os.path.join(MAINPATH, "config", "saved_configs.txt"), "r") as config_file:
        data = [line.strip() for line in config_file]
        info_list = []
        for items in data:
            info_parts = items.split(":")
            info_list.append(info_parts[1])
        lenght_mac = info_list.pop(0)
        username = info_list.pop(0)
        password = info_list.pop(0)
        return lenght_mac, username, password

# Get the max lenght of the macs in the config txt file and return it 
def get_lenght_mac():
    with open(os.path.join(MAINPATH, "config", "saved_configs.txt"), "r") as config_file:
        data = [line.strip() for line in config_file]
        info_list = []
        for items in data:
            info_parts = items.split(":")
            info_list.append(info_parts[1])
        lenght_mac = info_list.pop(0)
        return lenght_mac

# Function to create a new mac file and set it as the last mac file
def new_mac_file():
    # Create the variabla txt with the current date 
    mac_file = "MACS " + date.today().strftime("%d-%m-%y") + ".txt"
    if os.path.exists(os.path.join(MAINPATH, "macs", mac_file)) == True:
        with open(os.path.join(MAINPATH, "config", "counter.txt"), "r") as reader_counter_file:
            counter = reader_counter_file.read()
        int_counter = int(counter) + 1
        mac_file = "MACS " + date.today().strftime("%d-%m-%y") + " " + str(int_counter) + ".txt"
        with open(os.path.join(MAINPATH, "config", "counter.txt"), "w") as writer_counter_file:
            writer_counter_file.write(str(int_counter))
    else:
        with open(os.path.join(MAINPATH, "config", "counter.txt"), "w") as writer_counter_file:
            writer_counter_file.write("0")
            
    # Create the txt file
    open(os.path.join(MAINPATH, "macs", mac_file), "x")

    # Write it as the last MAC file
    with open(os.path.join(MAINPATH, "macs", "last_mac_file.txt"), "w") as writer_mac_file:
        writer_mac_file.write(mac_file)

# Function to get the path of the last mac file and the macs in this file 
def get_path():
    try:
        with open(os.path.join(MAINPATH, "macs", "last_mac_file.txt"), "r") as reader_mac_file:
            if not reader_mac_file.read(1):
                return "Não há arquivos para abrir"
            reader_mac_file.seek(0)
            last_mac_file = reader_mac_file.read()
            return os.path.join(MAINPATH, "macs", last_mac_file)
        
    except Exception as e:
        print("Erro ", e)

def get_macs():
    try:
        with open(get_path()) as mac_file:
            macs = [i.strip() for i in mac_file]
        return macs
    except Exception as e:
        print("Erro ", e)

# Function to get the path to the current mac file 
def get_last_mac_path():
    with open(os.path.join(MAINPATH, "macs", "last_mac_file.txt"), "r") as reader_mac_file:
            last_mac_file = reader_mac_file.read()
    return os.path.join(MAINPATH, "macs", last_mac_file)

# Function to read quantity of macs in the last MAC file made
def get_mac_quantity():
    try:
        with open(os.path.join(get_path()), "r") as reader_mac_file:
            return len(reader_mac_file.readlines())
    except Exception as e:
        print("Error Mac_Quantity: ", e)
        return None

# Function that return the macs in the last_10_macs txt file 
def write_last_10_macs():
    with open(os.path.join(MAINPATH, "macs", "last_10_macs.txt")) as mac_file:
        last_10_macs = [i.strip() for i in mac_file]
    return last_10_macs

# Function to clean the macs in the last_10_mac txt file, it unwrite the file completely 
def clean_last_10_macs():
    with open(os.path.join(MAINPATH, "macs", "last_10_macs.txt"), "w") as writer_mac_file:
        writer_mac_file.write("")

# Function to write a new mac into the last_10_macs txt file
def last_10_macs(mac):
    with open(os.path.join(MAINPATH, "macs", "last_10_macs.txt"), "r") as reader_mac_file:
        lenght_macs = len(reader_mac_file.readlines())
        if lenght_macs >= 10:
            clean_last_10_macs()
            # with open(os.path.join(MAINPATH, "macs", "last_10_macs.txt"), "w") as mac_file:
            #     mac_file.write("")
        with open(os.path.join(MAINPATH, "macs", "last_10_macs.txt")) as mac_file:
            items = [i.strip() for i in mac_file]
        items.append(mac)
        # Write all the macs in the list into the txt mac file
        with open(os.path.join(MAINPATH, "macs", "last_10_macs.txt"), "w") as writer_mac_file:
            writer_mac_file.write("\n".join(items))         