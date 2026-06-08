# main.py
import time
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
        r = Rango(valor, inicio, fin)
        almacen.rangos.append(r)
        almacen._agregar_al_indice(r)   # <-- CORRECCIÓN: inicializar freq_index al cargar
 
    Q = int(lineas[i]); i += 1
 
    for _ in range(Q):
        operaciones.append(lineas[i].split()); i += 1
 
    return almacen, operaciones
 
 
if __name__ == "__main__":
    almacen, operaciones = leer_entrada("entrada.txt")
    resultados = []
 
    tiempos = {"VALUE": 0, "SUM": 0, "UPDATE": 0, "FREQUENCY": 0,
               "MAX_RANGE": 0, "MIN_RANGE": 0, "DECOMPRESS": 0,
               "COUNT_RANGES": 0, "MERGE": 0, "TOP_K_FREQ": 0, "TOP_K_VAL": 0}
    conteos = {k: 0 for k in tiempos}
 
    for op in operaciones:
        nombre = op[0]
        t0 = time.time()
 
        if nombre == "VALUE":
            pos = int(op[1])
            resultado = almacen.value(pos)
            resultados.append(f"VALUE {pos} = {resultado}")
        
        elif nombre == "TOP_K_FREQ":
            k = int(op[1])
            top = almacen.top_k_by_frequency(k)
            # Formato: (valor,freq) (valor,freq) ...
            resultado_str = " ".join([f"({v},{f})" for v, f in top])
            resultados.append(f"TOP_K_FREQ {k} = {resultado_str}")

        elif nombre == "TOP_K_VAL":
            k = int(op[1])
            top = almacen.top_k_by_value(k)
            resultado_str = " ".join([f"({v},{i},{f})" for v, i, f in top])
            resultados.append(f"TOP_K_VAL {k} = {resultado_str}")
 
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
 
        tiempos[nombre] += time.time() - t0
        conteos[nombre] += 1
 
    # imprimir en consola
    for r in resultados:
        print(r)
 
    # imprimir tiempos por operacion
    print("\n--- TIEMPOS POR OPERACION ---")
    for k in tiempos:
        if conteos[k] > 0:
            print(f"{k}: {tiempos[k]:.3f}s ({conteos[k]} llamadas)")
 
    # escribir salida.txt
    with open("salida.txt", "w") as f:
        for r in resultados:
            f.write(r + "\n")