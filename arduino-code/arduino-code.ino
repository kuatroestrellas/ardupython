#include <LiquidCrystal.h>
#include <DHT.h>

LiquidCrystal milcd(12, 11, 5, 4, 3, 2); 
float h,t;			//humedad y temperatura

int led = 13;
int bomba = 7;
int focos = 8;
int spk = 9;

int dia = 0;
//int intruso = 0;
int waterSensor = 0;

int duration = 250; //Duración del sonido
int freqmin = 2000; 
int freqmax = 4000; 
int melodia[] = {262, 196, 196, 220, 196, 247, 262};
int duracionNota[] = {4,8,8,4,4,4,4,4};

int c[5]={131,262,523,1046,2093}; 	// frecuencias 4 octavas de Do
int cs[5]={139,277,554,1108,2217};	// Do#
int d[5]={147,294,587,1175,2349}; 	// Re
int ds[5]={156,311,622,1244,2489};	// Re#
int e[5]={165,330,659,1319,2637}; 	// Mi
int f[5]={175,349,698,1397,2794}; 	// Fa
int fs[5]={185,370,740,1480,2960};	// Fa#
int g[5]={196,392,784,1568,3136}; 	// Sol
int gs[5]={208,415,831,1661,3322};	// Sol#
int a[5]={220,440,880,1760,3520}; 	// La
int as[5]={233,466,932,1866,3729};	// La#
int b[5]={247,494,988,1976,3951}; 	// Si
void nota(int a, int b);						// declaracion de la funcion auxiliar. Recibe dos numeros

DHT dht(6, 11);					 //Pin 6 y sensor DHT11
void setup() 
{
	Serial.begin(9600);

  dht.begin();					 //inicializamos el sensor
  
  milcd.begin(16,2);     //inicializamos la pantalla
  
  pinMode(led, OUTPUT);
  pinMode(bomba, OUTPUT);
  pinMode(focos, OUTPUT);
  pinMode(spk, OUTPUT);
  
  milcd.print("..::STARTING::..");
  milcd.setCursor(0,2);
  milcd.print("'':: SYSTEM ::''");

  nota(g[2],500);noTone(spk);delay(100);
  nota(g[2],500);noTone(spk);delay(100);
  nota(g[2],500);noTone(spk);delay(100);
  nota(ds[2],500);noTone(spk);delay(1);
  nota(as[2],125);noTone(spk);delay(25);
  nota(g[2],500);noTone(spk);delay(100);
  nota(ds[2],500);noTone(spk);delay(1);
  nota(as[2],125);noTone(spk);delay(25);
  nota(g[2],500);
  noTone(spk);

  milcd.clear();

}

void nota(int frec, int t)
{
tone(spk,frec); // suena la nota frec recibida
delay(t); // para despues de un tiempo t
}

void loop() 
{
  leerSensor();
}


/*
* Lee datos del sensor DHT11
* Los manda imprime por el serial
* Y los muestra en una LCD
*/
void leerSensor()
{
  h = dht.readHumidity();
  t = dht.readTemperature();

  dia = analogRead(A0);
  //intruso = analogRead(A1);
  waterSensor = analogRead(A1);

  if (isnan(t) || isnan(h)) 
  {
    Serial.println("Algo falló ");
  } else 
  {
    Serial.print(h);
    Serial.print(",");
    Serial.print(t);
    Serial.print(",");
    Serial.print(dia);
    if(dia<20){
      digitalWrite(focos, 1);
      }
    else{
      digitalWrite(focos, 0);
      }
    Serial.print(",");
    if (waterSensor<=200)
    {
      Serial.print("Tinaco vacio");
      digitalWrite(led, 1);
    }else
    {
      Serial.print("Tinaco con agua");
      digitalWrite(led, 0);
    }
    Serial.print(",");    
    Serial.println("");
    //
    milcd.print("Humedad: ");
    milcd.print(h);
    milcd.print(" %");
    milcd.setCursor(0,2);
    milcd.print("Temp: ");
    milcd.print(t);
    milcd.print(" C");
    delay(500);
    milcd.clear();
  }
}


void alarma(){
  int i;
  for (i = freqmin; i<=freqmax; i++){
    tone (spk, i, duration);
  }
  for (i = freqmax; i>=freqmin; i--){
    tone (spk, i, duration); 
  }
}
