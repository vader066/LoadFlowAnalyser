import bisect

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
    
    
    

# Vector of Know Quantities
class Kvector:
  def __init__(self):
    self.data = []
    
  #adds quantities to the known vector but ensures they are only of type P and Q
  #and arranges them in the right order
  def push(self, qty):
    types = ['P', 'Q']
    if not isinstance(qty, Qty):
      raise TypeError(f'Expected a Qty object, but got {type(qty).__name__} instead.')
    if qty.type.upper() not in types:
      raise TypeError("cannot add V or D quantities to Vector of Knowns")
    
    # sort Vector so that P's come before Q's and they are arranged in ascending order
    type_order = {'P': 0, 'Q': 1}
    new_entry = (type_order[qty.type], qty.bus)
        
    # Use bisect to find the correct insertion index
    sortable_entries = [(type_order[obj.type], obj.bus) for obj in self.data]
    index = bisect.bisect_left(sortable_entries, new_entry)
    self.data.insert(index, qty)
    
    
  #for displaying the array in a user-friendly way in the console
  def __repr__(self):
    return repr([f"{qty.type}{qty.bus}: {qty.value}" for qty in self.data])
    
    
    
    
# Vector of Know Quantities
class Uvector:
  def __init__(self):
    self.data = []
    
  #adds quantities to the unknown vector but ensures they are only of type V and D
  #and arranges them in the right order
  def push(self, qty):
    types = ['V', 'D']
    if not isinstance(qty, Qty):
      raise TypeError(f'Expected a Qty object, but got {type(qty).__name__} instead.')
    if qty.type.upper() not in types:
      raise TypeError("cannot add P or Q quantities to Vector of Unknowns")
    
    # sort Vector so that D's come before V's and they are arranged in ascending order
    type_order = {'D': 0, 'V': 1}
    new_entry = (type_order[qty.type], qty.bus)
        
    # Use bisect to find the correct insertion index
    sortable_entries = [(type_order[obj.type], obj.bus) for obj in self.data]
    index = bisect.bisect_left(sortable_entries, new_entry)
    self.data.insert(index, qty)
    
    
  #for displaying the array in a user-friendly way in the console
  def __repr__(self):
    return repr([f"{qty.type}{qty.bus}: {qty.value}" for qty in self.data])
    
    
v2 = Qty("v", 2, 1.32)    
v1 = Qty("v", 1, 1.05)
v3 = Qty("v", 3, 1.32)    
d2 = Qty("d", 2, 1.32)    
v4 = Qty("v", 4, 1.32)    
d3 = Qty("d", 3, 1.32)    
    
Vector_of_Knowns = Uvector()

Vector_of_Knowns.push(v3)
Vector_of_Knowns.push(d3)
Vector_of_Knowns.push(v2)
Vector_of_Knowns.push(v4)
Vector_of_Knowns.push(v1)
Vector_of_Knowns.push(d2)

print(Vector_of_Knowns)



    
  
    
    
    