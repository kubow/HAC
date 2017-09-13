// nastaveni komunikacnich pinu - please keep updated s tym co delate
int WinSpPin = 3; //rychlost vetru
int WinDirPin = 4; //smer vetru (prevadi se na pismena)
int TempD1Pin = 5; //digital teplotni cidlo 1
int TempD2Pin = 6; //digital telpotni cidlo 2
int HumiPin = 7; //cidlo vlhkosti
int LuxoPin = 8; //svetelna intenzita
int RainPin = 9;
String Msg = ""; //universal message string

void setup() {
  // serial communication through USB port
  Serial.begin(9600);
  // digital temperature sensor
  pinMode(TempD1Pin, INPUT);
}

void loop() {
  // make the values output and send to serial output
  //float WindSp = analogRead(WinSpPin);
  float WindSp = 5.6;
  Msg = "WindSpeed:" + String(WindSp);
  Serial.println(Msg);
  //float WindSp = analogRead(WinDirPin);
  float WinDir = 1.8;
  Msg = "WindDirection:" + String(WinDir);
  Serial.println(Msg);
  //float Luxo = analogRead(LuxoPin);
  float Luxo = 857;
  Msg = "Luminosity:" + String(Luxo);
  Serial.println(Msg);
  //float Luxo = analogRead(LuxoPin);
  float Temp1 = 20.54;
  Msg = "Temperature1:" + String(Temp1);
  Serial.println(Msg);
  // slow down output for easier reading
  delay(500);
}
