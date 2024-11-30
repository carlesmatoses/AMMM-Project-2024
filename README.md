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

This works 8 out of 26 times, less than 30% of the time