#!/usr/bin/python


"""Serial Stream to CSV

This script connects to a serial communication port specified
in the command line arguments. The port is then continuously polled for data
until told to stop. The data is split by spaces and then written to a csv file
specified in the command line arguments.

The original intent of this script was to record a stream of sensor
readings from an arduino over time. The csv data could then be
used to analyze the data and test various processing techniques
without the need to have physical hardware.

Data over being sent over the serial connection should follow this packet protocol

    <data> <data> <data> ...


Author : Ryan Printup 
"""


import csv
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


def run(port, baud_rate, out_filename):
    """This is the main execution function for this script.
    Execution can be interrupted by pressing Ctrl + C
    
    Parameters
    ----------
    port : str
        The serial port to connect to
    baud_rate : int
        The baudrate for the serial connection
    out_filename : str
        The output file to store the csv data in
    """


    # Connect to serial port
    ser = serial.Serial(port, baud_rate)
    if (ser.is_open == False):
        ser.open()


    # Open CSV output file and writer
    out_file        = open(out_filename, 'w')
    out_file_writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')


    # Main loop
    global running
    running = True
    
    print("Recording Serial Data. Hit Ctrl + C to terminate")

    while running:
        # Read a packet of data from serial stream. Remove trailing
        # whitespace, new line character, and byte literal. Split data
        # by spaces.
        buffer = ser.readline().strip().decode('utf-8').split()
        
        # Check if buffer is populated
        if buffer:
            out_file_writer.writerow(buffer)


    # Clean up code
    out_file.close()
    ser.close()


def print_usage():
    """Print script usage to the user"""

    print("Usage: serial-stream-to-csv.py serial_port baud_rate out_file.csv")


if __name__ == "__main__":
    # Define command line arguments
    port          = None
    baud_rate     = None
    out_filename  = None
    
    
    # Parse command line args
    try:
        port          = sys.argv[1]
        baud_rate     = sys.argv[2]
        out_filename  = sys.argv[3]
    except IndexError:
        print_usage()
        sys.exit(1)


    # Init SIGINT handler for safe termination
    signal.signal(signal.SIGINT, signal_handler)


    # Execute main program
    run(port, baud_rate, out_filename)


### End of File ###
