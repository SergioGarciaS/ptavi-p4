#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import json
import time

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    Client_data = {}
    def register2json(self):
        """
        Lo usamos para crear el archivo json
        """
        with open('registered.json', "w") as outfile:
            json.dump(self.Client_data, outfile, sort_keys=True, indent=4)
    def time(self):

        Actual_Time = int(time.time())
        Actual_Time_str = time.strftime('%Y-%m-%d %H:%M:%S',
                          time.gmtime(time.time()))


    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        atributos = {} # Value de datos del cliente.
        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        LINE = self.rfile.read()
        DATA = LINE.decode('utf-8')
        CORTES = DATA.split(' ')
        EXPIRE = CORTES[4][:-4]
        time_expire_str = time.strftime('%Y-%m-%d %H:%M:%S',
                          time.gmtime(time.time()+int(EXPIRE)))
        if CORTES[0] == 'REGISTER':
            if EXPIRE != '0':
                atributos['address'] = self.client_address[0]
                atributos['expires'] = time_expire_str
                self.Client_data[CORTES[2]] = atributos
            else:
                self.Client_data.pop(CORTES[2])
        print("Datos cliente(IP, puerto): " + str(self.client_address))
        print("El cliente nos manda ", DATA[:-4])
       #print(self.Client_data)
        #print(" =============================")
        self.register2json()
if __name__ == "__main__":
    # Listens at localhost ('') port sys.argv[1]
    # and calls the EchoHandler class to manage the request
    Server_port = int(sys.argv[1])
    serv = socketserver.UDPServer(('', Server_port), SIPRegisterHandler)

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
