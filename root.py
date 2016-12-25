#!/usr/bin/env python
# -*- coding: utf-8 -*-

### importando librerias ###
from Tkinter import *
import sqlite3 as dbapi
import time
import os
from tkColorChooser import askcolor
from subprocess import call             ### Mucho cuidado con esta libreria ###
import webbrowser
import shelve                           # para guardar configuraciones
from time import sleep

# serial y bluetooth no vienen por defecto por lo que tiene que instalarse manualmente
import serial
import bluetooth

### importando modulos ###
import pdfs as a

### parametros iniciales ###
bbdd = dbapi.connect("data/bd.sqlite")
cursor = bbdd.cursor()
ser = serial.Serial('/dev/ttyACM0', 9600)
#BDADRESS="00:14:03:05:26:D8" #00:14:03:05:26:D8
#port=1
#sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#sock.connect((BDADRESS, port))

def reload():
    """
    Lee datos del arduino y los guarda en una bd de sqlite3 cada segundo
    al mismo tiempo que muestra en pantalla los datos leidos y actualiza
    el reloj
    """
    gui.after(1000, reload)
    fecha = str(time.localtime()[2]) + "/" + str(time.localtime()[1]) + "/" + str(time.localtime()[0])
    hora = str(time.localtime()[3]) + ":" + str(time.localtime()[4]) + ":" + str(time.localtime()[5])
    mifecha.set(fecha)
    mihora.set(hora)

    #leer = sock.recv(1024)
    leer = ser.readline()
    procesar_dato = leer.split(",")
    var1 = procesar_dato[0]
    var2 = procesar_dato[1]
    var3 = procesar_dato[2]
    var4 = procesar_dato[3]

    humlbl.set('Humedad: ' + str(var1) + ' %')
    temlbl.set('Temperatura: ' + str(var2) + ' *C')
    lumlbl.set('Nivel Luz: ' + str(var3))
    tanque.set(str(var4))

    # aqui guardamos todo en una simple bd de sqlite
    cursor.execute("""
    	insert into registros values ('%s',
    		'%s','%s','%s','%s','%s')"""%(fecha,hora,var1,var2,var3,var4))
    bbdd.commit()

def enviar(x):
    """ Envia ordenes al arduino """
    print x
    #sock.send(str(x))
	#while True:
	#	ser.write(str(x))
	#	break

def setBgColor():
    (triple, hexstr) = askcolor( )
    if hexstr:
        print hexstr
        shelf = shelve.open("/home/kuatroestrellas/NetBeansProjects/proyecto-perrito/src/data/data.dat")
        shelf["color"] = hexstr
        shelf.close()
        gui.configure(bg=hexstr)

def document():
    try:
        #os.system('iceweasel /home/kuatroestrellas/NetBeansProjects/proyecto-perrito/src/documentation/index.html')
        os.chdir('/home/kuatroestrellas/NetBeansProjects/proyecto-perrito/src/documentation/')
        os.startfile('index.html')
    except Exception:
        os.system("xdg-open \"%s\"" % 'index.html')

def github():
    try:
        os.chdir('/home/kuatroestrellas/NetBeansProjects/proyecto-perrito/src/proyecto-perrito.github.io/')
        os.startfile('index.html')
    except Exception:
        os.system("xdg-open \"%s\"" % 'index.html')

def notdone():
    pass#pendiente

def save():
    pass#pendiente

def open():
    shelf = shelve.open("data/data.dat")
    print shelf["color"]
    shelf.close()

def makemenu(win):
    top = Menu(win)
    win.config(menu=top)

    file = Menu(top, tearoff=0)
    file.add_command(label='Guardar...', command=save, underline=0)
    file.add_command(label='Open...', command=open, underline=0)
    file.add_command(label='Salir', command=win.quit, underline=0)
    top.add_cascade(label='Archivo', menu=file, underline=0)

    edit = Menu(top, tearoff=0)
    edit.add_command(label='Configuración',     command=setBgColor,  underline=0)
    edit.add_command(label='Paste',   command=notdone,  underline=0)
    edit.add_separator( )
    top.add_cascade(label='Opciones',     menu=edit,        underline=0)

    submenu = Menu(edit, tearoff=0)
    submenu.add_command(label='COM6', command=win.quit, underline=0)
    submenu.add_command(label='COM12', command=notdone,  underline=0)
    edit.add_cascade(label='Puerto Serie',   menu=submenu,     underline=0)

    about = Menu(top)
    about.add_command(label='Manual', command=document, underline=0)
    about.add_command(label='Pagina del proyecto', command=github, underline=0)
    about.add_command(label='GitHub',
                    command=(lambda: webbrowser.open_new_tab("https://github.com/kuatroestrellas/bluto")),
                    underline=0)
    about.add_separator( )
    about.add_command(label='Sobre Bluto', command=notdone, underline=0)
    top.add_cascade(label='Ayuda', menu=about, underline=0)

gui = Tk()
gui.title('avance 1%')
makemenu(gui)
#gui.iconbitmap('paper-plane.ico')
try:
    shelf = shelve.open("data/data.dat")
    fondo = shelf["color"]
    gui.configure(bg=fondo)
    shelf.close()
except Exception:
    gui.configure(background="white")
#gui.protocol("WM_DELETE_WINDOW", "onexit")
gui.resizable(0,0)
gui.maxsize(width="960",height="630")
gui.minsize(width="960",height="630")

uno = Button(gui,
                text="send",
                command=(lambda: enviar(1)),
                bg="blue",
                fg="white",
                bd=4).place(x=50,y=100)
dos = Button(gui,
                text="send",
                command=(lambda: enviar(2)),
                bg="blue",
                fg="white",
                bd=4).place(x=50,y=150)
tres = Button(gui,
                text="send",
                command=(lambda: enviar(3)),
                bg="blue",
                fg="white",
                bd=4).place(x=50,y=200)
cuatro = Button(gui,
                text="send",
                command=(lambda: enviar(4)),
                bg="blue",
                fg="white",
                bd=4).place(x=50,y=250)
pdf = Button(gui,
                text="create pdf",
                command=(lambda: a.fpdf()),
                bg="red",
                fg="white",
                bd=4).place(x=100,y=350)

humlbl = StringVar()
humedad = Label(gui,
                textvariable=humlbl,
                bg="white",
                fg="black",
                font=("Lucida Console",14),
                relief="sunken"
                ).place(x=440,y=100)

temlbl = StringVar()
temperatura = Label(gui,
                textvariable=temlbl,
                bg="white",
                fg="black",
                font=("Lucida Console",14),
                relief="sunken"
                ).place(x=440,y=150)

lumlbl = StringVar()
temperatura = Label(gui,
                textvariable=lumlbl,
                bg="white",
                fg="black",
                font=("Lucida Console",14),
                relief="sunken"
                ).place(x=440,y=200)

tanque = StringVar()
tinaco = Label(gui,
                textvariable=tanque,
                bg="white",
                fg="black",
                font=("Lucida Console",14),
                relief="sunken"
                ).place(x=440,y=250)

mifecha = StringVar()
l2 = Label(gui,
                textvariable=mifecha,
                bg="white",
                fg="black",
                font=("Lucida Console",14),
                relief="sunken").place(x=440,y=350)

mihora = StringVar()
l2 = Label(gui,
                textvariable=mihora,
                bg="white",
                fg="black",
                font=("Lucida Console",14),
                relief="sunken").place(x=440,y=400)

reload()
gui.mainloop()
