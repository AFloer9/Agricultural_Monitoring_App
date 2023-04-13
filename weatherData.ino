// Author: Alexander Flores Spring 2023 Class: CS 320
#include <dht.h>
#include <math.h>

#define dataPin 10
dht DHT;

/* temperature consts */
const int B = 4275; /* value of thermistor */
const int R0 = 100000; /* 100k ohms */

void setup() {
  // put your setup code here, to run once:
  
  Serial.begin(9600);

//   /* Photo sensor pins */
//   pinMode(13, OUTPUT);
//   digitalWrite(13, LOW);
//   pinMode(A0, INPUT);
  
 /* Temperature sensor pins */
  pinMode(11, OUTPUT);
  digitalWrite(11, LOW);
  pinMode(A2, INPUT);
  
  /* Humidity sensor pins */
  //pinMode(7, OUTPUT);
  //digitalWrite(7, LOW);
  pinMode(10, INPUT);


  /* Moisture sensor pins */
  //pinMode(12, OUTPUT);
  //digitalWrite(12, LOW);
  //pinMode(A1, INPUT);
  
  
  /* Water sensor pins */
  //pinMode(3, OUTPUT);
  //digitalWrite(3, LOW);
  //pinMode(A5, INPUT);
}

void loop() {
 
  // photoSensor();
  // delay(1000);

   temperatureSensor();
   delay(1000);
  
  humiditySensor();
  delay(2000);
  
  /*
  moistureSensor();
  delay(1000);
 
  waterSensor();
  delay(1000);
*/
}

void  photoSensor() {
  /*
  *
  * Setup (1-30): 
  *   5V-GND-A0
  *
  */
  digitalWrite(13, HIGH);
  delay(100);
  Serial.print("PHOTO ");
  float signal = analogRead(A0);
  digitalWrite(13, LOW);
  Serial.println(signal);
  
  //delay(5000);
  /*if (signal <= 400) {
    Serial.println(signal);
    Serial.println("Dark");
  } else if (signal <= 700) {
      Serial.println(signal);
      Serial.println("medium brightness");
  } else {
    Serial.println(signal);
    Serial.println("Bright");
  }
  */
}

void moistureSensor() {
  digitalWrite(12, HIGH);
  delay(10);
  float signal = analogRead(A1);
  digitalWrite(12, LOW);
  Serial.print("Moisture sensor: ");
  Serial.println(signal);

}

void temperatureSensor() {
  // Dig Temp -  tells you the change in temperature
  // A2 - 5V - GND
  //use new temp sensor; when there its warmer there is less resistance
  // vcc - 5v; sig - analog signal
  
  digitalWrite(11, HIGH);
  delay(10);
  float signal = analogRead(A2);
  digitalWrite(11, LOW);

  float R = 1023.0/signal-1.0;
  R = R0*R;
  float temp =  1.0/(log(R/R0)/B+1/298.15)-273.15; // Steinhart-Hart NTC equation
  float tempF = (temp * 1.8) + 32.0;
  Serial.print("TEMP ");
  Serial.println(tempF);
  
  //float volt = signal * (5/1023);//0.003225806;//
  //float tempc = (volt - 0.5) *100;
  //Serial.println(tempc);
  //Serial.println(signal);

}

void humiditySensor() {
  /*
  digitalWrite(10, HIGH);
  Serial.print("Humidity sensor: ");
  Serial.println(analogRead(A3));  
  */
  /*
    CONNECTION: GND-IGNORE-DATA-VCC
    Arduino:    GND-______-DIGITAL10&&5.1KOHM&&5V_-5V_
  */
  //digitalWrite(7, HIGH);
  //delay(10);
  
  int readData   = DHT.read11(dataPin);
  float tempC    = DHT.temperature;
  float humidity = DHT.humidity;
  //digitalWrite(7, LOW);
  
  float tempF = (tempC * 9.0) / 5.0 + 32.0;

  Serial.print("DHT_TEMP "); // Fahrenheit
  Serial.println(tempF);
  Serial.print("DHT_HUM "); // %
  Serial.println(humidity);
  
  }

void waterSensor() {
  /*
   D3 - GND - A5
   less resistance when there is more water
   max 155~
   middle 120~
   */

  digitalWrite(3, HIGH);
  delay(10);
  float signal = analogRead(A5);
  digitalWrite(3, LOW);  
  Serial.print("Water sensor: ");
  Serial.println(signal); 
  
}
