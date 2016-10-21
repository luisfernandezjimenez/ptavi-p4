#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Clase (y programa principal) para un servidor de eco en UDP simple."""

import socketserver
import sys
import json
import time


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """Echo server class."""

    def handle(self):
        """Almacenar y eliminar usuarios en mi lista de clientes."""
        self.json2registered()
        fichero = self.rfile.read()
        linea_cliente = fichero.decode('utf-8').split(' ')

        metodo = linea_cliente[0]
        direccion = linea_cliente[1].split(':')
        usuario = direccion[1]
        IP = self.client_address[0]
        expires = int(' '.join(linea_cliente[3].split(': ')))

        tiempo_actual = int(time.time())
        tiempo_actual_string = time.strftime('%Y-%m-%d %H:%M:%S',
                                             time.gmtime(tiempo_actual))
        tiempo_expirar = int(expires + tiempo_actual)
        tiempo_expiracion_string = time.strftime('%Y-%m-%d %H:%M:%S',
                                                 time.gmtime(tiempo_expirar))
        print('El cliente nos manda: ',  ' '.join(linea_cliente))

        self.datos = {}
        eliminar = []  # metemos los usuarios que borremos
        if metodo == 'REGISTER':
            datos['Direccion'] = IP
            datos['Expiracion'] = tiempo_expiracion_string
            lista_clientes[usuario] = datos
            if expires != 0:
                print('REGISTRAMOS a ' + usuario + ' en la lista de clientes.')

            for Cliente in lista_clientes:
                dato = lista_clientes[Cliente]
                if tiempo_actual_string >= dato['Expiracion']:
                    eliminar.append(Cliente)

            for usuario in eliminar:
                print('El usuario ' + usuario + ' se ha DESCONECTADO')
                del lista_clientes[usuario]

            print('Mandamos confirmacion\r\n')
            self.wfile.write(b'SIP/2.0 200 OK' + b'\r\n\r\n')
            self.register2json()

    def register2json(self):
        u"""Imprimir fichero registered.json con información del usuario."""
        with open('registered.json', 'w') as archivo_json:
            json.dump(lista_clientes, archivo_json, sort_keys=True,
                      indent=4, separators=(',', ': '))

    def json2registered(self):
        """Comprobar si hay un fichero llamado registered.json."""
        try:
            with open("registered.json", 'r') as json_fich:
                datos_json = json.load(json_fich)
                usuarios = datos_json.keys()
            for usuario in usuarios:
                lista_clientes[usuario] = self.datos
        except:
            pass

if __name__ == "__main__":
    lista_clientes = {}
    serv = socketserver.UDPServer(('', int(sys.argv[1])), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
