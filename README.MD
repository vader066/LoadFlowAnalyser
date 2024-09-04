The Project is predominantly Object Oriented

Classes are in the nr_models.py file
Main Functions are in the simulation_core.py file

The Quantities V, D, P, Q for Voltage, delta(angle of voltage), Real Power and Reactive Power will all be instances of the class Qty.

A quantity class has properties:
Type: can be P, Q, V or D (they are Not case sensitive)
bus: any positive non-zero integer
value: the value of the quantity

These properties must all be present at the time of definition

eg
p2 = Qty("P", 2, 1.5)

The known vector is a class Kvector.
It has an array property that can only contain only Qty objects of type P and Q.
It must be empty at the time of definition

It has method push to add Qty objects to it

eg
specified = Kvector()
specified.push(p2)

the Unkown vector is a class Uvector.
It has an array property that can only contain only Qty objects of type V and D.
It must be empty at the time of definition

It is similar to Kvector class in all other ways

The rect function is used to convert complex numbers from rectangular to polar form

Eg.
rect(15, -60)

can be used to enter values into the Y matrix quickly
