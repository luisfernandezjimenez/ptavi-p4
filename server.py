#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        datos = {}
        self.wfile.write(b"Hemos recibido tu peticion")
        for line in self.rfile:
            if line.decode('utf-8')[:8] == 'REGISTER':
                datos[line.decode('utf-8')[14:-10]] = self.client_address[0]
                print("El cliente nos manda ", line.decode('utf-8'))
                print('SIP/2.0 200 OK\r\n\r\n')
            elif line.decode('utf-8') != '\r\n':
                print("El cliente nos manda ", line.decode('utf-8'))    

if __name__ == "__main__":
    serv = socketserver.UDPServer(('', int(sys.argv[1])), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
