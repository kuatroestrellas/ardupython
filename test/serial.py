import serial

ser = serial.Serial('COM12', 9600) #especificar el puerto y la velocidad en baudios

print """Introduce un caracter
1 para prender el led 1
2 para apagarlo
3 para encender el led 2
4 para apagarlo
('salir' para salir): """
entrada = raw_input("input:  ")

while entrada != 'salir': #salir rompe el bucle

   ser.write(entrada) #envia la entrada por serial
   print ""
   if(int(entrada)==1):
	print "(led1, HIGH);"
   if(int(entrada)==2):
	print "(led1, LOW);"
   if(int(entrada)==3):
	print "(led2, HIGH);"
   if(int(entrada)==4):
	print "(led2, LOW);"
   print ""

   entrada = raw_input("input:  ")
