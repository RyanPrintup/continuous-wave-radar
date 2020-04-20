""" Defines Digital Signal Processing (DSP) filter functions

Author: Ryan Printup
"""

def moving_average(samples, size):
    """ Computes the moving average from a batch
        of samples

        Parameters
        ----------
        samples : list
            A buffer containin the samples
        size : int
            The amount of samples
    """

    return sum(samples) / size


""" End of File """