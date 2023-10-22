from threading import Thread

from serial import Serial

from _dataHYE import DataHYE

from numpy import frombuffer
from numpy import uint8, uint16



def Logger_HYE( serial: Serial, DB: DataHYE ):

    hdrf = 0

    rxData = DB.rxData

    serial.timeout = 0.003

    while ( DB.recording and DB.idxn != DB.n ):

        idxn = DB.idxn

        if ( hdrf == 2 ):
            byte = serial.read(12)
            rxbf = frombuffer( byte, uint16 )
            hdrf = 0

            if ( len( rxbf ) == 6 ):
                rxData[:,idxn] = rxbf
                print( rxbf )

            DB.idxn += 1
            DB.flag  = True

            if ( DB.idxn == DB.n ):
                DB.recording = False

        elif ( hdrf == 0 ):
            byte = serial.read()
            if ( byte == b'\x4D' ):
                hdrf = 1

        elif ( hdrf == 1 ):
            byte = serial.read()
            if ( byte == b'\x4C' ):
                hdrf = 2

        else:
            hdrf = 0