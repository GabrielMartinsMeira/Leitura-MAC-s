from datetime import date
import os.path

# Function to write the txt with MACS
def write_mac(mac, first_mac): 
    try:
        # Verify if the MAC input has 12 characters
        if len(mac) == 12:
            print("Valid MAC")
            # If is the first MAC, it will create a new txt file
            if first_mac == True:
                # Create the txt file with the current date
                last_mac()
            
            #f = open(path_mac_file, "x")
            # with open(mac_file, 'a') as file:
            #     file.write("\n".join(mac))
            return "OK" 
        else:
            return("Not a valid MAC")
    except Exception as e:
        print("Error ", e)

# Function to create a new mac file and set it as the last mac file
def last_mac():
    # Create the variabla txt with the current date 
    mac_file = "MAC " + date.today().strftime("%d-%m-%y") + ".txt"
    # Define the path to the txt file
    path_mac_file = os.path.join(r"C:\Users\ga060496\Documents\Leitura-MAC-s\macs", mac_file)
    print("PATH: ", path_mac_file)
    # Create the txt file
    f = open(path_mac_file, "x")
    # Write it as the last MAC file
    with open(r"C:\Users\ga060496\Documents\Leitura-MAC-s\macs\last_mac_file.txt", "w") as f:
        f.write(mac_file)

# Function to read quantity of macs in the last MAC file made
def mac_quantity():
    with open(r"C:\Users\ga060496\Documents\Leitura-MAC-s\macs\last_mac_file.txt", "r") as f:
        last_mac_file = f.read()

    path_last_mac_file = os.path.join(r"C:\Users\ga060496\Documents\Leitura-MAC-s\macs", last_mac_file)

    with open(path_last_mac_file, "r") as f:
        #print(len(f.readlines()))
        return len(f.readlines())
    
#write_mac("982A0A510D32", True)
mac_quantity()