from datetime import date
import os.path

# Function to write the txt with MACS
def save_mac(mac, is_first_mac): 
    try:
        # Verify if the MAC input has 12 characters
        if len(mac) == 12:
            # If is the first MAC, it will create a new txt file with the current date
            if is_first_mac == True: 
                last_mac()
            # Get the path to the last txt mac file
            items, path = get_path()
            # Check if the new MAC isn't in the last txt mac file 
            if not mac in items:
                if len(items) >= 400:
                    last_mac()
                    items, path = get_path()
                # Add the mac to the list
                items.append(mac)
                # Write all the macs in the list into the txt mac file
                with open(path, "w") as writer_mac_file:
                    writer_mac_file.write("\n".join(items))
                last_10_macs(mac)
                return "MAC ASSOCIADO!" 
            else:
                return "MAC Repetido!"

        else:
            return "Leitura Incorreta! Não é um MAC valido!"
    except Exception as e:
        print("Error ", e)

# Function to create a new mac file and set it as the last mac file
def last_mac():
    # Create the variabla txt with the current date 
    mac_file = "MAC " + date.today().strftime("%d-%m-%y") + ".txt"
    # Define the path to the txt file
    path_mac_file = os.path.join(r"C:\Users\ga060496\Documents\Leitura-MAC-s\macs", mac_file)
    # Create the txt file
    f = open(path_mac_file, "x")
    # Write it as the last MAC file
    with open(r"C:\Users\ga060496\Documents\Leitura-MAC-s\macs\last_mac_file.txt", "w") as f:
        f.write(mac_file)

def get_path():
    with open(r"C:\Users\ga060496\Documents\Leitura-MAC-s\macs\last_mac_file.txt", "r") as f:
        last_mac_file = f.read()
        path = os.path.join(r"C:\Users\ga060496\Documents\Leitura-MAC-s\macs", last_mac_file)
    with open(path) as mac_file:
        items = [i.strip() for i in mac_file]
    return items, path

# Function to read quantity of macs in the last MAC file made
def mac_quantity():
    try:
        with open(r"C:\Users\ga060496\Documents\Leitura-MAC-s\macs\last_mac_file.txt", "r") as f:
            last_mac_file = f.read()
        path_last_mac_file = os.path.join(r"C:\Users\ga060496\Documents\Leitura-MAC-s\macs", last_mac_file)
        with open(path_last_mac_file, "r") as f:
            return len(f.readlines())
    except Exception as e:
        print("Error Mac_Quantity: ", e)
        return None
    
def write_mac():
    with open(r"C:\Users\ga060496\Documents\Leitura-MAC-s\macs\last_10_macs.txt") as mac_file:
        items = [i.strip() for i in mac_file]
    return items

def last_10_macs(mac):
    with open(r"C:\Users\ga060496\Documents\Leitura-MAC-s\macs\last_10_macs.txt", "r") as f:
        lenght_macs = len(f.readlines())
        if lenght_macs >= 10:
            with open(r"C:\Users\ga060496\Documents\Leitura-MAC-s\macs\last_10_macs.txt", "w") as f:
                f.write("")
        with open(r"C:\Users\ga060496\Documents\Leitura-MAC-s\macs\last_10_macs.txt") as mac_file:
            items = [i.strip() for i in mac_file]
        items.append(mac)
        # Write all the macs in the list into the txt mac file
        with open(r"C:\Users\ga060496\Documents\Leitura-MAC-s\macs\last_10_macs.txt", "w") as writer_mac_file:
            writer_mac_file.write("\n".join(items))
            