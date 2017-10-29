#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import json

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    Client_data = {}
    def register2json(self):
        """
        Lo usamos para crear el archivo json
        """
        json.dump(self.Client_data, open('registered.json', "w"))
    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")

        LINE = self.rfile.read()
        DATA = LINE.decode('utf-8')
        CORTES = DATA.split(' ')
        if CORTES[0] == 'REGISTER':
            if CORTES[4] != '0\r\n\r\n':
                self.Client_data[CORTES[2]] = self.client_address[0]
            else:
                self.Client_data.pop(CORTES[2])
        print("Datos cliente(IP, puerto): " + str(self.client_address))
        print("El cliente nos manda ", DATA)
        print(self.Client_data)
        print(" =============================")
        self.register2json()
if __name__ == "__main__":
    # Listens at localhost ('') port 6001
    # and calls the EchoHandler class to manage the request
    Server_port = int(sys.argv[1])
    serv = socketserver.UDPServer(('', Server_port), SIPRegisterHandler)

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
