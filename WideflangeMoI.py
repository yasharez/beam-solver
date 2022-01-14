# Class used for calculating moment of inertia for rectangular section
# By Yashar Zafari

class WideflangeI(object):
    '''
    variables:
    self.ft             flange thickness
    self.wt             web thickness
    self.w              total width
    self.h              total height
    methods:
    def __init__ (self, flanget, webt, w, h)
    def getIrect (self)
    '''

    def __init__(self, flanget = 0.0, webt = 0.0, w = 0.0, h = 0.0):
        self.ft = flanget
        self.wt = webt
        self.w = w
        self.h = h
        self.lh = self.h - (2 * self.ft)

    def getIwide(self):
        i = self.wt * (self.lh ** 3.0) / 12.0
        i += (self.w / 12.0) * ((self.h ** 3) - (self.lh ** 3))
        return i