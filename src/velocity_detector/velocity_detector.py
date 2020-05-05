#!/usr/bin/python

"""Velocity Detector

Detect velocity from a continous-wave radar

Author : Ryan Printup 
"""


# Vendors
import matplotlib.pyplot as plt
import numpy as np

# Standard
import signal
import sys
import serial
import csv # DELETE
from math import pow
from statistics import mean

# Custom
from ring_buf import RingBuffer
import filters as flt
import config as cfg
import freq_utils


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
    impulse_buf  = RingBuffer(cfg.get('filtering', 'impulse_bin_size')) # Store samples for impulse removal
    avg_buf      = RingBuffer(cfg.get('filtering', 'avg_bin_size'))     # Store samples to be averaged
    fft_buf      = [None] * cfg.get('filtering', 'fft_bin_size')        # Store samples to perform FFT on
    fft_buf_i    = 0                                                    # Current index of fft_buf

    # Used to plot velocity graph
    velocity_buf = RingBuffer(100) # Store last 100 velocity values
    fig = plt.figure()
    fig.suptitle("m/s over time")
    fig.show()
    artist, = plt.plot(0)

    # Connect to serial port
    port      = cfg.get('serial', 'port')
    baud_rate = cfg.get('serial', 'baud_rate')

    ser = serial.Serial(port, baud_rate)
    if (ser.is_open == False):
        ser.open()

    # Main loop
    global running
    running = True

    print("Running... Hit Ctrl + C to terminate")
    print("------------------------------------")
    print("\n")
    print("{:6s} {:6s} {:4s}".format("Mag", "Freq", "Speed"))

    while running:
        # Read a packet of data from serial stream. Remove trailing
        # whitespace, new line character, and byte literal. Split data
        # by spaces.
        sample = ser.readline().strip().decode('utf-8')
        
        try:
            sample = int(sample)
        except ValueError:
            continue
        
        sample = flt.remove_dc(sample)

        impulse_buf.append(sample)

        # Wait for the buffer to fill up (initial condition)
        if not impulse_buf.full():
            continue

        # Apply impulse removal and append to average buffer
        # for next step of filtering
        avg_buf.append(flt.impulse_removal(impulse_buf.get()))

        # Wait for the buffer to fill up (initial condition)
        if not avg_buf.full():
            continue
                
        # Peform moving average
        u = mean(avg_buf.get())

        # Populate FFT buffer
        fft_buf[fft_buf_i] = u
        fft_buf_i += 1

        # Wait for the buffer to fill up
        if fft_buf_i == len(fft_buf):
            fft_buf_i = 0
                
            # Perform FFT, find dominant frequency, and compute speed
            freqs, mags = freq_utils.perform_fft(fft_buf)
            freq_d, mag = freq_utils.get_dominant_freq(freqs, mags)
            velocity    = freq_utils.calc_speed_from_freq(freq_d)

            velocity_buf.append(velocity)

            # Debug output
            print("{:02.4f} {:3.1f}Hz {:02.2f}".format(mag, freq_d, velocity))

            # Update velocity plot
            artist.remove()
            artist, = plt.plot(velocity_buf.get(), 'r')
            fig.canvas.draw()
            plt.pause(0.005)

    # Clean up code
    ser.close()


if __name__ == "__main__":
    # Init SIGINT handler for safe termination
    signal.signal(signal.SIGINT, signal_handler)

    # Execute main program
    run()


### End of File ###
