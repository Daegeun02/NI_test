from threading import Thread

from time import sleep



class TEST( Thread ):
    
    def __init__( self ):

        super().__init__()

        self.daemon = True
        self.end    = True

        self.i = 0
        self.j = 0

    
    def run( self ):

        print( f"\n" * 4 )
        i = 0

        while self.end:
            print( f"\033[A" * 6 )
            print( f"\033[Kasdfasdf{i}" )
            print( f"\033[B" * 3 )

            sleep( 0.5 )

            i += 1

    def chop( self ):
        
        print( f"\033[K\033[Aasdfasdf{self.j}" )
        self.j += 1


if __name__ == "__main__":

    test = TEST()

    test.start()

    t = 0

    while t < 5:
        t += 1

        test.chop()

        sleep( 1 )

    test.end = False
    test.join()