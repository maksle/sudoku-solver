# Sudoku solver

Based on constraint satisfaction algorithms in the book `Artificial Intelligence: A Modern Approach, 3rd edition` by Stuart Russell and Peter Norvig.

It first uses AC-3 to infer reductions in the domain of variables before the search. If this reduces the domains to one value per cell, the puzzle is effectively solved. If some variable's domain becomes the empty set, the puzzle is unsolveable. Otherwise, a search is done to find a solution.

The search uses backtracking. Order of solutions tried in the DFS matters, as some orders can prune large parts of the tree. The following heuristics are used to sort variables and values:

- Minimum value remaining heuristic
- Least constraining value heuristic

Forward checking is used to maintain arc consistency for a variable X after a value is chosen for it. This infers domain reductions in neighboring variables.

If the puzzle is solveable, a solution is returned.

## Example
```
import sudoku 

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

solved = sudoku.search(evil)
if solved: sudoku.print_solution(solved)

>>>
8 3 7 | 2 4 5 | 6 9 1 
6 2 4 | 1 9 7 | 3 5 8 
5 1 9 | 3 8 6 | 7 4 2 
- - - - - - - - - - - 
2 4 6 | 9 1 3 | 5 8 7 
7 8 1 | 5 6 2 | 4 3 9 
3 9 5 | 4 7 8 | 2 1 6 
- - - - - - - - - - - 
1 5 8 | 7 2 4 | 9 6 3 
9 7 3 | 6 5 1 | 8 2 4 
4 6 2 | 8 3 9 | 1 7 5 
```
