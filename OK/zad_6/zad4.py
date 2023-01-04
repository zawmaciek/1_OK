from pysmt.shortcuts import *


def solve(max):
    x = Symbol("x", INT)
    y = Symbol("y", INT)
    solver = Solver(name='z3')
    solver.add_assertion(x >= 30000)
    solver.add_assertion(y >= 30000)
    solver.add_assertion(x + y < max)
    solver.add_assertion(Equals((x * x + x + 1), (3 * (y * y))))
    try:
        res = solver.solve()
    except Exception as e:
        return False
    if res:
        x = solver.get_value(x)
        y = solver.get_value(y)
        print(f"CURRENT LOWEST RESULT: x: {solver.get_value(x)} y: {solver.get_value(y)}")
        return x._content.payload + y._content.payload
    else:
        return False


cur_max = 100000
while True:
    print(f"Searching for x+y under {cur_max}")
    result = solve(cur_max)
    if result:
        cur_max = result
    else:
        print('Not solvable, previous result was the smallest one')
        break
