/**
 * daq.c
 *
 * Target Device: Teensy 4.0
 * Description:   This script uses the ADC on a Teensy 4.0
 *                as a DAQ. It is designed to be minimal achieving
 *                the highest sampling rate possible. All signal
 *                processing should take place on the receiving computer
 *                for maximum efficiency.
 * Author:        Ryan Printup
 **/


#include <math.h>


/* Define Pinouts */
const uint_8 INPUT_PIN = A0;


/* Sampling Parameters */

/**
 * Code Snippet from Teensy 4.0 Source
 * 
 * #define MAX_ADC_CLOCK 20000000
 * // 8 bit conversion (17 clocks) plus 8 clocks for input settling
 * // 10 bit conversion (17 clocks) plus 20 clocks for input settling
 * // 12 bit conversion (25 clocks) plus 24 clocks for input settling
 **/

// The Teensy 4.0 has a 12-bit ADC defaulting
// to 10-bits. This value cannot exceed 12-bits.
const uint8_t SAMPLE_RESOLUTION  = 12; // bits

// Averaging will be performed on the receiving computer
// to avoid unecessary computations on the Teensy.
// This is set to 1 to speed up the Teensy.
const uint8_t SAMPLE_AVERAGE_SIZE = 1;

// NOTE: Averaging is implemented on the receiving computer resulting
// in downsampling. This will NOT be the resultant sampling frequency
const uint32_t SAMPLING_FREQUENCY = 200; // Hz
unsigned long SAMPLING_PERIOD = (unsigned long) ((1.0 / SAMPLING_FREQUENCY) * pow(10, 6)); // us

unsigned long lastTime = 0;


void setup()
{
    analogReadResolution(SAMPLE_RESOLUTION);
    analogReadAveraging(SAMPLE_AVERAGE_SIZE);

    /**
     * NOTE: Teensy 4.0 default internal reference voltage
     * is 3.3V. This value can NOT be changed.
     * Calling analogReference() has no effect.
     **/

    pinMode(RADAR_IN_PIN, INPUT);

    /**
     * NOTE: Teensy 4.0 conducts all serial communication
     * at USB speeds (480 MBit/sec). The value passed into
     * this setting is ignored, but needed to initialize
     * the serial object.
     **/
    Serial.begin(9600);
} /* setup() */


void loop()
{
    // Ensure sample frequency by computing time between
    // samples and checking if it exceeds our sample
    // period
    if ((micros() - lastTime) >= SAMPLING_PERIOD)
    {
        lastTime = micros();

        // Sample analog pin and send over serial
        uint16_t value = analogRead(INPUT_PIN);
        Serial.println(value);
    }
} /* loop() */


/*** End of File ***/
