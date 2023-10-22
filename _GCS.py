from threading import Thread

import sys

from serial import Serial

from _resolution import *

from numpy import zeros
from numpy import load
from numpy import frombuffer
from numpy import float64
from numpy import uint16, uint8
from numpy import int16

from time import sleep


txh0_L_TO_1 = int( "0x4C", 16 )
txh1_L_TO_1 = int( "0x4D", 16 )

port = '/dev/ttyUSB1'
baud = 115200


class GroundStation( Thread ):

    def __init__( self, packet: Serial, thread: Thread ):

        super().__init__()

        self.daemon = True
        self.packet = packet
        self.thread = thread

        self.MSG1 = False
        self.MSG5 = False
        self.MSG6 = False
        self.MSG9 = False

        self.MSG11 = 0
        self.MSG12 = 0
        self.MSG13 = 0


    def run( self ):

        while ( not (
            self.MSG1 and self.MSG6 and self.MSG9
        ) ):
            print( f"\033[K    ID       STATUS" )
            print( f"\033[K1 : MSG1  => Target Position" )
            print( f"\033[K5 : MSG5  => Thrust Command" )
            print( f"\033[K6 : MSG6  => Control Command" )
            print( f"\033[K7 : MSG7  => RESET" )
            print( f"\033[K9 : MSG9  => Launch Sign({self.MSG1 and self.MSG9})" )
            print( f"\033[K11: MSG11 => Control Authority" )
            print( f"\033[K12: MSG12 => Mission Number" )
            print( f"\033[K13: MSG13 => Ignition Flag" )

            MSG = input( "\033[KYou need to set 1 parameter\n>>> " )

            print( f"\033[K\033[A" * 12, "\n" )

            print( f"\033[KMSG ID {MSG}" )

            sleep( 1 )

            if ( MSG == "exit" ):
                print( f"\033[EExit process\033[E" )

                self.MSG1 = True
                self.MSG6 = True
                self.MSG9 = True

                sys.exit()

            elif( MSG == "7" ): self._MSG7()
            elif( MSG == "9" ): self._MSG9()

            elif( MSG == "11" ): self._MSG11()
            elif( MSG == "12" ): self._MSG12()
            elif( MSG == "13" ): self._MSG13()

            elif( MSG == "1" ): 
                print( f"" )
                print( f"=" * 80 )
                print( f"\033[KWaypoint for flight" )
                print( f"" )

                Ascent_pos = array(
                    list( map( float64, input( f"\033[KGuidance.Ascent_pos\n>>> " ).split() ) )
                )
                divert_dist = array(
                    list( map( float64, input( f"\033[KGuidance.divert_dist\n>>> " ).split() ) )
                )

                self._MSG1( Ascent_pos, divert_dist )

            elif( MSG == "5" ):
                if self.thread.is_alive():
                    pass
                else:
                    self.thread.start()
                print( f"" )
                print( f"=" * 80 )
                print( f"\033[KThrust Command serial Mode" )
                print( f"" )

                Mode = input( f"\033[KAutomatic or Manual?\n>>> " )

                if ( Mode == "auto" ):
                    Thrust_Profile = load( './HY_scenario.npy' )[80:]
                    for Thrust_CMD in Thrust_Profile:
                        self._MSG5( Thrust_CMD )
                        sleep( 0.02 )
                else:
                    Thrust_CMD = float( input( f"\033[KControl.Thrust_CMD\n>>> " ) )

                    self._MSG5( Thrust_CMD )
            
            elif ( MSG=="6" ):
                print( f"" )
                print( f"=" * 80 )
                print( f"\033[KCommand to send HYE" )
                print( f"" )

                Thrust_CMD = float( input( f"\033[KControl.Thrust_CMD\n>>> " ) )
                RCS_CMD    = array(
                    list( map( int, input( f"\033[KControl.Tx_cmd\n>>> " ).split() ) )
                )

                self._MSG6( Thrust_CMD, RCS_CMD )

    
    def _MSG1( self, Ascent_pos, divert_dist ):
        print( f"" )
        print( f"\033[KAscent_pos : {Ascent_pos}" )
        print( f"\033[Kdivert_dist: {divert_dist}" )
        print( f"=" * 80 )
        print( f"" )

        self.packet.timeout = 1

        txbf = zeros( 17, dtype=uint8 )
        txbf[0] = txh0_L_TO_1
        txbf[1] = txh1_L_TO_1
        txbf[3] = 1

        txbf[ 4:10] = frombuffer(
            ( Ascent_pos * TXRESOLUTION[POS_RES] ).astype(int16).tobytes(), uint8
        )
        txbf[10:16] = frombuffer(
            ( divert_dist * TXRESOLUTION[POS_RES] ).astype(int16).tobytes(), uint8
        )

        self.packet.write( txbf )

        data = self._echo()

        print( 
            ( frombuffer( data[2:14], int16 ) * RXRESOLUTION[POS_RES] ).astype(float64)
        )

        self.MSG1 = True

    
    def _MSG5( self, Thrust_CMD, NON_Print=False ):
        if ( not NON_Print ):
            print( f"" )
            print( f"\033[KThrust CMD: {Thrust_CMD}" )
            print( f"=" * 80 )
            print( f"" )

        txbf = zeros( 17, dtype=uint8 )
        txbf[0] = txh0_L_TO_1
        txbf[1] = txh1_L_TO_1
        txbf[3] = 5

        txbf[4:6] = frombuffer(
            ( Thrust_CMD * TXRESOLUTION[THR_RES] ).astype(uint16).tobytes(), uint8
        )

        self.packet.write( txbf )

    
    def _MSG6( self, Thrust_CMD, RCS_CMD ):
        print( f"" )
        print( f"\033[KThrust CMD: {Thrust_CMD}" )
        print( f"\033[KRCS CMD   : {RCS_CMD}" )
        print( f"=" * 80 )
        print( f"" )

        txbf = zeros( 17, dtype=uint8 )
        txbf[0] = txh0_L_TO_1
        txbf[1] = txh1_L_TO_1
        txbf[3] = 6

        txbf[4:6] = frombuffer(
            ( Thrust_CMD * TXRESOLUTION[THC_RES] ).astype(uint16).tobytes(), uint8
        )
        txbf[6] = uint8( RCS_CMD[0] )
        txbf[7] = uint8( RCS_CMD[1] )
        txbf[8] = uint8( RCS_CMD[2] )
        txbf[9] = uint8( RCS_CMD[3] )

        self.packet.write( txbf )

        
    def _MSG7( self ):
        txbf = zeros( 17, dtype=uint8 )
        txbf[0] = txh0_L_TO_1
        txbf[1] = txh1_L_TO_1
        txbf[3] = 7

        self.packet.write( txbf )

    
    def _MSG9( self ):
        txbf = zeros( 17, dtype=uint8 )
        txbf[0] = txh0_L_TO_1
        txbf[1] = txh1_L_TO_1
        txbf[3] = 9

        self.packet.write( txbf )

        self.MSG9 = True

        self.thread.start()


    def _MSG11( self ):
        pass


    def _MSG12( self ):
        pass


    def _MSG13( self ):
        pass


    def _echo( self ):

        data = None

        self.packet.timeout = 1

        byte = self.packet.read()
        if ( frombuffer( byte, uint8 ) == txh1_L_TO_1 ):
            byte = self.packet.read()
            if ( frombuffer( byte, uint8 ) == txh0_L_TO_1 ):
                data = self.packet.read( 15 )
        
        if ( data == None ):
            print( f"cannot receive echo from GCCM1" )

            return zeros( 17, dtype=uint8 )

        return data
