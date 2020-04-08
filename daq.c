/* Define Pinouts */
const int RADAR_IN_PIN = A0;

/* Serial Configuration */
const int BAUD_RATE = 115200;

/* Sampling Parameters */
const int SAMPLE_RESOLUTION = 12; // bits
const int SAMPLING_FREQUENCY = 200; // Hz
const int SAMPLING_PERIOD = ((1 / SAMPLING_FREQUENCY) * pow(10, 6)); // us
unsigned long lastTime = 0;



void setup()
{
    analogReadResolution(SAMPLE_RESOLUTION);
    pinMode(RADAR_IN_PIN, INPUT);
    Serial.begin(BAUD_RATE);
} /* setup() */

void loop()
{
    // Ensure sample frequency by checking time between
    // samples and determing if we should sample the radar
    if ((micros() - lastTime) >= SAMPLING_PERIOD)
    {
        lastTime = micros();


        // Sample radar and send over serial
        int value = analogRead(RADAR_IN_PIN);
        Serial.println(value);
    }
} /* loop() */

/*** End of File ***/
