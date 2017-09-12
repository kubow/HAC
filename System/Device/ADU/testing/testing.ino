// variable to hold random number
long randomNumber;
String Heading;

void setup() {
  // serial communication through USB port
  Serial.begin(9600);
  // randomizer
  randomSeed(100);
  // print table heading - to python parser
  Heading = "temp, luxo, humi, windir, windsp";
}

void loop() {
  // generate random number
  randomNumber = random(100);
  // print heading
  Serial.println(Heading);
  // make the values output and send to serial output
  String Msg = "20, 80, 30, NW, 5.5";
  //String Msg = "";
  //Msg.concat(randomNumber + ", ");
  //Msg.concat(randomNumber + ", ");
  //Msg.concat(randomNumber + ", ");
  //Msg.concat(randomNumber + ", ");
  //Msg.concat(randomNumber);
  Serial.println(Msg);
  // slow down output for easier reading
  delay(500);
}
