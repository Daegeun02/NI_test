from numpy import load, linspace

import matplotlib.pyplot as plt



data = load( "./log/log_2차.npy" )

fig = plt.figure( figsize=(10,3) )

ax1 = fig.add_subplot( 131 )
ax2 = fig.add_subplot( 132 )
ax3 = fig.add_subplot( 133 )

LOX = data[3][(data[3,:] > 300) & (data[3,:] < 1000)]
tim = linspace( 0, len(LOX)/100, len(LOX) )

ax1.plot( tim, LOX, label="LOX Tank Pressure" )
ax1.tick_params( axis='both', labelsize=7 )
ax1.legend( fontsize=7 )
ax1.grid()

LNG = data[4][(data[4,:] > 300) & (data[4,:] < 1000)]
tim = linspace( 0, len(LNG)/100, len(LNG) )

ax2.plot( tim, LNG, label="LNG Tank Pressure" )
ax2.tick_params( axis='both', labelsize=7 )
ax2.legend( fontsize=7 )
ax2.grid()

GN2 = data[5][(data[5,:] > 500) & (data[5,:] < 5000)]
tim = linspace( 0, len(GN2)/100, len(GN2) )

ax3.plot( tim, GN2, label="GN2 Tank Pressure" )
ax3.tick_params( axis='both', labelsize=7 )
ax3.legend( fontsize=7 )
ax3.grid()

fig.savefig( "./image/log_2차.png" )