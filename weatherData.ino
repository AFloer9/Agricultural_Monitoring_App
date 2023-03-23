void setup() {
  // put your setup code here, to run once:
  
  Serial.begin(9600);

  /* Photo sensor pins */
  
  pinMode(13, OUTPUT);
  pinMode(A0, INPUT);
  

  /* Moisture sensor pins */
  pinMode(12, OUTPUT);
  pinMode(A1, INPUT);

  /* Temperature sensor pins */
  pinMode(11, OUTPUT);
  pinMode(A2, INPUT);
  
  /* Humidity sensor pins */
  pinMode(10, OUTPUT);
  pinMode(A3, INPUT);
  
  /* Water sensor pins */
  pinMode(3, OUTPUT);
  pinMode(A5, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:

 /*
  photoSensor();
  delay(1000);

  moistureSensor();
  delay(1000);

  temperatureSensor();
  delay(1000);
  

  humiditySensor();
  delay(1000);
  */

  waterSensor();
  delay(1000);
}

void  photoSensor() {
  digitalWrite(13, HIGH);
  Serial.print("Photo sensor: ");
  Serial.println(analogRead(A0));
}

void moistureSensor() {
  digitalWrite(12, HIGH);
  Serial.print("Moisture sensor: ");
  Serial.println(analogRead(A1));
}

void temperatureSensor() {
  digitalWrite(11, HIGH);
  Serial.print("Temperature sensor: ");
  Serial.println(analogRead(A2));
}

void humiditySensor() {
  digitalWrite(10, HIGH);
  Serial.print("Humidity sensor: ");
  Serial.println(analogRead(A3));  
}

void waterSensor() {
  digitalWrite(3, HIGH);
  Serial.print("Water sensor: ");
  Serial.println(analogRead(A5));   
}
