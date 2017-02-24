int LDR_Pin = A0; //analog pin 0

void setup(){
  Serial.begin(9600);
}

void loop(){
  int LDRReading = analogRead(LDR_Pin); 
  String Sensor = "luxo:";
  String Msg = Sensor + LDRReading;
  Serial.println(Msg);
  delay(500); //just here to slow down the output for easier reading
}
