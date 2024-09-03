import powerclasses as pc
import numpy as np

def eval(initial, Jacob, mismatch):
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
    new_Vector = pc.Uvector()
    i = 0
    for obj in vector.data:
      obj.value = array[i]
      new_Vector.push(obj)
      i += 1
    return new_Vector
    
  # converting vector objects into numerical arrays 
  mm = arrify(mismatch)
  init = arrify(initial)
  
  invJacob = np.linalg.inv(Jacob)
  product = np.matmul(invJacob, mm)  
  sum = init + product
  result = vectorfy(sum, initial)

  return result



def NR(iters, spec, init, D, V, Y ):
  for n in range(iters):
    mismatch = pc.MismatchV(spec, D, V, Y)
    jacob = pc.Jacobian(spec, init, D, V, Y)
    iterationi = eval(init, jacob, mismatch) 
    print(iterationi)
    pc.update(iterationi, D, V) 
  
  print(f'{iters}: iteration performed')
  
  return iterationi
  