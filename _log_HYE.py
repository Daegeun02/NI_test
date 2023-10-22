from serial import Serial

from _dataHYE import DataHYE

from _parHYE import ParsingHYE



def Logger_HYE( serial: Serial, DB: DataHYE ):

    hdrf = 0

    serial.timeout = 0.1

    while ( DB.recording and DB.idxn != DB.n ):

        if ( hdrf == 2 ):
            byte = serial.read(56)
            hdrf = 0

            if ( len(byte) == 56 ):
                ParsingHYE( DB, byte )

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