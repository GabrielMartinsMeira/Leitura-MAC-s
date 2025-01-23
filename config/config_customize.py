import os
import customtkinter as ctk

token_window = None

# Mainpath to the software, to allow work in any directory and OS
MAINPATH = os.path.join(os.path.dirname(os.path.abspath("config_customize.py")))

def close_new_window():
    global token_window
    if token_window is not None:
        token_window.destroy()
        token_window = None
    
def open_new_window():
    global token_window
    if token_window is None or not token_window.winfo_exists():
        # Janela principal
        ctk.set_appearance_mode("dark")
        token_window = ctk.CTk()

        token_window.title("Cadastro do TOKEN")
        token_window.geometry("400x225")
        
        # Não deixa redimencionar a tela
        token_window.resizable(False, False)

        # Função para carregar as informações do arquivo
        def carregar_informacoes():
            if os.path.exists(os.path.join(MAINPATH, "config", "token.txt")):
                with open(os.path.join(MAINPATH, "config", "token.txt"), "r") as file:
                    lines = file.readlines()
                    if len(lines) >= 4:
                        entry1.insert(0, lines[0].strip().split(": ")[1])

        # Função para salvar as informações em um arquivo
        def salvar_informacoes():
            item1 = entry1.get()

            with open(os.path.join(MAINPATH, "config", "token.txt"), "w") as file:
                file.write(f"{item1}\n")
            print("Informações salvas com sucesso!")
            close_new_window()
        # Frame para as entradas
        frame = ctk.CTkFrame(token_window, corner_radius=10)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Entradas de texto
        label1 = ctk.CTkLabel(frame, text="Token Válido")
        label1.pack(pady=5)
        entry1 = ctk.CTkEntry(frame)
        entry1.pack(pady=5)

        # Botão de salvar
        save_button = ctk.CTkButton(frame, text="Salvar", command=salvar_informacoes)
        save_button.pack(pady=20)

        # Carregar informações do arquivo ao iniciar
        carregar_informacoes()

        token_window.protocol("WM_DELETE_WINDOW", close_new_window)
        # Iniciar o loop principal
        token_window.mainloop()
    else:
        token_window.lift()