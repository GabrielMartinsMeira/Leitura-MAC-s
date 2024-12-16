import csv
import os.path

# Function to convert MAC txt file to a csv file
def convert_mac():
    # Open a txt file with the last mac file used by the user
    with open(r"macs\last_mac_file.txt", "r") as f:
        # Stores the information in a var
        last_mac_file = f.read()
        # Get the path to the last mac file
        path = os.path.join(r"macs", last_mac_file)
        # Open the last mac file with a reader 
        with open(path, 'r') as f:
            # Split the file name and extension in 2 variables
            file_name, ext = os.path.splitext(os.path.basename(path))
            file_name += ".csv"
            # Get all the macs in the file and put them in a list
            all_macs = [linha.strip() for linha in f if linha.strip()]
        
        # Set the path where the csv file will be
        csv_path = os.path.join(r"macs\csv_files", file_name)
        # Create the csv file with file_name
        with open(csv_path, 'w', newline='') as csvfile:
            # Set the writer
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['USUARIO', 'SENHA', 'MAC'])
            # Write all the macs in the file
            for mac in all_macs:
                ':'.join(mac[i:i+2] for i in range(0, len(mac), 2)).lower()
                #mac_formatado = formatar_mac(all_macs)
                writer.writerow(['admin', 'admin', mac])