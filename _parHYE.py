from _dataHYE import DataHYE

from _resolution import *

from numpy import frombuffer
from numpy import float64, uint16, int16, uint8



def ParsingHYE( DB: DataHYE, data ):
    i = DB.idxn

    DB.IF[0,i] = data[0]
    DB.CF[0,i] = data[1]
    DB.IR[0,i] = data[2]
    DB.IT[0,i] = data[3]
    DB.IE[0,i] = data[4]
    DB.St[0,i] = data[5]
    DB.Ti[0,i] = data[6]

    DB.TVC[0,i] = data[ 7]
    DB.TVC[1,i] = data[ 8]
    DB.TVC[2,i] = data[ 9]
    DB.RCS[0,i] = data[10]
    DB.RCS[1,i] = data[11]
    DB.RCS[2,i] = data[12]
    DB.FCV[0,i] = data[13]
    DB.FCV[1,i] = data[14]
    DB.FCV[2,i] = data[15]

    DB.Ascent_pos[:,i] = \
        ( frombuffer( data[16:22], int16 ) * RXRESOLUTION[POS_RES] ).astype(float64)

    DB.act_CMD[:,i] = \
        ( frombuffer( data[22:26], uint16 ) * RXRESOLUTION[ACT_RES] ).astype(float64)

    DB.act_RES[:,i] = \
        ( frombuffer( data[26:30], uint16 ) * RXRESOLUTION[ACT_RES] ).astype(float64)

    DB.RCS_value[:,i] = frombuffer( data[30:38], uint8 )

    DB.Thrust_CMD[0,i] = \
        ( frombuffer( data[38:40], uint16 ) * RXRESOLUTION[THC_RES] ).astype(float64)

    DB.Tank[:,i] = \
        ( frombuffer( data[40:46], uint16 ) * 0.1 ).astype(float64)

    DB.FCV[3:5,i] = \
        ( frombuffer( data[46:50], uint16 ) * 0.01 ).astype(float64)