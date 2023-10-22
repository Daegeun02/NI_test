from threading import Thread

import sys

from serial import Serial

from _interface import Interface

from _resolution import *

from _dataHYE import DataHYE

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

    def __init__( self, packet: Serial, thread: Thread, DB: DataHYE, interface: Interface ):

        super().__init__()

        self.interface = interface

        self.daemon = True
        self.packet = packet
        self.thread = thread
        self.DB     = DB

        self.MSG1 = False
        self.MSG5 = False
        self.MSG6 = False
        self.MSG9 = False

        self.MSG11 = 0
        self.MSG12 = 0
        self.MSG13 = 0

        sleep( 1 )


    def run( self ):
        
        interface = self.interface
        interface.start()

        sleep( 0.5 )

        while ( not (
            self.MSG1 and self.MSG6 and self.MSG9
        ) ):
            interface.lock = False

            interface.previous['MSG9'] = self.MSG1 and self.MSG9

            MSG = input( "\033[K   <<< select command you want" )

            interface.lock = True

            interface.clean( 34 )

            print( f"\033[KMSG ID: {MSG}" )

            sleep( 1 )

            interface.clean( 2 )

            if ( MSG == "exit" ):
                print( f"Exit Process\033[E" )

                self.MSG1 = True
                self.MSG6 = True
                self.MSG9 = True

                sys.exit()

            elif ( MSG == "1" ): self._MSG1()
            elif ( MSG == "5" ): self._MSG5()
            elif ( MSG == "6" ): self._MSG6()
            elif ( MSG == "7" ): self._MSG7()
            elif ( MSG == "8" ): self._MSG8()
            elif ( MSG == "9" ): self._MSG9()

            elif ( MSG == "11" ): self._MSG11()
            elif ( MSG == "12" ): self._MSG12()
            elif ( MSG == "13" ): self._MSG13()

            else: self.interface.print_margin( 31 )

    
    def _MSG1( self ):
        interface = self.interface
        
        interface.MSG_enter_interface( "Target Position" )

        Ascent_pos  = interface.MSG_input_interface( "Ascent position" )
        divert_dist = interface.MSG_input_interface( "divert distance" )

        interface.clean( 5 )

        self.interface.previous['MSG1'][0:3] = Ascent_pos
        self.interface.previous['MSG1'][3:6] = divert_dist

        interface.MSG_check_interface( "Ascent position", Ascent_pos  )
        interface.MSG_check_interface( "divert distance", divert_dist )

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

        interface.clean( 3 )

        interface.print_margin( 27 )

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
        interface = self.interface

        interface.MSG_enter_interface( "Thrust Command" )

        ThrustCMD = interface.MSG_input_interface( "Thrust Command in %" )
        RCSCMD    = interface.MSG_input_interface( "RCS Command" )

        interface.clean( 5 )

        self.interface.previous['MSG6'][ 0 ] = ThrustCMD
        self.interface.previous['MSG6'][1:5] = RCSCMD

        interface.MSG_check_interface( "Thrust Command", ThrustCMD )
        interface.MSG_check_interface( "RCS Command   ", RCSCMD )

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

        interface.print_margin( 25 )

    
    def _MSG7( self ):
        txbf = zeros( 17, dtype=uint8 )
        txbf[0] = txh0_L_TO_1
        txbf[1] = txh1_L_TO_1
        txbf[3] = 7

        self.packet.write( txbf )

        self.MSG1 = False
        self.MSG9 = False

        self.interface.initialize_previous()

        self.interface.print_margin( 31 )


    def _MSG8( self ):
        interface = self.interface
        
        interface.MSG_enter_interface( "Actuator Command" )

        command = interface.MSG_input_interface( "command x, y" )

        interface.clean( 3 )

        interface.previous['MSG8'] = command

        interface.MSG_check_interface( "x", command[0] )
        interface.MSG_check_interface( "y", command[1] )

        txbf = zeros( 17, dtype=uint8 )
        txbf[0] = txh0_L_TO_1
        txbf[1] = txh1_L_TO_1
        txbf[3] = 8

        txbf[4:8] = frombuffer(
            ( command * TXRESOLUTION[ACT_RES] ).astype(uint16).tobytes(), uint8
        )

        self.packet.write( txbf )

        self.interface.print_margin( 25 )

    
    def _MSG9( self ):
        txbf = zeros( 17, dtype=uint8 )
        txbf[0] = txh0_L_TO_1
        txbf[1] = txh1_L_TO_1
        txbf[3] = 9

        self.packet.write( txbf )

        self.MSG9 = True

        self.interface.print_margin( 31 )

    
    def _MSG11( self ):
        interface = self.interface

        interface.MSG_enter_interface( "Control Authority" )

        Authority = interface.MSG_input_interface( "TVC, RCS, FCV" )

        interface.clean( 3 )

        interface.previous['MSG11'] = Authority

        interface.MSG_check_interface( "TVC", Authority[0] )
        interface.MSG_check_interface( "RCS", Authority[1] )
        interface.MSG_check_interface( "FCV", Authority[2] )

        txbf = zeros( 17, dtype=uint8 )
        txbf[0] = txh0_L_TO_1
        txbf[1] = txh1_L_TO_1
        txbf[3] = 11

        txbf[4] = Authority[0]
        txbf[5] = Authority[1]
        txbf[6] = Authority[2]

        self.packet.write( txbf )

        interface.print_margin( 24 )


    def _MSG12( self ):
        interface = self.interface

        interface.MSG_enter_interface( "Mission Number" )

        MissionNumber = interface.MSG_input_interface( "Mission Number" )

        interface.clean( 3 )

        interface.previous['MSG12'] = MissionNumber

        interface.MSG_check_interface( "Mission Number", MissionNumber )

        txbf = zeros( 17, dtype=uint8 )
        txbf[0] = txh0_L_TO_1
        txbf[1] = txh1_L_TO_1
        txbf[3] = 12

        txbf[4] = MissionNumber

        self.packet.write( txbf )

        interface.print_margin( 26 )


    def _MSG13( self ):
        interface = self.interface

        interface.MSG_enter_interface( "Ignition Flag" )

        Ignite = interface.MSG_input_interface( "Ignite Flag" )
        CutOff = interface.MSG_input_interface( "Cutoff Flag" )

        interface.clean( 5 )

        interface.previous['MSG13'][0] = Ignite
        interface.previous['MSG13'][1] = CutOff

        interface.MSG_check_interface( "Ignite Flag", Ignite )
        interface.MSG_check_interface( "Cutoff Flag", CutOff )

        txbf = zeros( 17, dtype=uint8 )
        txbf[0] = txh0_L_TO_1
        txbf[1] = txh1_L_TO_1
        txbf[3] = 13

        txbf[4] = Ignite
        txbf[5] = CutOff

        self.packet.write( txbf )

        interface.print_margin( 25 )

    
    def _echo( self ):

        self.packet.timeout = 1

        if ( frombuffer( self.packet.read(), uint8 ) == txh1_L_TO_1 ):
            if ( frombuffer( self.packet.read(), uint8 ) == txh0_L_TO_1 ):
                return self.packet.read( 15 )

        return zeros( 17, dtype=uint8 )