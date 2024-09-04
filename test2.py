from nr_models import rect
import nr_models as nr
from simulation_core import NR 
import numpy as np

Y = np.array([[rect(14, -90), rect(10, 90), rect(4, 90)], 
              [rect(10, 90), rect(15, -90), rect(5, 90)], 
              [rect(4, 90), rect(5, 90), rect(9, -90)]], 
             dtype=np.complex64)


spec = nr.Kvector()
p2 = nr.Qty('p', 2, -0.9)
p3 = nr.Qty('p', 3, 0.6)
q2 = nr.Qty('q', 2, -0.5)
spec.push(p2)
spec.push(p3)
spec.push(q2)

init = nr.Uvector()
d2 = nr.Qty("D", 2, 0.0)
d3 = nr.Qty("D", 3, 0.0)
v2 = nr.Qty("V", 2, 1.0)
init.push(d2)
init.push(d3) 
init.push(v2)

v = np.array([1.0, 1.0, 1.01], dtype=np.float32)
d = np.array([0.0, 0.0, 0.0], dtype=np.float32)

nr5 =  NR(5, spec, init, d, v, Y)
print(nr5)

