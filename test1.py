import nr_models as nr
from simulation_core import NR
from nr_models import rect
import numpy as np

#Test Values

#This is how to create and populate the specified vector of knowns
#First Create the Quantites that belong in this vector and then add them to the vector
spec = nr.Kvector()
P2 = nr.Qty("P", 2, 0.5)
P3 = nr.Qty("P", 3, -1.5)
Q2 = nr.Qty("Q", 2, 1.0)
spec.push(P2)
spec.push(P3)
spec.push(Q2)


#ITERATION 1

init = nr.Uvector()
D2 = nr.Qty("D", 2, 0)
D3 = nr.Qty("D", 3, 0)
V2 = nr.Qty("V", 2, 1)
init.push(D2)
init.push(D3)
init.push(V2)

v = np.array([1.04, 1, 1.04], dtype=np.float32) 

# d =np.array([0, 0, 0])
d =np.array([0, 0, 0], dtype=np.float32)

# class Vmat:

#Example use of the rect function to add polar values directly to the admittance matrix
Y = np.array([[rect(24.23, -75.95), rect(12.13, 104.04), rect(12.13, 104.04)],
                     [rect(12.13, 104.04), rect(24.23, -75.95), rect(12.13, 104.04)],
                     [rect(12.13, 104.04), rect(12.13, 104.04), rect(24.23, -75.95)]],
                    dtype=np.complex64)

#NOTE: TEST VALUES WERE TAKEN FROM THE EXAMPLE 6 QUESTION IN THE SLIDES: UNIT ONE, SLIDE 86
  

#Test  

nr = NR(50, spec, init, d, v, Y)
print(f'NR result: {nr}')
  