import customtkinter as ctk
import os
import asyncio
import threading

window_customize = None

def close_customize_window():
    global window_customize
    window_customize.destroy()
    window_customize = None

def open_window_customize(async_loop):
    
    from config.config_customize import open_new_window
    global window_customize
    if window_customize is None or not window_customize.winfo_exists():
        ctk.set_appearance_mode("dark")
        window_customize = ctk.CTk()

        window_customize.title("Customize")
        window_customize.geometry("1020x580")
        window_customize.configure(fg_color='#433A3A')

        window_customize.resizable(False, False)

        # Container para os cards
        container = ctk.CTkFrame(window_customize, fg_color="#433A3A")
        container.pack(pady=20)
        
        for i in range(10):
            card, entry, status_label, fw_label, client_label = create_card(container, f"Produto {i+1}", "MAC", "Desconhecido", "1.25.5", "Desconhecido")
            entries.append(entry)
            status_labels.append(status_label)
            fw_labels.append(fw_label)
            client_labels.append(client_label)
            row, col = divmod(i, 5)
            card.grid(row=row, column=col, padx=10, pady=10)
            
            # Iniciar o loop assíncrono em uma thread separada para cada MAC
            next_entry = entries[i + 1] if i < len(entries) - 1 else None
            threading.Thread(target=start_async_loop, args=(entry, status_label, fw_label, client_label, next_entry)).start()

        button_frame = ctk.CTkFrame(window_customize, fg_color="#433A3A")
        button_frame.pack(pady=10)

        # Botão para tratar os dados
        buttonStart = ctk.CTkButton(button_frame, text="Configuração", command=open_new_window)
        buttonStart.pack(side="left", padx=10)

        # Botão para limpar os campos de entrada
        buttonClear = ctk.CTkButton(button_frame, text="Limpar Campos", command=clear_entries)
        buttonClear.pack(side="left", padx=10)

        window_customize.protocol("WM_DELETE_WINDOW", close_customize_window)
        window_customize.mainloop()
    else:
        window_customize.lift()

# Função para criar um card individual com entrada de dados
def create_card(parent, title, mac, status, fw_version, client):
    card = ctk.CTkFrame(parent, width=150, height=250, fg_color="#009DB8", corner_radius=15)
    
    title_label = ctk.CTkLabel(card, text=title, font=("Arial", 12), width=150, height=30, fg_color="#433A3A", corner_radius=15)
    title_label.pack(pady=12, padx=10)
    
    # Entradas de dados
    mac_entry = ctk.CTkEntry(card, placeholder_text=mac)
    mac_entry.pack(pady=5)
    
    status_label = ctk.CTkLabel(card, text=f"Sem mac\n{status}", font=("Arial", 12), text_color="black", justify="center")
    status_label.pack(pady=5)
    
    fw_label = ctk.CTkLabel(card, text=f"Versão de FW\n{fw_version}", font=("Arial", 12), text_color="black", justify="center")
    fw_label.pack(pady=5)

    client_label = ctk.CTkLabel(card, text=f"Cliente\n{client}", font=("Arial", 12), text_color="black", justify="center")
    client_label.pack(pady=5)

    return card, mac_entry, status_label, fw_label, client_label

# Função assíncrona para fazer a consulta e atualizar o status, versão e cliente
async def update_status_async(entry, status_label, fw_label, client_label, next_entry=None):
    from scripts.consult import consulta_mac
    while True:
        try:
            mac = entry.get().lower()
            if len(mac) == 12:  # Verifica se o MAC tem exatamente 12 caracteres
                result = consulta_mac(mac)  # Chame a função de consulta do seu script Python
                if result != 10:  # Verifica se o MAC foi encontrado
                    assoc_status, fw_version, client = result
                    if assoc_status == 0:
                        status_label.configure(text="Status: Sem perfil", text_color="white")
                    elif assoc_status == 1:
                        status_label.configure(text="Status: Aplicando", text_color="blue")
                    elif assoc_status == 2:
                        status_label.configure(text="Status: Confirmado", text_color="green")
                    elif assoc_status == 4:
                        status_label.configure(text="Status: Reaplicando", text_color="yellow")

                    fw_label.configure(text=f"Versão de FW\n{fw_version}",  text_color="white")  # Atualiza a versão de firmware
                    client_label.configure(text=f"Cliente\n{client}",  text_color="white")  # Atualiza o cliente
                else:
                    status_label.configure(text="MAC não encontrado", text_color="red")
                    fw_label.configure(text="Versão de FW\nDesconhecida", text_color="black")
                    client_label.configure(text="Cliente\nDesconhecido", text_color="black")
                # Simula o 'tab' para mover para o próximo campo
                if next_entry:
                    next_entry.event_generate("<Tab>")
            elif len(mac) > 12:
                # Limpa o campo e mostra mensagem de erro
                entry.delete(0, ctk.END)
                status_label.configure(text="Erro: MAC muito longo", text_color="red")
                fw_label.configure(text="Versão de FW\nErro")
                client_label.configure(text="Cliente\nErro")
            else:
                status_label.configure(text="Sem mac", text_color="blue")
                fw_label.configure(text="Versão de FW\nDesconhecida", text_color="black")
                client_label.configure(text="Cliente\nDesconhecido", text_color="black")
            await asyncio.sleep(0.5)  # Aguarde 1 segundo antes da próxima consulta
        except Exception as e:
            print("Error ", e)
            break

# Função para iniciar a consulta de forma assíncrona
def start_async_loop(entry, status_label, fw_label, client_label, next_entry=None):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(update_status_async(entry, status_label, fw_label, client_label, next_entry))

# Função para limpar todos os campos de entrada
def clear_entries():
    for entry in entries:
        entry.delete(0, ctk.END)  # Limpa o valor do campo de entrada

# Criando e posicionando os cards individualmente
entries = []
status_labels = []
fw_labels = []
client_labels = []
