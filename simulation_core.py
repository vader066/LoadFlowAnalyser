import nr_models as nr
import numpy as np
import sympy as sp


#Function for calculating the Mismatch vector. 
# Takes in arguments: 
# Vector of specified values:
# delta vector for angles of V
# Voltage vector
# Admittance Matrix

# NOTE!!!: The vector of specified values MUST not be a normal array. It should be an
#instance of the Kvector class 'filled' with objects of the specified values


def MismatchV(spec, D, V, Y):
  # Initialized empty Vector for calculated Values of P and Q's 
  calc = nr.Kvector()

  #Calculating for Quantities corresponding to the same quantities in the specified vector
  for qty in spec.data:
    if qty.type == "P":
      val = nr.calc_P_i(qty.bus, D, V, Y)
    elif qty.type == "Q":
      val = nr.calc_Q_i(qty.bus, D, V, Y)
      
    entry = nr.Qty(qty.type, qty.bus, val)
    calc.push(entry) 
  # print(calc)

  #NOTE!! This function returns the kVector object, mismatch, initialized below  
  mismatch = nr.Kvector()

  #Calculating differences between specified data and calculated data
  order = len(calc.data)    
  for i in range(order):
    qty_cal = calc.data[i]
    qty_spec = spec.data[i]
    calc_val = qty_spec.value - qty_cal.value
    entry = nr.Qty(qty_cal.type, qty_cal.bus, calc_val)
    mismatch.push(entry)
    
  
    
  return mismatch



def Jacobian(Kvector, Uvector, D, V, Y):
  JacobV = np.empty(0)
  for qty in Kvector.data:
    i = qty.bus
    
    #Generating the buses numbers for variables in the equation of each Known Value
    j_indices = [idx + 1 for idx in range(len(Kvector.data)) ]
  
    
    # Dynamically defining variables of corresponding buses
    Vi = sp.symbols(f"V{i}")
    Vj = [sp.symbols(f"V{j}") for j in j_indices]
    Di = sp.symbols(f"D{i}")
    Dj = [sp.symbols(f"D{j}") for j in j_indices]
    
    #Funtion definition for Generating function for Known vector quantity Pi or Qi
    def generate_p_function(Vi, Vj, Di, Dj):
      summation_term = sum(Vj[k] * np.abs(Y[i-1, k]) * sp.cos(np.angle(Y[i-1, k]) + Dj[k] - Di) for k in range(len(Vj)))
      full = Vi * summation_term
      return full
    
    def generate_q_function(Vi, Vj, Di, Dj):
      summation_term = sum(Vj[k] * np.abs(Y[i-1, k]) * sp.sin(np.angle(Y[i-1, k]) + Dj[k] - Di) for k in range(len(Vj)))
      full = -Vi * summation_term
      return full
      
    #Generating the function of the Known Quantity
    if qty.type == 'P':
      func = generate_p_function(Vi, Vj, Di, Dj)
    elif qty.type == 'Q':
      func = generate_q_function(Vi, Vj, Di, Dj)
    
    
    #Differentiating the function with respect to 
    for qty in Uvector.data:       
      var = sp.symbols(f"{qty.type}{qty.bus}")  # determining the independent variables for differentiation for each iteration
      diff = sp.diff(func, var)
      
      # Generating values for substitution 
      subs = {}
      
      for item in range(len(V)):      #Values of vector V
        sub = {f'V{item + 1}': V[item]}
        subs.update(sub)
        
      for item in range(len(D)):      #Values of vector Delta
        sub = {f'D{item + 1}': D[item]}
        subs.update(sub)
        
      eval_val = float(diff.subs(subs))
      JacobV = np.append(JacobV, eval_val)
      n = len(V)
      
  JacobM = JacobV.reshape(n, n)
  return JacobM


#updates the Uvector, the Delta vector and the V vector

def update(init, D, V):
    for obj in init.data:
      if obj.type == 'D':
        D[obj.bus -1 ] = obj.value
      elif obj.type == 'V':
        V[obj.bus -1] = obj.value



def NR(max_iters, spec, init, D, V, Y ):
  #tolerance
  tol=1e-6
  
  #iterations
  for i in range(max_iters):
    mismatch = MismatchV(spec, D, V, Y)
    jacob = Jacobian(spec, init, D, V, Y)
    x_curr = nr.eval(init, jacob, mismatch) 
    print(x_curr[0])
    update(x_curr[0], D, V) 
    
    # Check for convergence
    if np.linalg.norm(x_curr[1]) < tol:
        print(f"Converged in {i+1} iterations.")
        return x_curr[0]
    
  raise ValueError("Newton-Raphson did not converge within the maximum number of iterations.")
    
  

  
  