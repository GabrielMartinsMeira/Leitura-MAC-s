root = None

def close_new_window():
    global root
    root.destroy()
    root = None

def open_new_window():
    import customtkinter as ctk
    import os
    global root
    if root is None or not root.winfo_exists():
        # Janela principal
        root = ctk.CTk()
        root.title("Cadastro do TOKEN")
        root.geometry("400x225")
        
        # Não deixa redimencionar a tela
        root.resizable(False, False)

        # Função para carregar as informações do arquivo
        def carregar_informacoes():
            if os.path.exists("token.txt"):
                with open("token.txt", "r") as file:
                    lines = file.readlines()
                    if len(lines) >= 4:
                        entry1.insert(0, lines[0].strip().split(": ")[1])

        # Função para salvar as informações em um arquivo
        def salvar_informacoes():
            item1 = entry1.get()

            with open("token.txt", "w") as file:
                file.write(f"{item1}\n")
            print("Informações salvas com sucesso!")
            root.destroy()
        # Frame para as entradas
        frame = ctk.CTkFrame(root, corner_radius=10)
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

        root.protocol("WM_DELETE_WINDOW", close_new_window)
        # Iniciar o loop principal
        root.mainloop()
    else:
        root.lift()