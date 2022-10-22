# Smart Lock com RPi

> Projeto de Rafael Pimenta para Electrofun > Setembro 2022
> Rep: https://github.com/Rafawastaken/locker_rpi

## Sobre o Projeto

Fechadura capaz de ser controlada por:

- Servidor
- GSM - SMS
- Keypad

## Servidor

Servidor será o principal componente do projeto, deverá:

### Gerir Utilizadores

- Adicionar, Remover e Editar utilizadores

### Gerir Códigos de Keypad

- Possiblitar a alteração de códigos do keypada para cada porta

### Logs

- Armazenar os LOGS de cada abertura e fecho de porta (GSM, Keypad ou Servidor)

### GSM

- Gerir números permitidos para controlar as portas

### Integração de novos Raspberries

- Aceitar a configuração de forma simples de outros raspberries

### Integração de outras Portas

- Aveitar a configuração ed mais portas e associar ao respetivo controlador

## Raspberry

O script a ser executado no raspberry deve conter as seguintes funcionalidades

### Interface ao GSM:

- Ler mensagens em tempo real
- Processar mensagens recebidas:
- Controlar GPIOS
- Estado do SIM (Saldo)
- Alterar Códigos (Codigos de portas)

### Interface Keypad:

- Ler codigos de portas
- Comparar códigos de portas

### Comunicar com Servidor:

- GET Request estado de portas
- PATCH Request altear estado de portas
- POST Request adicionar logs

## Creds.json

Armazena os dados para acesso:

- API Key - Servidor
- GSM Contacto - GSM
- Codigos de Portas - Keypad

## Montagem

Ligações a serem executadas com o raspberry e respetivos perifericos

### Keypad - Raspberry

L1 = 1
L2 = 2
L3 = 8
L4 = 7
C1 = 3
C2 = 4
C3 = 5

### GSM - Raspberry

VCC - 5V
GND - GND
RX - TX
TX - RX
