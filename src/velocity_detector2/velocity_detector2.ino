/**
 * daq.c
 *
 * Target Device: Teensy 4.0
 * Description:   This script uses the ADC on a Teensy 4.0
 *                as a DAQ. It is designed to be minimal achieving
 *                the highest sampling rate possible. All signal
 *                processing should take place on the receiving computer
 *                for maximum efficiency.
 * Author:        Ryan Printup, Matt Smith
 **/


#include <math.h>
#define NUM_SAMPLES 100
#define THRESHOLD 1960
#define CALFACTOR 0.0011


/* Define Pinouts */
const uint8_t RADAR_IN_PIN = A0;


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
const uint32_t SAMPLING_FREQUENCY = 10000; // Hz
unsigned long SAMPLING_PERIOD = (unsigned long) ((1.0 / SAMPLING_FREQUENCY) * pow(10, 6)); // us

unsigned long lastTime = 0;
float EMA = 1950;
float prev_EMA = 1950;
float counter = 1;


void setup()
{
    analogReadResolution(SAMPLE_RESOLUTION);
    //analogReadAveraging(SAMPLE_AVERAGE_SIZE); //causes erroneous spikes, do not use

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
    Serial.begin(115200);
} /* setup() */


void loop()
{
    // Ensure sample frequency by computing time between
    // samples and checking if it exceeds our sample
    // period
    int sum = 0;
    if ((micros() - lastTime) >= SAMPLING_PERIOD)
    {
          lastTime = micros();
          // Sample analog pin and send over serial
          uint16_t value = analogRead(RADAR_IN_PIN);        //read voltage on pin
          prev_EMA = EMA;                                   //store previous value of exponential moving average
          EMA = (EMA*(NUM_SAMPLES-1) + value)/NUM_SAMPLES;  //calculate exponential moving average to reduce noise
          //Serial.println(EMA);
          
        if (EMA > THRESHOLD && prev_EMA <= THRESHOLD){      //if the EMA is crossing over a threshold
          if (counter > 50) {                               //make sure it is a minimum value to not trigger off noise
            //Serial.println(counter);
            float freq = (10000/counter);                   //convert number of samples to frequency
            if (freq <= 500) {                              //if freq is above 500 it is probably an error
              float speed = (freq*299792458*CALFACTOR)/(2*2000000);   //convert frequency to speed with carrier freq and speed of light
              Serial.println(speed);                        //it is also multiplied by a calibration factor to be accurate
            }
            counter = 0;
          }
        }
        else if (counter > 10000) {                         //make timeout, if no crossing occurs within 10000 samples (1s)
          //Serial.println("1000");
          Serial.println("0");                              //output 0 m/s
          counter = 0;
        }
        counter++;
    }
    
} /* loop() */


/*** End of File ***/
