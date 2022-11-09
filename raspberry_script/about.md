## Script que estar a rodar no Raspberry

#### Interface ao GSM:

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

#### Creds.json

possui os dados para acesso:

- API Key - Servidor
- GSM Contacto - GSM
- Codigos de Portas - Keypad
