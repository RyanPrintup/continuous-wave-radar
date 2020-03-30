// Configuration
const int RADAR_IN_PIN = A0;
const int BAUD_RATE = 115200;

void setup()
{
    Serial.begin(BAUD_RATE);

    pinMode(RADAR_IN_PIN, INPUT);
} /* setup() */

void loop()
{
    int value = digitalRead(RADAR_IN_PIN);

    Serial.print(value);
} /* loop() */

/*** End of File ***/
