from itertools import product, permutations
from operator import itemgetter 


def make_variables():
    """Returns mapping of the cell coordinates to their values"""
    rows = "ABCDEFGHI"
    cols = "123456789"
    combs = product(rows, cols)
    return {c: None for c in combs}

def make_constraints():
    """Returns mapping of cell coordinate to neighboring cells 
    in the CSF graph"""
    rows = "ABCDEFGHI"
    cols = "123456789"
    # ex. "A1","A2" and "A4", "A5"
    allcombs = []
    for r in rows:
        combs = product(r, cols)
        allcombs.extend(list(permutations(combs, 2)))
    # ex. "A1", "B1" and "D4", "E4"
    for c in cols:
        combs = product(rows, c)
        allcombs.extend(list(permutations(combs, 2)))
    # ex. "A2", "C3"
    squares = [["ABC", "DEF", "GHI"], ["123", "456", "789"]]
    for h in squares[0]:
        for v in squares[1]:
            allcombs.extend(list(permutations(product(h, v), 2)))
    combs = set(allcombs)
    res = {}
    for x, y in combs:
        if x not in res: res[x] = []
        res[x].append(y)
    return res    

def make_domains(variables):
    """Returns mapping of cell coordinate to the starting domain of each cell"""
    return { var: set(list(range(1, 10))) for var in variables.keys() }

def make_pruned(variables):
    """Returns mapping of cell to set of pruned (neighbor_cell, value) pairs"""
    return { var: set() for var in variables.keys() }

def constraint_satisfied(xval, yval):
    """Returns true iff constraint on xval and yval is satisfied"""
    return xval != yval

def consistent(x, val, variables, constraints):
    """Returns true iff all constraints involving x are satisfied"""
    return all(constraint_satisfied(variables[n], val) for n in constraints[x])

def select_unassigned_variable(variables, constraints, domains):
    """minimum remaining values heuristic"""
    unassigned_vars = (v for v in variables if variables[v] is None)
    return min(unassigned_vars, key=lambda v: len(domains[v]))

def ordered_vals(variable, domains):
    """least constraining value heuristic"""
    d = domains[variable]
    sort_order = [sum(1 for n in constraints[variable] if d in domains[n]) 
                  for dv in d]
    dsort = zip(d, sort_order)
    sorted_domain = [x[0] for x in sorted(dsort, key=itemgetter(1))]
    return sorted_domain

def revise(xi, xj, domains):
    """Returns true iff we revise domain of xi"""
    revised = False
    for dv_xi in domains[xi]:
        for dv_xj in domains[xj]:
            if constraint_satisfied(dv_xi, dv_xj):
                break
        else:
            domains[xi].remove(dv_xi)
            revised = True
    return revised

def ac3(domains, constraints):
    """Returns false if inconsistency is found (not solvable), true otherwise"""
    q = [(k, v) for (k, vs) in constraints.items() for v in vs]
    while q:
        xi, xj = q.pop()
        if revise(xi, xj, domains):
            if len(ds[xi]) == 0: return False
            for xk in constraints[xi]:
                if xk == xi: continue
                q.append(xk)
    return True

def forward_check(x, variables, constraints, domains, pruned):
    """Esablishes arc consistency for X: for each unassigned Y connected to X, 
    remove from Y's domain any value that is inconsistent with the chosen xi value"""
    xval = variables[x]
    for y in constraints[x]:
        for dv_y in domains[y].copy():
            if dv_y == xval:
                domains[y].remove(dv_y)
                pruned[x].add((y, dv_y))
                
def unassign(x, variables, domains, pruned, constraints):
    """Unassign x and restore pruned values from neighbor variables' domains"""
    variables[x] = None
    for y, dv_y in pruned[x]:
        domains[y].add(dv_y)
    pruned[x].clear()    

def backtrack(variables, constraints, domains, pruned):
    """Returns the solved variable set if the CSF is solved, else returns False"""
    if None not in variables.values(): return variables
    var = select_unassigned_variable(variables, constraints, domains)
    for val in ordered_vals(var, domains, constraints):
        if consistent(var, val, variables, constraints):
            variables[var] = val
            if not any(True for n in variables.values() if n is None):
                return variables
            forward_check(var, variables, constraints, domains, pruned)
            result = backtrack(variables, constraints, domains, pruned)
            if result: return variables
            unassign(var, variables, domains, pruned, constraints)
    return False

def flat_vars(variables):
    """Orders vars for reading in board input"""
    return sorted(variables.keys(), key=lambda v: (ord('9') - ord(v[1]), v[0]))

def search(brd):
    """Solves sudoku puzzle, returns the board values if solvable"""
    variables = make_variables()
    constraints = make_constraints()
    domains = make_domains(variables)
    pruned = make_pruned(variables)
    for i,v in enumerate(flat_vars(variables)):
        variables[v] = brd[i] or None
        
    # Preprocess to check for inconsistencies. 
    # Sometimes this also effectively solves the puzzle by reducing all domains 
    # to one value.
    if not ac3(domains, constraints):
        print("not solvable")
        return False
    
    result = backtrack(variables, constraints, domains, pruned)
    if not result:
        print("not solvable")
        print(result)
        return False
    return result

def print_solution(solution):
    for i,v in enumerate(flat_vars(solution)):
        if i % 9 == 0 and i > 0: print()
        elif i % 3 == 0 and i > 0: print("| ", end="")
        if i % 27 == 0 and i > 0: print("- "* 11)
        print(solution[v], end=" ")

if __name__ == '__main__':
    # Taken from https://www.websudoku.com/
    evil = [
        0,0,7,0,0,5,0,9,0,
        6,2,0,1,0,7,0,0,8,
        0,1,0,0,0,0,0,0,0,
        0,0,0,0,0,3,5,0,0,
        0,8,0,0,6,0,0,3,0,
        0,0,5,4,0,0,0,0,0,
        0,0,0,0,0,0,0,6,0,
        9,0,0,6,0,1,0,2,4,
        0,6,0,8,0,0,1,0,0
    ]
    
    solved = search(evil)
    if solved: print_solution(solved)
