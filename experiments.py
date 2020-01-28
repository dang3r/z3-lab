
from z3 import *

"""Example from the z3 tutorials"""
Tie, Shirt = Bools('Tie Shirt')
s = Solver()
s.add(Or(Tie, Shirt), 
    Or(Not(Tie), Shirt), 
    Or(Not(Tie), Not(Shirt)))
print(s.check())
print(s.model())

"""
Consider the following puzzle. Spend exactly 100 dollars and buy exactly 100 animals.
Dogs cost 15 dollars, cats cost 1 dollar,
and mice cost 25 cents each. You have to buy at least one of each.
How many of each should you buy?
"""
s = Solver()
d, c, m = Ints("dog cat mouse")

# todo: Why didnt floats work?
# s.add(15*d + c + .25*m == 10000)
s.add(1500*d + 100*c + 25*m == 10000)
s.add(d + c + m == 100)
s.add(d > 0, c > 0, m > 0)
s.check()
print(s.model())

"""
TODO: 
Application: Install Problem
The install problem consists of determining whether a new set of packages can be installed in a system. This application is based on the article OPIUM: Optimal Package Install/Uninstall Manager. Many packages depend on other packages to provide some functionality. Each distribution contains a meta-data file that explicates the requirements of each package of the distribution. The meta-data contains details like the name, version, etc. More importantly, it contains depends and conflicts clauses that stipulate which other packages should be on the system. The depends clauses stipulate which other packages must be present. The conflicts clauses stipulate which other packages must not be present.
The install problem can be easily solved using Z3. The idea is to define a Boolean variable for each package. This variable is true if the package must be in the system. If package a depends on packages b, c and z, we write:
"""

"""
Scheduling
3 employees
employee 1 - works 3 days, not on wednesday
employee 2 - works 2-4 days, not weekends
employee 3 - works 2 days
maximum of 2 workers a day
inspired from https://developers.google.com/optimization
"""
mon, tue, wed, thu, fri, _sat, sun = list(range(7))
dayofweek = "monday tuesday wednesday thursday friday saturday sunday".split()
solver = Solver()
b = []
for emp in range(3):
    for day in range(7):
        b.append(Bool(f"{emp}_{day}"))

# Employee 1 works 3 days
solver.add(Sum([If(b[i], 1, 0) for i in range(7)]) == 3)
solver.add(b[wed] == False)

# Employee 2
solver.add(Sum([If(b[7 + i], 1, 0) for i in range(7)]) >= 2, Sum([If(b[7 + i], 1, 0) for i in range(7)]) <= 4)
solver.add(b[_sat] == False)
solver.add(b[sun] == False)

# Employee 3
solver.add(Sum([If(b[14 + i], 1, 0) for i in range(7)]) == 2)

# At most 2 workers a day
for i in range(7):
    solver.add(Sum([If(b[i + 7*j], 1, 0) for j in range(3)]) <= 2)

if solver.check() == sat:
    m = solver.model()
    for item in b:
        if is_true(m[item]):
            emp, day = item.decl().name().split("_")
            print(f"Employee {emp} is working on {dayofweek[int(day)]}")


