/**
**el código es el mismo para bluetooth y para el serial
**/
int mssg = 0; //variable para guardar el mensaje

void setup()
{
   pinMode(8, OUTPUT);
   pinMode(7, OUTPUT);
   Serial.begin(9600); //iniciando Serial
}

void loop()
{
   if (Serial.available() > 0)
   {
      mssg = Serial.read(); //leemos el serial

      if(mssg == '1')
      {
         digitalWrite(8, HIGH); //si recibe '1' encendemos
      }
      else if(mssg == '2')
      {
         digitalWrite(8, LOW); //si recibe '2' apagamos
      }
       if(mssg == '3')
      {
         digitalWrite(7, HIGH); //si recibe '3' apagamos
      }
      else if(mssg == '4')
      {
         digitalWrite(7, LOW); //si recibe '4' encendemos
      }
   }
}
