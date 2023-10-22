from threading import Thread

from _interface import Interface

from serial import Serial

from _dataHYE import DataHYE

from _log_HYE import Logger_HYE

from numpy import save

import datetime



port = '/dev/tty.usbserial-0001'
baud = 115200


if __name__ == "__main__":

    d    = datetime.datetime.now()
    date = f"{d.year}-{d.month:02}-{d.day:02}-{d.hour:02}-{d.minute:02}-{d.second:02}"

    packet = Serial( port, baud )
    DB     = DataHYE( 5000 )

    thread = Thread( target=Logger_HYE, args=[packet, DB], daemon=True )

    thread.start()

    input( "stop when you want" )

    if ( thread.is_alive() ):
        DB.recording = False
        DB.idxn      = 5000

        thread.join()

    save( f"./log/{date}", DB.rxData )
    print( f"Saved at ./log/{date}.npy" )
    print( f"Use ./read_log.py" )