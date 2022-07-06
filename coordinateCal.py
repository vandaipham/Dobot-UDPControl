# Program to plot a Circle
# using Center-Radius form of circle equation
 
import numpy as np
import matplotlib.pyplot as plt
import csv

my_formatter = "{0:.4f}"

theta = np.linspace( 0 , 2 * np.pi , 150)
 
radius = 20
 
a = np.around(radius * np.cos( theta ) + 253, decimals=2)

b = np.around(radius * np.sin( theta ), decimals=2)
 
figure, axes = plt.subplots( 1 )
 
axes.plot( a, b )
axes.set_aspect( 1 )

header = ['X', 'Y', 'Z']
z = -59

with open('Coordinates.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    #writer.writerow(header)
    writer.writerow([260, -25, -20])
    for i in range(0, len(a)):
        writer.writerow([a[i], b[i], z])
    
    writer.writerow([260, -25, -20])

plt.title( 'Parametric Equation Circle' )
plt.grid(True)
plt.show()