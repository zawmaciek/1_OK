from pulp import LpMaximize, LpProblem, LpVariable

"""PuLP is an LP modeler written in Python. PuLP can generate MPS or LP files and call GLPK, COIN-OR CLP/CBC, CPLEX, GUROBI, MOSEK, XPRESS, CHOCO, MIPCL, SCIP to solve linear problems."""
model = LpProblem(name="zad_3", sense=LpMaximize)
# create variables
# a for nominator, b for denominator
sliwowica = LpVariable(name="sliwowica", cat='Integer', lowBound=0)
zytnia = LpVariable(name="zytnia", cat='Integer', lowBound=0)

# add constraints
model += (3 * sliwowica + 4 * zytnia <= 5000, "czas")
model += (3 * sliwowica + 2 * zytnia <= 4000, "budzet")
# add function
model += 6 * sliwowica + 5.4 * zytnia
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
