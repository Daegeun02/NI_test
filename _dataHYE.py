from numpy import zeros

from numpy import uint16



class DataHYE:

    def __init__( self, n ):

        self.Thrust_CMD = zeros((1,n))
        self.RCS_value  = zeros((8,n))

        self.Ascent_pos = zeros((3,n))

        self.act_CMD = zeros((2,n))
        self.act_RES = zeros((2,n))

        self.IF = zeros((1,n))
        self.CF = zeros((1,n))
        self.IR = zeros((1,n))
        self.IT = zeros((1,n))
        self.IE = zeros((1,n))
        self.St = zeros((1,n))
        self.Ti = zeros((1,n))

        self.TVC = zeros((3,n))
        self.RCS = zeros((3,n))
        self.FCV = zeros((5,n))

        self.Tank = zeros((3,n))

        self.idxn = 0
        
        self.n = n

        self.recording = True

        self.flag = False