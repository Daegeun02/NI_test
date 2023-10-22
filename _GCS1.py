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

            print( f"\033[K\033[A" * 12 )

            print( f"\033[KMSG ID: {MSG}" )

            sleep( 1 )

            if ( MSG == "exit" ):
                print( f"\033[EExit Process\033[E" )

                self.MSG1 = True
                self.MSG6 = True
                self.MSG9 = True

                sys.exit()

            elif ( MSG == "1" ): self._MSG1()
            elif ( MSG == "5" ): self._MSG5()
            elif ( MSG == "6" ): self._MSG6()
            elif ( MSG == "7" ): self._MSG7()
            elif ( MSG == "9" ): self._MSG9()

            elif ( MSG == "11" ): self._MSG11()
            elif ( MSG == "12" ): self._MSG12()
            elif ( MSG == "13" ): self._MSG13()

    
    def _MSG1( self ):
        print( f"" )
        print( f"=" * 80 )
        print( f"\033[KTarget Position\n" )

        Ascent_pos = array(
            list( map( float64, input( f"\033[KAscent position\n>>> " ).split() ) )
        )

        divert_dist = array(
            list( map( float64, input( f"\033[Kdivert distance\n>>> " ).split() ) )
        )

        print( f"\033[K\033[A" * 5 )
        print( f"\033[KAscent position: {Ascent_pos}" )
        print( f"\033[Kdivert distance: {divert_dist}" )
        print( f"" )

        txbf = zeros(17, dtype=uint8 )
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
            f"\033[Kecho >>> ",
            ( frombuffer( data[2:14], int16) * RXRESOLUTION[POS_RES] ).astype(float64)
        )

        print( f"=" * 80 )
        print( f"" )

        self.MSG1 = True


    def _MSG5( self ):
        print( f"" )
        print( f"=" * 80 )
        print( f"\033[KThrust Command\n" )

        txbf = zeros( 17, dtype=uint8 )
        txbf[0] = txh0_L_TO_1
        txbf[1] = txh1_L_TO_1
        txbf[3] = 5

        Mode = input( f"\033[KAutomatic of Manual?\n>>> " )

        if ( Mode == "auto" ):
            ThrustProfile = load( './HY_scenario.npy' )[80:]
            for ThrustCMD in ThrustProfile:
                txbf[4:6] = frombuffer(
                    ( ThrustCMD * TXRESOLUTION[THR_RES] ).astype(uint16).tobytes(), uint8
                )
                self.packet.write( txbf )
                sleep( 0.02 )
        else:
            ThrustCMD = float64( input( f"\033[KThrust Command in N \n>>> " ) )
            txbf[4:6] = frombuffer(
                ( ThrustCMD * TXRESOLUTION[THR_RES] ).astype(uint16).tobytes(), uint8
            )
            self.packet.write( txbf )

        
    def _MSG6( self ):
        print( f"" )
        print( f"=" * 80 )
        print( f"\033[KThrust Command\n" )

        ThrustCMD = float64( input( f"\033[KThrust Command in % \n>>> " ) )
        RCSCMD    = array(
            list( map( int, input( f"\033[KRCS Command\n>>> " ).split() ) )
        )

        print( f"\033[K\033[A" * 5 )
        print( f"\033[KThrust Command: {ThrustCMD}" )
        print( f"\033[KRCS Command   : {RCSCMD}" )

        txbf = zeros( 17, dtype=uint8 )
        txbf[0] = txh0_L_TO_1
        txbf[1] = txh1_L_TO_1
        txbf[3] = 6

        txbf[4:6] = frombuffer(
            ( ThrustCMD * TXRESOLUTION[THC_RES] ).astype(uint16).tobytes(), uint8
        )
        txbf[6] = uint8( RCSCMD[0] )
        txbf[7] = uint8( RCSCMD[1] )
        txbf[8] = uint8( RCSCMD[2] )
        txbf[9] = uint8( RCSCMD[3] )

        self.packet.write( txbf )

        print( f"=" * 80 )
        print( f"" )

    
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
        print( f"" )
        print( f"=" * 80 )
        print( f"\033[KControl Authority\n" )

        Authority = array(
            list( map( int, input( f"\033[KTVC, RCS, FCV >>> " ).split() ) )
        )

        print( f"\033[K\033[A" * 2 )
        print( f"\033[KTVC: {Authority[0]}" )
        print( f"\033[KRCS: {Authority[1]}" )
        print( f"\033[KFCV: {Authority[2]}" )

        txbf = zeros( 17, dtype=uint8 )
        txbf[0] = txh0_L_TO_1
        txbf[1] = txh1_L_TO_1
        txbf[3] = 11

        txbf[4] = Authority[0]
        txbf[5] = Authority[1]
        txbf[6] = Authority[2]

        self.packet.write( txbf )

        print( f"=" * 80 )
        print( f"" )


    def _MSG12( self ):
        print( f"" )
        print( f"=" * 80 )
        print( f"\033[KMission Number\n" )

        MissionNumber = input( f"\033[KMission Number\n>>> " )

        txbf = zeros( 17, dtype=uint8 )
        txbf[0] = txh0_L_TO_1
        txbf[1] = txh1_L_TO_1
        txbf[3] = 12

        txbf[4] = MissionNumber

        self.packet.write( txbf )

        print( f"=" * 80 )
        print( f"" )


    def _MSG13( self ):
        print( f"" )
        print( f"=" * 80 )
        print( f"\033[KIgnition Flag\n" )

        Ignite = input( f"\033[KIgnite Flag\n>>> " )
        CutOff = input( f"\033[KCutoff Flag\n>>> " )

        print( f"\033[K\033[A" * 5 )
        print( f"\033[KIgnite Flag: {Ignite}" )
        print( f"\033[KCutoff Flag: {CutOff}" )

        txbf = zeros( 17, dtype=uint8 )
        txbf[0] = txh0_L_TO_1
        txbf[1] = txh1_L_TO_1
        txbf[3] = 13

        txbf[4] = Ignite
        txbf[5] = CutOff

        self.packet.write( txbf )

        print( f"=" * 80 )
        print( f"" )

    
    def _echo( self ):

        self.packet.timeout = 1

        if ( frombuffer( self.packet.read(), uint8 ) == txh1_L_TO_1 ):
            if ( frombuffer( self.packet.read(), uint8 ) == txh0_L_TO_1 ):
                return self.packet.read( 15 )

        print( f"cannot receive echo from GCCM1" )
        
        return zeros( 17, dtype=uint8 )