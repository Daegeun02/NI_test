from numpy import load

date = input( "date >>> " )

data = load( f"./log/{date}.npy" )

print( data )
