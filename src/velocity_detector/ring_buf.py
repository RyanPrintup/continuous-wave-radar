"""

Author: Ryan Printup
"""

class RingBuffer:
    """ Implements a not-yet-full buffer """
    def __init__(self, size):
        self.buf_size = size
        self.data = []

    class __Full:
        """ Implements a full buffer """
        def append(self, x):
            """ Append an element to the end of the buffer
        
                Parameters
                ----------
                x : any
                    The element to append
            """

            self.data[self.cur] = x
            self.cur = (self.cur + 1) % self.buf_size

        def get(self):
            """ Return a list of elements from the oldest to the newest """

            return self.data[self.cur:] + self.data[:self.cur]

        def size(self):
            """ Returns the size of the ring buffer """

            return self.buf_size

        def full(self):
            """ Returns true if the ring buffer is full """

            return True

    def append(self, x):
        """ Append an element to the end of the buffer
        
            Parameters
            ----------
            x : any
                The element to append
        """

        self.data.append(x)

        # Check if buffer is full
        if len(self.data) == self.buf_size:
            # If so, initalize our index variable
            # and permanently change self's class
            # from non-full to full buffer
            self.cur = 0
            self.__class__ = self.__Full

    def get(self):
        """ Return a list of elements from the oldest to the newest """

        return self.data

    def size(self):
        """ Returns the size of the ring buffer """

        return self.buf_size

    def full(self):
        """ Returns true if the ring buffer is full """

        return False
    

""" End of File """
