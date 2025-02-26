#!/usr/bin/env python

import freegs
import matplotlib.pyplot as plt

#########################################
# Create the machine, which specifies coil locations
# and equilibrium, specifying the domain to solve over

JT60SA = freegs.machine.JT60SA()

eq = freegs.Equilibrium(tokamak=JT60SA,
                        Rmin=1.00, Rmax=6.00,    # Radial domain
                        Zmin=-4.5, Zmax=4.5 ,   # Height range
                        nx=65, ny=65)          # Number of grid points


#########################################
# Plasma profiles

profiles = freegs.jtor.ConstrainPaxisIp(eq,
                                        1.69819e5, # Plasma pressure on axis [Pascals]
                                        -2.3e6, # Plasma current [Amps]
                                        -5.11, # vacuum f = R*Bt with R = 2.96 m, Bt = 2.25 T
                                        alpha_m=4.0,
                                        alpha_n=2.0,
                                        Raxis =2.97) 

#########################################
# Coil current constraints
#
# Specify locations of the X-points
# to use to constrain coil currents

xpoints = [(2.3, -2.2)]   # (R,Z) locations of X-points
isoflux = [(2.3, -2.2, 4.1, -0.0), (2.3, -2.2, 1.86, 0.35), (2.3, -2.2, 2.0, 1.64), (2.3, -2.2, 2.54, 2.05), (2.3, -2.2, 3.0, 1.8)]
#psivals = [ (1.86, 0.30, 0.0), (4.0, 0.30, 0.0)]
#current_limits = [(-200000.0, 200000.0), (-200000.0, 200000.0), (-200000.0, 200000.0), (-200000.0, 200000.0), (-200000.0, 200000.0), (-200000.0, 200000.0), (-200000.0, 200000.0), (-200000.0, 200000.0), (-200000.0, 200000.0), (-200000.0, 200000.0)]

#constrain = freegs.control.constrain(xpoints=xpoints, isoflux=isoflux, psivals=psivals)
constrain = freegs.control.constrain(xpoints=xpoints, isoflux=isoflux)
constrain(eq)

#########################################
# Nonlinear solve
freegs.solve(eq,          # The equilibrium to adjust
             profiles,    # The plasma profiles
             constrain,   # Plasma control constraints
             show=True)   # Shows results at each nonlinear iteration

# eq now contains the solution

print("Done!")

print("Plasma current: %e Amps" % (eq.plasmaCurrent()))
print("Pressure on axis: %e Pascals" % (eq.pressure(0.0)))
print("Plasma poloidal beta: %e" % (eq.poloidalBeta()))
print("Plasma volume: %e m^3" % (eq.plasmaVolume()))

eq.tokamak.printCurrents()

# plot equilibrium
axis = eq.plot(show=False)
JT60SA.plot(axis=axis, show=False)
#constrain.plot(axis=axis, show=True)

# Safety factor
# plt.plot(*eq.q())
# plt.xlabel(r"Normalised $\psi$")
# plt.ylabel("Safety factor")
# plt.grid()
# plt.show()

##############################################
# Save to geqdsk file

from freegs import geqdsk

with open("jt60sa.geqdsk", "w") as f:
    geqdsk.write(eq, f)

# Call matplotlib show so plot pauses
plt.show()
