#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Programa cliente UDP que abre un socket a un servidor."""

import socket
import sys

# Constantes. Dirección IP del servidor y contenido a enviar
try:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    METODO = sys.argv[3]
    LOGIN = sys.argv[4]
    EXPIRES = int(sys.argv[5])
except IndexError:
    print('Usage: client.py ip puerto register sip_address expires_value')

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PORT))
    Primer_Mensaje = (METODO.upper() + ' sip:' + LOGIN + ' SIP/2.0\r\n')
    Segundo_Mensaje = ('Expires: ' + str(EXPIRES) + '\r\n')
    Mensaje = Primer_Mensaje + Segundo_Mensaje
    print('Enviando: ' + Mensaje)
    my_socket.send(bytes(Mensaje, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    print('Recibido --> ', data.decode('utf-8'))
print("Socket terminado.")
