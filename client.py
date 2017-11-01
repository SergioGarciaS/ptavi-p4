#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import socket
import sys

# Constantes. Dirección IP del servidor y contenido a enviar
if len(sys.argv) == 6:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    USER = sys.argv[4]
    EXPIRES = sys.argv[5]
    if sys.argv[3] == 'register':
        USER = str('REGISTER sip:' + USER)
    # Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
        my_socket.connect((SERVER, PORT))
        Data = USER + ' ' + 'SIP/2.0\r\n' + 'Expires: ' + EXPIRES + '\r\n\r\n'
        print("Enviando:", USER)
        my_socket.send(bytes(Data, 'utf-8'))
        data = my_socket.recv(1024)
        print('Recibido -- ', data.decode('utf-8'))

    print("Socket terminado.")
else:
    sys.exit('Usage: client.py ip puerto register sip_addres expires_value')
