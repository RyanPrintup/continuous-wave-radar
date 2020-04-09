#!/usr/bin/python


"""Velocity Detector



Author : Ryan Printup 
"""


import serial
import signal
import sys


# Global run variable
running = False


def signal_handler(signal, frame):
    """A signal handler function used to safely exit
    the main execution loop"""

    global running
    running = False



def run(port, baud_rate, sampling_frequency):
    """This is the main execution function for this script.
    Execution can be interrupted by pressing Ctrl + C
    
    Parameters
    ----------
    port : str
        The serial port to connect to
    baud_rate : int
        The baudrate for the serial connection
    sampling_frequency : int
        The sampling frequeny of the DAQ
    """

    # Average Filter Settings
    n        = 50  # Batch Size
    buffer   = []  # Filter Buffer
    buffer_i = 0   # Buffer index

    # Main loop
    global running
    running = True
    
    print("Detecting velocities. Hit Ctrl + C to terminate")

    while running:
        # Read a packet of data from serial stream. Remove trailing
        # whitespace, new line character, and byte literal
        data = ser.readline().strip().decode('utf-8')
        
        # Check if data is populated
        if data:
            buffer[buffer_i] = data
            buffer_i = buffer_i + 1

            # Check if buffer is full
            if (buffer_i >= 50):
                buffer_i = 0
                data_out = sum(buffer) / n
                
                print(data_out)




def print_usage():
    """Print script usage to the user"""

    print("Usage: serial-stream-to-csv.py serial_port baud_rate sampling_frequency")


if __name__ == "__main__":
    # Define command line arguments
    port               = None
    baud_rate          = None
    sampling_frequency = None
    
    # Parse command line args
    try:
        port               = sys.argv[1]
        baud_rate          = sys.argv[2]
        sampling_frequency = sys.argv[3]
    except IndexError:
        print_usage()
        sys.exit(1)


    # Init SIGINT handler for safe termination
    signal.signal(signal.SIGINT, signal_handler)


    # Execute main program
    run(port, baud_rate, sampling_frequency)


### End of File ###
