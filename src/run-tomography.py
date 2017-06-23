"""
A wrapper for the main tomography script.
"""

# Author : Sangeeta Bhatia

import pymc as pm
import tomography as tm
from pymc.Matplot import plot
from os import rename
import sys

runs = int(input("Enter the number of iterations for the MCMC simulation: "))
burnin = int(input("Enter the burn in for the MCMC simulation: "))
thin = int(input("Enter the thining variable for the MCMC simulation: "))
S = pm.MCMC(tm)
S.sample(runs, burnin, thin)
stats = S.stats()
S.write_csv("summary.csv", variables=['Q', 'tau'])
plot(S) # Automatically saves the output - one .png file for each variable.

#Finally
fname = sys.argv[1]
sname = fname + '-summary.csv'
qname = fname + '-Q.png'
tname = fname + '-tau.png'
rename("summary.csv", sname)
rename("Q.png", qname)
rename("tau.png", tname)