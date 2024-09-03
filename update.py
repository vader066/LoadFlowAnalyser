import powerclasses as pc
import numpy as np
#for first iteration I need to sum the uvector array with 
# the product of the jacobian matrix and mismatch vector.

#1. create an np array of values from the mismatch Kvector

specified = pc.Kvector()
P2 = pc.Qty("P", 2, 0.5)
P3 = pc.Qty("P", 3, -1.5)
Q2 = pc.Qty("Q", 2, 1.0)
specified.push(P2)
specified.push(P3)
specified.push(Q2)

def arrify(Kvector):
  array = []
  for obj in Kvector.data:
    array.append(obj.value)
  return np.array(array) 

print(arrify(specified))
  
    
    



#The result of this computation will be a new uvector of the same quantities 
# but different values.

result_uvector = pc.Uvector()

D2 = pc.Qty("D", 2, -0.023)
D3 = pc.Qty("D", 3, -0.0654)
V2 = pc.Qty("V", 2, 1.089)
result_uvector.push(D2)
result_uvector.push(D3)
result_uvector.push(V2)


#This new uvector will be used to update the voltage matrix and the Delta matrix:

V_matrix = np.array([1.04, 1, 1.04]) 

D_matrix =np.array([0, 0, 0], dtype=float)

def update(Uvector):
  for obj in Uvector.data:
    if obj.type == 'D':
      D_matrix[obj.bus -1 ] = obj.value
    elif obj.type == 'V':
      V_matrix[obj.bus -1] = obj.value
      

update(result_uvector)


print(D_matrix)
print(V_matrix)


#The new V and D matrices and the new Uvector will then be used to find the Mismatch, 
# and the Jacobian again 























































































