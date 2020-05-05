#!/usr/bin/python

""" Implements a Ring Buffer data type

Author: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch05s19.html
"""


class RingBuffer:
    """ Implements a not-yet-full buffer """


    def __init__(self, size):
        self.size = size
        self.data = []


    def append(self, x):
        """ Append an element to the end of the buffer
        
            Parameters
            ----------
            x : any
                The element to append
        """
        self.data.append(x)

        # Check if buffer is full
        if len(self.data) == self.size:
            # If so, initalize our index variable
            # and permanently change self's class
            # from non-full to full buffer
            self.cur = 0
            self.__class__ = self.__Full


    def get(self):
        """ Return a list of elements from the oldest to the newest
        
            Return: [any] - The buffer of elements
        """
        return self.data


    def size(self):
        """ Returns the size of the ring buffer
        
            Return: int - The size of the buffer
        """
        return self.size


    def full(self):
        """ Returns true if the ring buffer is full
        
            Return: bool - If the buffer is full or not
        """
        return False


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
            self.cur = (self.cur + 1) % self.size


        def get(self):
            """ Return a list of elements from the oldest to the newest
            
                Return: [any] - The buffer of elements
            """
            return self.data[self.cur:] + self.data[:self.cur]


        def size(self):
            """ Returns the size of the ring buffer
            
                Return: int - The size of the buffer
            """
            return self.buf_size


        def full(self):
            """ Returns true if the ring buffer is full
            
                Return: bool - If the buffer is full or not
            """
            return True
    

""" End of File """
