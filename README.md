# Leitura-MAC-s
Software dedicado a customização de produtos, capaz de realizar a leitura de MAC's e acompanhamento de informções de customização via request com token.

# 📋 Pré-requisitos
Use o instalador de pacotes pip para instalar as bibliotecas presentes no arquivo requirements.txt conforme exemplo abaixo:
pip install example

# Configuração
Será necessário inserir informações em partes do código para a execução do software.

Em "scripts/consult.py", na função "consulta_mac" deve-se inserir o link da API que retornara a informação de customização.
![example 1](https://github.com/user-attachments/assets/8934daee-9c12-43b1-96bb-030bd3703972)

Em "config/token.txt" deve-se colocar o token de acesso ao link já inserido.

Por fim em "scripts/convert_csv.py", na função "send_mac_server" deve ser colocado o endereço IP do host a receber o arquivo .csv
![example 2](https://github.com/user-attachments/assets/31315af8-73ae-4640-8675-19e55ac2df86)

# Complilação
