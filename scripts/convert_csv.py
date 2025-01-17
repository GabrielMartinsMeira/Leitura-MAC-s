import csv
import os.path

# Mainpath to the software, to allow work in any directory and OS
MAINPATH = os.path.join(os.path.dirname(os.path.abspath("convert_csv.py")))

# Function to convert MAC txt file to a csv file
def convert_mac():
    from scripts.save_mac import get_infos
    try:
        from scripts.save_mac import get_last_mac_path
        # Get user saved data of max_lenght per file, user and pass 
        dump_lenght_mac, username, password = get_infos()
        # Open the last mac file in reading mode 
        with open(get_last_mac_path(), 'r') as mac_file:
            # Split the file name and extension in 2 variables, and dumps the extension into a useless var
            file_name, dump_extension = os.path.splitext(os.path.basename(get_last_mac_path()))
            file_name += ".csv"
            # Get all the macs in the file and write them in a list
            all_macs = [linha.strip() for linha in mac_file if linha.strip()]
            # Set the path where the csv file will be
            csv_path = os.path.join(MAINPATH, "macs", "csv_files", file_name)
            # Create the csv file with file_name
            with open(csv_path, 'w', newline='') as csvfile:
                # Set the writer
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(['USUARIO', 'SENHA', 'MAC'])
                # Write all the macs in the file using the list created above
                for mac in all_macs:
                    ':'.join(mac[i:i+2] for i in range(0, len(mac), 2)).lower()
                    writer.writerow([username, password, mac])
    except Exception as e:
        print("Error ", e)