#---------------------THE BEGINNING---------------------#
#-- programmer : angga ---------------------------------#
#-- For learning Python, Numpy, Tensorflow and Scipy ---#
#-------------------------------------------------------#

import numpy as nm
import numpy.random as rad
from scipy.optimize import curve_fit

#------------------BASIC CALCULATION------------------#

ar1 = nm.arange(100)
ar2 = nm.zeros((2,2,2))
ar3 = nm.array(ar1)
ar4 = nm.linspace(0, 1, 50)
ar5 = nm.reshape(ar4, (5,5,2))
ar6 = rad.random(10)

#-------------TEXT-----------------------#

#txt1 = open('test1.txt', 'r')

#print (txt1)
#txt1.close()

#-------------MATRIX---------------------#

A = nm.matrix([[2,-3,4],
                [-3,5,6],
                [1,6,8]])
B = nm.matrix([[10],
                [3],
                [2]])

C = A ** (-1) * B

#print(B)