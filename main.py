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
    print("Rangos cargados:", almacen.rangos)
    print("Operaciones:", operaciones)