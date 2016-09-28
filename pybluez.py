#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bluetooth

BDADRESS="00:14:03:05:26:D8" #dirección del dispositivo bluetooth

port=1
sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((BDADRESS, port))
print """ingresa
1 para encender el led 1
2 para apagar el led 1
3 para encender el led 2
4 para apagar el led 2
s para salir
"""
valor=raw_input("input: ")
while valor !='s': #s romple el bucle
    sock.send(valor)
    valor=raw_input("input: ")
