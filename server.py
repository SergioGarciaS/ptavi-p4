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
        Json creator
        """
        with open('registered.json', "w") as outfile:
            json.dump(self.Client_data, outfile, sort_keys=True, indent=4)
            
    def json2registered(self):
        """
        Json file checker
        """
        try:
            with open("registered.json", "r") as data_file:
                self.Client_da = json.load(data_file)
                self.exist_file = True
        except:
            self.exist_file = False
    
    def comprobar_cad(self):
        time_str = time.strftime('%Y-%m-%d %H:%M:%S +%Z',
                          time.gmtime(time.time()))
        for cosas in self.Client_data:
            print(self.Client_data[cosas]['expires'])
            if self.Client_data[cosas]['expires'] >= time_str:
                print("PUTO AMO")
            else:
                print("MAS AMO TODAVIA")
            """
            for movidas in self.Client_data[cosas]:
            
                print(movidas)
                if movidas == 'expires':
                    print("true")
                else:
                    print("que loco")
            """                
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
        time_expire_str = time.strftime('%Y-%m-%d %H:%M:%S +%Z',
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
        self.comprobar_cad()
        self.register2json()
        self.json2registered()
        if self.exist_file == 'true':
            print(self.Client_da)
if __name__ == "__main__":

    Server_port = int(sys.argv[1])
    serv = socketserver.UDPServer(('', Server_port), SIPRegisterHandler)

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
