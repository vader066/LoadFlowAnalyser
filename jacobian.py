import sympy as sp
import powerclasses as pc
from powerclasses import rect
import numpy as np


# D, V, P = sp.symbols('D V P', real = True)

# f = 4*D**2*V + 2*V**3*D

# print(sp.diff(f, D))


def Jacobian(Kvector, Y):
  for obj in Kvector.data:
    i = obj.bus
    
    #Generating the buses numbers for variables in the equation of each Known Value
    j_indices = [idx + 1 for idx in range(len(Kvector.data)) ]
  
    
    # Dynamically defining variables of corresponding buses
    Vi = sp.symbols(f"V{i}")
    Vj = [sp.symbols(f"V{j}") for j in j_indices]
    Di = sp.symbols(f"D{i}")
    Dj = [sp.symbols(f"D{j}") for j in j_indices]
    
    def generate_function(Vi, Vj, Di, Dj):
      summation_term = sum(Vj[k] * np.abs(Y[i-1, k]) * sp.cos(np.angle(Y[i-1, k]) + Dj[k] - Di) for k in range(len(Vj)))
      full = Vi * summation_term
      print(full)
      return full
      
    
    f = generate_function(Vi, Vj, Di, Dj)
    diff = sp.diff(f, Vj[0] )
    print(diff)
  
  return diff


specified = pc.Kvector()
P2 = pc.Qty("P", 2, 0.5)
P3 = pc.Qty("P", 3, -1.5)
Q2 = pc.Qty("Q", 2, 1.0)
specified.push(P2)
specified.push(P3)
specified.push(Q2)

Y_matrix = np.array([[rect(24.23, -75.95), rect(12.13, 104.04), rect(12.13, 104.04)],
                     [rect(12.13, 104.04), rect(24.23, -75.95), rect(12.13, 104.04)],
                     [rect(12.13, 104.04), rect(12.13, 104.04), rect(24.23, -75.95)]],
                    dtype=np.complex64)

print(np.abs(Y_matrix[0, 0]))
Jacobian(specified, Y_matrix)