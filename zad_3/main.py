"""5.
(4 punkty) Wyznacz dokładne rozwiązanie poniższego problemu liniowego.
max 𝑧 = 141𝑥1 + 393𝑥2 + 273𝑥3 + 804𝑥4 + 175𝑥5
3𝑥1 + 5𝑥2 + 2𝑥3 + 5𝑥4 + 4𝑥5 ≤ 36
7𝑥1 + 12𝑥2 + 11𝑥3 + 10𝑥4 ≤ 21
− 3𝑥2 + 12𝑥3 + 7𝑥4 + 2𝑥5≤17
0≤x1...x5≤20"""
from pulp import LpMaximize, LpProblem, LpVariable

"""PuLP is an LP modeler written in Python. PuLP can generate MPS or LP files and call GLPK, COIN-OR CLP/CBC, CPLEX, GUROBI, MOSEK, XPRESS, CHOCO, MIPCL, SCIP to solve linear problems."""
model = LpProblem(name="zad_3", sense=LpMaximize)
# create variables
x1 = LpVariable(name="x1", lowBound=0, upBound=20)
x2 = LpVariable(name="x2", lowBound=0, upBound=20)
x3 = LpVariable(name="x3", lowBound=0, upBound=20)
x4 = LpVariable(name="x4", lowBound=0, upBound=20)
x5 = LpVariable(name="x5", lowBound=0, upBound=20)
# add constraints
model += (3 * x1 + 5 * x2 + 2 * x3 + 5 * x4 + 4 * x5 <= 36, "const_1")
model += (7 * x1 + 12 * x2 + 11 * x3 + 10 * x4 <= 21, "const_2")
model += (-3 * x2 + 12 * x3 + 7 * x4 + 2 * x5 <= 17, "const_3")
# add function
model += 141 * x1 + 393 * x2 + 273 * x3 + 804 * x4 + 175 * x5
# output model for checking
print(model)
# solve
status = model.solve()
# checkout results
if status:
    print(f"Max function value: {model.objective.value()}")
    for var in model.variables():
        print(f"{var.name}: {var.value()}")
else:
    print('Failure')
