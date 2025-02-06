import csv
import os
import socket
import tqdm

# Mainpath to the software, to allow work in any directory and OS
MAINPATH = os.path.join(os.path.dirname(os.path.abspath("convert_csv.py")))

def send_mac_server(csv_path, file_name):
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 1024 * 4 #4KB

    host = ''  # Insira o endereço IP do computador receptor
    port = 308  # Insira a porta que o receptor está ouvindo

    # get the file size
    filesize = os.path.getsize(csv_path)


    # create the client socket
    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")

    s.connect((host, port))
    print("[+] Connected.")

    # send the filename and filesize
    s.send(f"{file_name}{SEPARATOR}{filesize}".encode())
    progress = tqdm.tqdm(range(filesize), f"Sending {file_name}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(csv_path, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in 
            # busy networks
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))

        # close the socket
        s.close()

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
            send_mac_server(csv_path, file_name)
    except Exception as e:
        print("Error ", e)