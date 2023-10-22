from numpy import zeros

from numpy import uint16



class DataHYE:

    def __init__( self, n ):

        self.rxData = zeros((6,n), dtype=uint16)

        self.Thrust_CMD = zeros((1,n))
        self.LOX_Valve  = zeros((1,n))
        self.LNG_Valve  = zeros((1,n))

        self.LOX = zeros((1,n))
        self.LNG = zeros((1,n))
        self.GN2 = zeros((1,n))

        self.idxn = 0
        
        self.n = n

        self.recording = True

        self.flag = False