# Class used for calculating moment of inertia for rectangular section
# By Yashar Zafari

class RectangleI(object):
    '''
    variables:
    self.w
    self.h
    methods:
    def __init__ (self, w, h)
    def getIrect (self, w, h)
    '''

    def __init__(self, w = 0.0, h = 0.0):
        self.w = w
        self.h = h

    def getIrect(self):
        i = self.w * self.h * self.h * self.h / 12
        return i