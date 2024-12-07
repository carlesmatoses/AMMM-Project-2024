# AMMM-Project-2024

## Generating instances
```
cd InstanceGeneratorCustom
python Main.py <config relative path>
```

## Heuristics
```
cd Heuristics
python Main.py
```

### funcionamiento:
miembros = [Miembro_{0},Miembro_{1},..,Miembro_{N-1}]
SFinal = SolucionVacia()
miembros.sorted("descending")
For i in miembros:
    S = SolucionVacia()
    S.assign(i) # cada iteración empieza la solución por un miembro diferente

    while !S.isFeasible():
        S.assignFeasibleMember(alpha) # assign random member

    SFinal = bestFit(S,SFinal)

We care about: 
- The times we get a solution
- The closest solutions to perfect
- The time rquired to find a solution

Successes: 0  out of 100 executions with alpha = 1.0
Successes: 42 out of 100 executions with alpha = 0.7
Successes: 2  out of 100 executions with alpha = 0.2

# Document
Ordenar document com:
- Statement
- ILP formulation
- Metaheuristics
  - isFeasible() for member or for set
  - w(i,S)
    - basic one,
    - improved one (relaxing)
  - Greedy constructive algorithm
    - generate a list of feasible members
    - select the one with more weight
    - check if it is correct
  - local search algorithm
  - GRASP algorithm


# gràfiques:
1. com altera el numero de departaments, membres i p en el temps d'execució cplex