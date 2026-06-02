# main.py

from range_store import Rango, AlmacenRangos

def leer_entrada(nombre_archivo):
    almacen = AlmacenRangos()
    operaciones = []

    with open(nombre_archivo, 'r') as f:
        lineas = f.read().splitlines()

    i = 0
    N = int(lineas[i]); i += 1

    for _ in range(N):
        partes = lineas[i].split(); i += 1
        valor = int(partes[0])
        inicio = int(partes[1])
        fin = int(partes[2])
        almacen.rangos.append(Rango(valor, inicio, fin))

    Q = int(lineas[i]); i += 1

    for _ in range(Q):
        operaciones.append(lineas[i].split()); i += 1

    return almacen, operaciones


if __name__ == "__main__":
    almacen, operaciones = leer_entrada("entrada.txt")
    resultados = []

    for op in operaciones:
        nombre = op[0]

        if nombre == "VALUE":
            pos = int(op[1])
            resultado = almacen.value(pos)
            resultados.append(f"VALUE {pos} = {resultado}")

        elif nombre == "COUNT_RANGES":
            resultados.append(f"COUNT_RANGES = {almacen.count_ranges()}")

        elif nombre == "FREQUENCY":
            val = int(op[1])
            resultados.append(f"FREQUENCY {val} = {almacen.frequency(val)}")
            
        elif nombre == "SUM":
            ini, fin = int(op[1]), int(op[2])
            resultados.append(f"SUM {ini} {fin} = {almacen.sum_range(ini, fin)}")

        elif nombre == "MAX_RANGE":
            ini, fin = int(op[1]), int(op[2])
            resultados.append(f"MAX_RANGE {ini} {fin} = {almacen.max_range(ini, fin)}")

        elif nombre == "MIN_RANGE":
            ini, fin = int(op[1]), int(op[2])
            resultados.append(f"MIN_RANGE {ini} {fin} = {almacen.min_range(ini, fin)}")
        
        elif nombre == "DECOMPRESS":
            ini, fin = int(op[1]), int(op[2])
            resultados.append(f"DECOMPRESS {ini} {fin} = {almacen.decompress(ini, fin)}")
            
        elif nombre == "UPDATE":
            ini, fin, val = int(op[1]), int(op[2]), int(op[3])
            almacen.update(ini, fin, val)
            resultados.append(f"UPDATE {ini} {fin} {val} = OK")
            
        elif nombre == "MERGE":
            almacen.merge()
            resultados.append(f"MERGE = OK")

    # imprimir en consola
    for r in resultados:
        print(r)

    # escribir salida.txt
    with open("salida.txt", "w") as f:
        for r in resultados:
            f.write(r + "\n")