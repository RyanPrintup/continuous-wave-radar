""" Defines Digital Signal Processing (DSP) filter functions

Author: Ryan Printup
"""

def moving_average(samples):
    """ Computes the moving average from a batch
        of samples

        Parameters
        ----------
        samples : list
            A buffer containing the samples
    """

    return sum(samples) / len(samples)


def dc_removal(sample):
    """ TODO
    
        Parameters
        ----------
        sample: any
            The sample to remove the DC bias from
    """

    return sample - 1960


def impulse_noise_removal(samples):
    """ TODO
    
        Parameters
        ----------
        samples : list
            A buffer containing the samples
    """

    N    = len(samples)
    mean = sum(samples) / N

    tallies = { "positive": 0, "negative": 0, "difference": 0 }
    for sample in samples:
        if (sample > mean):
            tallies["positive"] += 1
            tallies["difference"] += sample - mean

        if (sample < mean):
            tallies["negative"] += 1

    return mean + ((tallies["positive"] - tallies["negative"]) \
           * tallies["difference"]) / (N * N)



""" End of File """