import numpy as np
import bisect




#Class for the various quantites of interest for Load flow studies [P, Q, V, D]
class Qty:
  def __init__(self, type, bus, value ):
    self.bus = bus
    self.type = type
    self.value = value
    
  @property
  def type(self):
    return self._type
  
  @type.setter
  def type(self, val):
    types = ['P', 'Q', 'D', 'V']
    if not val:
      raise ValueError("type cannot be empty")
    elif val.upper() not in types:
      raise ValueError("Invalid Type. Type must be: [P, Q, D, V]")
    self._type = val.upper()
  
  @property
  def bus(self):
    return self._bus
  
  @bus.setter
  def bus(self, val):
    if not val:
      raise ValueError("bus cannot be empty")
    elif not isinstance(val, int) or val < 0:
      raise ValueError("Value must be a positive Integer")
    self._bus = val
    
  @property 
  def value(self):
    return self._value
  
  @value.setter
  def value(self, val):
    self._value = val
    
    
    



# Class for the Vector of Known Quantities
class Kvector:
  def __init__(self):
    self.data = []
    
  #adds quantities objects to the vector but ensures they are only of type P and Q and arranges them in the right order
  def push(self, qty):
    types = ['P', 'Q']
    if not isinstance(qty, Qty):
      raise TypeError(f'Expected a Qty object, but got {type(qty).__name__} instead.')
    if qty.type.upper() not in types:
      raise TypeError("cannot add V or D quantities to Vector of Knowns")
    
    # Rest of the code below is for sorting Vector so that P's come before Q's and they are arranged in ascending order of bus numbers
    
    type_order = {'P': 0, 'Q': 1}
    new_entry = (type_order[qty.type], qty.bus)
        
    # Using bisect to find the correct insertion index
    sortable_entries = [(type_order[obj.type], obj.bus) for obj in self.data]
    index = bisect.bisect_left(sortable_entries, new_entry)
    self.data.insert(index, qty)
    
    
  #for displaying the array in a user-friendly way in the console when you print objects of the class
  def __repr__(self):
    return repr([f"{qty.type}{qty.bus}: {qty.value}" for qty in self.data])
    
    


    
    
# Class for the Vector of Unknown Quantities
class Uvector:
  def __init__(self):
    self.data = []
    
  #adds quantities to the unknown vector but ensures they are only of type V and D and arranges them in the right order
  def push(self, qty):
    types = ['V', 'D']
    if not isinstance(qty, Qty):
      raise TypeError(f'Expected a Qty object, but got {type(qty).__name__} instead.')
    if qty.type.upper() not in types:
      raise TypeError("cannot add P or Q quantities to Vector of Unknowns")
    
    # For sorting the Vector so that D's come before V's and they are arranged in ascending order of bus numbers
    type_order = {'D': 0, 'V': 1}
    new_entry = (type_order[qty.type], qty.bus)
        
    # Using bisect to find the correct insertion index
    sortable_entries = [(type_order[obj.type], obj.bus) for obj in self.data]
    index = bisect.bisect_left(sortable_entries, new_entry)
    self.data.insert(index, qty)
    
    
  #for displaying the array in a user-friendly way in the console
  def __repr__(self):
    return repr([f"{qty.type}{qty.bus}: {qty.value}" for qty in self.data])
    



 
#Function to calculate P. Takes arguments of the bus, delta vector, Voltage vector and Addmittance matrix
def calc_P_i(bus, D, V, Y):
  i = bus-1  # Index for P_i
  
  #Checks arrays to ensure they are of matching order
  if D.shape != V.shape:
    raise TypeError("V matrix and D matrix must have the same order")
  elif len(Y) != len(V) and len(Y[0] != len(V)):
    raise TypeError(f"Admittance matrix must be a {len(V)} by {len(V)} matrix")

  sum_term = 0
  for j in range(len(V)):
    #computing summation terms first
    cos_term = np.cos(np.angle(Y[i, j]) + D[j] - D[i])
    sum_term += V[j] * np.abs(Y[i, j]) * cos_term
  P_i = V[i] * sum_term   #multiplying summation term with V  
  
  return P_i

  
#Function to calculate Q. Takes the same arguments as for P above
def calc_Q_i(bus, D, V, Y):
  i = bus-1  # Index for Q_i
  
  #Checks arrays to ensure they are of matching order
  if D.shape != V.shape:
    raise TypeError("V matrix and D matrix must have the same order")
  elif len(Y) != len(V) and len(Y[0] != len(V)):
    raise TypeError(f"Admittance matrix must be a {len(V)} by {len(V)} matrix")

  sum_term = 0
  for j in range(len(V)):      
    #computing summation terms first
    cos_term = np.sin(np.angle(Y[i, j]) + D[j] - D[i])
    sum_term += V[j] * np.abs(Y[i, j]) * cos_term

  Q_i = -V[i] * sum_term   #multiplying summation term with V
    
  return Q_i


#Evaluates the new value: X + delta_x

def eval(initial, Jacob, mismatch):
  # Check if the Jacobian is singular
  if np.linalg.matrix_rank(Jacob) < Jacob.shape[0]:
      raise ValueError("Jacobian is singular, cannot proceed with Newton-Raphson iteration.")   
    
  # converting vector objects into numerical arrays 
  mism = arrify(mismatch)
  x_prev = arrify(initial)
  
  #Evaluating Xk+1
  invJacob = np.linalg.inv(Jacob)
  delta_x = np.matmul(invJacob, mism)  
  x_curr = x_prev + delta_x
  x_curr_obj = vectorfy(x_curr, initial)

  return (x_curr_obj, delta_x)    #returns the result of the current iteration and the delta_x (to be used for convergence)


#This function converts values from polar form to rectangular form for calculations
#It takes arguments of the magnitude and angle in degrees
def rect(r, theta):
  real = r*np.cos(np.radians(theta))
  img = r*np.sin(np.radians(theta))
  result = real + img*1j
  return result

    
# transforms the initial vector object 
# into an array of values for mathematical computation
def arrify(vector):
  array = []
  for obj in vector.data:
    array.append(obj.value)
  return np.array(array) 

# transforms the resulting array of the computation 
# into the Uvector object to be returned
def vectorfy(array, vector):
  new_Vector = Uvector()
  i = 0
  for obj in vector.data:
    obj.value = array[i]
    new_Vector.push(obj)
    i += 1
  return new_Vector