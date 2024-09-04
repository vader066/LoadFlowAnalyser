from nr_models import rect
import nr_models as nr
from simulation_core import NR 
import numpy as np

# wrong testing values

Y = np.array([[rect(60, -90), rect(40, 90), rect(20, 90)], 
              [rect(40, 90), rect(60, -90), rect(20, 90)], 
              [rect(20, 90), rect(20, 90), rect(40, -90)]], 
             dtype=np.complex64)


spec = nr.Kvector()
p2 = nr.Qty('p', 2, 4.0)
p3 = nr.Qty('p', 3, -5.0)
q3 = nr.Qty('q', 3, -4.0)
spec.push(p2)
spec.push(p3)
spec.push(q3)



init = nr.Uvector()
d2 = nr.Qty("D", 2, 0.0)
d3 = nr.Qty("D", 3,  0.0)
v3 = nr.Qty("V", 3, 1.0)
init.push(d2)
init.push(d3) 
init.push(v3)

v = np.array([1.0, 1.05, 1.0], dtype=np.float32)
d = np.array([0.0, 0.0,  0.0], dtype=np.float32)

nr5 =   NR(5, spec, init, d, v, Y)