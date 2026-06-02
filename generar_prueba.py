# generar_prueba.py
import random

N = 100000  # rangos
Q = 50000   # consultas

lineas = []
lineas.append(str(N))

# generar rangos que no se solapan y cubren posiciones hasta 10^9
pos = 1
for _ in range(N):
    tamanio = random.randint(1, 10000)
    fin = pos + tamanio - 1
    valor = random.randint(1, 1000)
    lineas.append(f"{valor} {pos} {fin}")
    pos = fin + 1

lineas.append(str(Q))

pos_maxima = pos - 1

for _ in range(Q):
    op = random.randint(1, 6)

    if op == 1:
        p = random.randint(1, pos_maxima)
        lineas.append(f"VALUE {p}")
    elif op == 2:
        a = random.randint(1, pos_maxima)
        b = random.randint(a, min(a + 1000000, pos_maxima))
        lineas.append(f"SUM {a} {b}")
    elif op == 3:
        a = random.randint(1, pos_maxima)
        b = random.randint(a, min(a + 1000000, pos_maxima))
        v = random.randint(1, 1000)
        lineas.append(f"UPDATE {a} {b} {v}")
    elif op == 4:
        a = random.randint(1, pos_maxima)
        b = random.randint(a, min(a + 1000000, pos_maxima))
        lineas.append(f"MAX_RANGE {a} {b}")
    elif op == 5:
        v = random.randint(1, 1000)
        lineas.append(f"FREQUENCY {v}")
    elif op == 6:
        lineas.append(f"COUNT_RANGES")

with open("entrada.txt", "w") as f:
    f.write("\n".join(lineas))

print(f"entrada.txt generado con {N} rangos y {Q} consultas")