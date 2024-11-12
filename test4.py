from nr_models import rect
import nr_models as nr
from simulation_core import NR 
import numpy as np

spec = nr.Kvector()
p2 = nr.Qty("P", 2, 1.0)
q2 = nr.Qty("Q", 2, 0.5)
spec.push(p2)
spec.push(q2)

init = nr.Uvector()
v2 = nr.Qty("V", 2, 1.0)
d2 = nr.Qty("D", 2, 0)
init.push(v2)
init.push(d2)

v = np.array([1.0, 1.0], dtype=np.float32)
d = np.array([0.0, 0.0], dtype=np.float32)

y = np.array([[-20j, 20j],
              [20j, -20j]], dtype=np.complex64)

nr2 = NR(7, spec, init, d, v, y)

