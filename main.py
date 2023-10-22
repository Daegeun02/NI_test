from threading import Thread

from _GCS1 import GroundStation

from _interface import Interface

from _dataHYE import DataHYE

from _log_HYE import Logger_HYE

from numpy import zeros, save

from serial import Serial

import datetime



port = '/dev/tty.usbserial-0001'
baud = 115200

packet = Serial( port, baud )
DB     = DataHYE( 100000 )


if __name__ == "__main__":

    d    = datetime.datetime.now()
    date = f"{d.year}-{d.month:02}-{d.day:02}-{d.hour:02}-{d.minute:02}-{d.second:02}"

    interface = Interface( DB )

    thread = Thread( target=Logger_HYE, args=[packet, DB], daemon=True )

    thread.start()

    GCS = GroundStation( packet, thread, DB, interface )

    GCS.start()

    GCS.join()

    if ( thread.is_alive() ):
        DB.recording = False

        thread.join()

    idxn = DB.idxn

    data = zeros((37,idxn))
    data[ 0 ,:] = DB.Thrust_CMD[0,:idxn]
    data[1:9,:] = DB.RCS_value[:,:idxn]
    
    data[ 9:12,:] = DB.Ascent_pos[:,:idxn]
    data[12:14,:] = DB.act_CMD[:,:idxn]
    data[14:16,:] = DB.act_RES[:,:idxn]
    data[16:17,:] = DB.IF[0,:idxn]
    data[17:18,:] = DB.CF[0,:idxn]
    data[18:19,:] = DB.IR[0,:idxn]
    data[19:20,:] = DB.IT[0,:idxn]
    data[20:21,:] = DB.IE[0,:idxn]
    data[21:22,:] = DB.St[0,:idxn]
    data[22:23,:] = DB.Ti[0,:idxn]
    data[23:26,:] = DB.TVC[:,:idxn]
    data[26:29,:] = DB.RCS[:,:idxn]
    data[29:34,:] = DB.FCV[:,:idxn]
    data[34:37,:] = DB.Tank[:,:idxn]

    save( f"./log/{date}", data )
    print( f"Saved at ./log/{date}.npy" )
    print( f"Use ./read_log.py" )