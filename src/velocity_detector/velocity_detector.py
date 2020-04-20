#!/usr/bin/python


"""Velocity Detector

WORK IN PROGRESS

Author : Ryan Printup 
"""


import matplotlib.pyplot as plt
import signal
import sys
import csv
import filters
from ring_buf import RingBuffer
from filters import moving_average


# Global run variable
running = False


def signal_handler(signal, frame):
    """ A signal handler function used to safely exit
        the main execution loop
    """

    global running
    running = False


def run():
    """ This is the main execution function for this script.
        Execution can be interrupted by pressing Ctrl + C
    """

    # Initalize data buffers
    out_data_buf_raw = []
    out_data_buf = [] # Output Data Buffer

    ring_buf = RingBuffer(10)

    # Main loop
    global running
    running = True

    print("Running... Hit Ctrl + C to terminate")

    with open('../../data/movement_test2.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        for row in csv_reader:
            sample = int(row[0])

            ### Modify from here on ###
            out_data_buf_raw.append(sample)
            ring_buf.append(sample)

            if ring_buf.full():
                out_data_buf.append(moving_average(ring_buf.get(), ring_buf.size()))
                




    plt.plot(out_data_buf)
    plt.show()    


def print_usage():
    """ Print script usage to the user """

    print("Usage: velocity-detector.py")


if __name__ == "__main__":
    # Init SIGINT handler for safe termination
    signal.signal(signal.SIGINT, signal_handler)


    # Execute main program
    run()


### End of File ###
