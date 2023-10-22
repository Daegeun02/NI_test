from threading import Thread

from _dataHYE import DataHYE

from numpy import zeros, array
from numpy import float64

from time import sleep



class Interface( Thread ):
    
    def __init__( self, DB: DataHYE ):

        super().__init__()

        self.daemon = True

        self.previous = {
            'MSG1' : zeros(6),
            'MSG5' : 0,
            'MSG6' : zeros(5),
            'MSG7' : 0,
            'MSG8' : zeros(2),
            'MSG9' : 0,
            'MSG11': zeros(3),
            'MSG12': 0,
            'MSG13': zeros(2),
            'echo': zeros(6)
        }

        self.lock = False
        self.working = True
        self.DB = DB

    
    def run( self ):

        print( f"\n" * 31 )

        DB = self.DB

        while self.working:

            if ( ( not self.lock ) and DB.flag ):
                i = DB.idxn-1

                print( f"\033[A" * 33 )

                print( f"\033[K<Engine>" )
                print( f"\033[KIF: {DB.IF[0,i]} CF: {DB.CF[0,i]} IR: {DB.IR[0,i]} IT: {DB.IT[0,i]} IE: {DB.IE[0,i]} St: {DB.St[0,i]} Ti: {DB.Ti[0,i]}" )
                print( f"\033[K<TVC>" )
                print( f"\033[KRq: {DB.TVC[0,i]} Ca: {DB.TVC[1,i]} Au: {DB.TVC[2,i]}" )
                print( f"\033[K<RCS>" )
                print( f"\033[KRq: {DB.RCS[0,i]} Ca: {DB.RCS[1,i]} Au: {DB.RCS[2,i]}" )
                print( f"\033[K<TVC>" )
                print( f"\033[KRq: {DB.FCV[0,i]} Ca: {DB.FCV[1,i]} Au: {DB.FCV[2,i]}" )
                print( f"\033[K<Ascent position>" )
                print( f"\033[K{DB.Ascent_pos[:,i]}" )
                print( f"\033[K<Actuator>" )
                print( f"\033[KCMD: {DB.act_CMD[:,i]} RES: {DB.act_RES[:,i]}" )
                print( f"\033[K<Tank>" )
                print( f"\033[KLOX: {DB.Tank[0,i]} LNG: {DB.Tank[1,i]} GN2: {DB.Tank[2,i]}" )
                print( f"\033[K<FCV>" )
                print( f"\033[KLOX: {DB.FCV[3,i]} LNG: {DB.FCV[4,i]}" )
                print( f"\033[K<Thrust Command>" )
                print( f"\033[K{DB.Thrust_CMD[0,i]}" )
                print( f"\033[K<RCS value>" )
                print( f"\033[K{DB.RCS_value[0:4,i]}" )
                print( f"\033[K{DB.RCS_value[4:8,i]}" )

                self.print_GCS_interface()

                DB.flag = False

    
    def initialize_previous( self ):
        self.previous['MSG1']  = zeros(6)
        self.previous['MSG5']  = 0
        self.previous['MSG6']  = zeros(6)
        self.previous['MSG7']  = 0
        self.previous['MSG8']  = zeros(2)
        self.previous['MSG9']  = 0
        self.previous['MSG11'] = zeros(3)
        self.previous['MSG12'] = 0
        self.previous['MSG13'] = zeros(2)
        self.previous['echo']  = zeros(6)


    def print_GCS_interface( self ):

        print( f"\033[K" )

        print( f"\033[K    ID       STATUS                      PREVIOUS" )
        print( f"\033[K1 : MSG1  => Target Position             {self.previous['MSG1']} , echo: {self.previous['echo']} " )
        print( f"\033[K5 : MSG5  => Thrust Command              {self.previous['MSG5']} " )
        print( f"\033[K6 : MSG6  => Control Command             {self.previous['MSG6']} " )
        print( f"\033[K7 : MSG7  => RESET                       {self.previous['MSG7']} " )
        print( f"\033[K8 : MSG8  => Actuator Command            {self.previous['MSG8']} " )
        print( f"\033[K9 : MSG9  => Launch Sign                 {self.previous['MSG9']} " )
        print( f"\033[K11: MSG11 => Control Authority           {self.previous['MSG11']}" )
        print( f"\033[K12: MSG12 => Mission Number              {self.previous['MSG12']}" )
        print( f"\033[K13: MSG13 => Ignition Flag               {self.previous['MSG13']}" )

    
    def MSG_enter_interface( self, MSG ):
        print( f"" )
        print( f"=" * 80 )
        print( f"\033[K{MSG}\n" )

    
    def MSG_input_interface( self, MSG ):

        _input = array(
            list( map( float64, input( f"\033[K{MSG}\n>>> " ).split() ) )
        )

        return _input

        
    def MSG_check_interface( self, MSG, data ):

        print( f"\033[K{MSG}: {data}" )

    
    def MSG_clean_interface( self, n ):
        
        print( f"=" * 80 )
        print( f"" )

        sleep( 1 )

        self.clean( n )

    
    def print_margin( self, n ): print( f"\n" * n )

    def clean( self, n ): print( f"\033[K\033[A" * n )