# Smart Lock com RPi

> Projeto de Rafawastaken para Electrofun > Setembro 2022

## Sobre o Projeto

Fechadura capaz de ser controlada por:

- Servidor
- GSM - SMS
- Keypad

## Servidor

O servidor será o principal componente do projecto:

- Armazena o estado atual das fechaduras;
- Possui uma API que o Raspberry utiliza para comunicar com o servidor para:
  1.  Alterar o estado;
  2.  Receber o estado atual.

## Raspberry

O raspberry vai estar constantemente a comunicar com o Servidor:

- Enviar GET-Requests para API do servidor para ler estado dos GPIOS;
- Enviar PATCH-Request para Alterar o estado dos GPIOS no servidor.
  - Quando recebe SMS;
  - Quando o código keypad se encontra correto.
