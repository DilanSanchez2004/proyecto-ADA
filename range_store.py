# range_store.py

class Rango:
    def __init__(self, valor, inicio, fin):
        self.valor = valor
        self.inicio = inicio
        self.fin = fin

    def __repr__(self):
        return f"[{self.inicio}-{self.fin}]={self.valor}"


class AlmacenRangos:
    def __init__(self):
        # Lista de objetos Rango, ordenada por posición de inicio
        self.rangos = []
        
    def value(self, posicion):
        for r in self.rangos:
            if r.inicio <= posicion <= r.fin:
               return r.valor
        return None  # posición vacía

    def count_ranges(self):
        return len(self.rangos)

    def frequency(self, valor):
        total = 0
        for r in self.rangos:
            if r.valor == valor:
                total += (r.fin - r.inicio + 1)
        return total
    
    def sum_range(self, inicio, fin):
        total = 0
        for r in self.rangos:
            # ver si el rango se solapa con [inicio, fin]
            solape_ini = max(r.inicio, inicio)
            solape_fin = min(r.fin, fin)
            if solape_ini <= solape_fin:
                cantidad = solape_fin - solape_ini + 1
                total += r.valor * cantidad
        return total

    def max_range(self, inicio, fin):
        maximo = None
        for r in self.rangos:
            if r.inicio <= fin and r.fin >= inicio:  # hay solapamiento
                if maximo is None or r.valor > maximo:
                    maximo = r.valor
        return maximo

    def min_range(self, inicio, fin):
        minimo = None
        for r in self.rangos:
            if r.inicio <= fin and r.fin >= inicio:
                if minimo is None or r.valor < minimo:
                    minimo = r.valor
        return minimo
    
    def decompress(self, inicio, fin):
        resultado = []
        for r in self.rangos:
            solape_ini = max(r.inicio, inicio)
            solape_fin = min(r.fin, fin)
            if solape_ini <= solape_fin:
                cantidad = solape_fin - solape_ini + 1
                for _ in range(cantidad):
                    resultado.append(str(r.valor))
        return ' '.join(resultado)
    
    def update(self, inicio, fin, valor):
        nuevos = []

        for r in self.rangos:
            # rango completamente fuera del intervalo, se deja igual
            if r.fin < inicio or r.inicio > fin:
                nuevos.append(r)

        # rango completamente dentro del intervalo, se elimina
            elif r.inicio >= inicio and r.fin <= fin:
                pass  # no se agrega

        # rango sobresale por la izquierda
            elif r.inicio < inicio and r.fin <= fin:
                nuevos.append(Rango(r.valor, r.inicio, inicio - 1))

        # rango sobresale por la derecha
            elif r.inicio >= inicio and r.fin > fin:
                nuevos.append(Rango(r.valor, fin + 1, r.fin))

        # rango envuelve completamente el intervalo (se divide en dos)
            else:
                nuevos.append(Rango(r.valor, r.inicio, inicio - 1))  # parte izquierda
                nuevos.append(Rango(r.valor, fin + 1, r.fin))        # parte derecha

    # insertar el nuevo rango en la posición correcta
        insertado = False
        for i in range(len(nuevos)):
            if nuevos[i].inicio > inicio:
                nuevos.insert(i, Rango(valor, inicio, fin))
                insertado = True
                break
        if not insertado:
            nuevos.append(Rango(valor, inicio, fin))

        self.rangos = nuevos
        
    def merge(self):
        if len(self.rangos) == 0:
            return

        fusionados = [self.rangos[0]]

        for i in range(1, len(self.rangos)):
            ultimo = fusionados[-1]
            actual = self.rangos[i]

        # son consecutivos y tienen el mismo valor?
            if ultimo.valor == actual.valor and ultimo.fin + 1 == actual.inicio:
                ultimo.fin = actual.fin  # extender el último rango
            else:
                fusionados.append(actual)

        self.rangos = fusionados