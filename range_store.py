# range_store.py

class TablaHash:
    def __init__(self, capacidad=2048):
        self.capacidad = capacidad
        self.tabla = [None] * capacidad

    def _hash(self, clave):
        return clave % self.capacidad

    def get(self, clave):
        idx = self._hash(clave)
        bucket = self.tabla[idx]
        if bucket is None:
            return 0
        for k, v in bucket:
            if k == clave:
                return v
        return 0

    def set(self, clave, valor):
        idx = self._hash(clave)
        if self.tabla[idx] is None:
            self.tabla[idx] = []
        bucket = self.tabla[idx]
        for i in range(len(bucket)):
            if bucket[i][0] == clave:
                bucket[i] = (clave, valor)
                return
        bucket.append((clave, valor))

    def sumar(self, clave, cantidad):
        actual = self.get(clave)
        self.set(clave, actual + cantidad)


class Rango:
    def __init__(self, valor, inicio, fin):
        self.valor = valor
        self.inicio = inicio
        self.fin = fin

    def __repr__(self):
        return f"[{self.inicio}-{self.fin}]={self.valor}"


class AlmacenRangos:
    def __init__(self):
        self.rangos = []
        self.freq_index = TablaHash()

    # ── Índice auxiliar ───────────────────────────────────────────────

    def _agregar_al_indice(self, rango):
        cantidad = rango.fin - rango.inicio + 1
        self.freq_index.sumar(rango.valor, cantidad)

    def _quitar_del_indice(self, rango):
        cantidad = rango.fin - rango.inicio + 1
        actual = self.freq_index.get(rango.valor)
        self.freq_index.set(rango.valor, actual - cantidad)

    # ── Búsqueda binaria ──────────────────────────────────────────────

    def _buscar_indice(self, posicion):
        izq = 0
        der = len(self.rangos) - 1

        while izq <= der:
            mid = (izq + der) // 2
            r = self.rangos[mid]

            if r.inicio <= posicion <= r.fin:
                return mid
            elif posicion < r.inicio:
                der = mid - 1
            else:
                izq = mid + 1

        return -1

    def _buscar_primer_solapamiento(self, inicio):
        izq = 0
        der = len(self.rangos) - 1
        resultado = len(self.rangos)

        while izq <= der:
            mid = (izq + der) // 2
            if self.rangos[mid].fin >= inicio:
                resultado = mid
                der = mid - 1
            else:
                izq = mid + 1

        return resultado

    # ── Operaciones ───────────────────────────────────────────────────

    def value(self, posicion):
        idx = self._buscar_indice(posicion)
        if idx == -1:
            return None
        return self.rangos[idx].valor

    def count_ranges(self):
        return len(self.rangos)

    def frequency(self, valor):
        return self.freq_index.get(valor)

    def sum_range(self, inicio, fin):
        total = 0
        idx = self._buscar_primer_solapamiento(inicio)
        for i in range(idx, len(self.rangos)):
            r = self.rangos[i]
            if r.inicio > fin:
                break
            solape_ini = max(r.inicio, inicio)
            solape_fin = min(r.fin, fin)
            total += r.valor * (solape_fin - solape_ini + 1)
        return total

    def max_range(self, inicio, fin):
        maximo = None
        idx = self._buscar_primer_solapamiento(inicio)
        for i in range(idx, len(self.rangos)):
            r = self.rangos[i]
            if r.inicio > fin:
                break
            if maximo is None or r.valor > maximo:
                maximo = r.valor
        return maximo

    def min_range(self, inicio, fin):
        minimo = None
        idx = self._buscar_primer_solapamiento(inicio)
        for i in range(idx, len(self.rangos)):
            r = self.rangos[i]
            if r.inicio > fin:
                break
            if minimo is None or r.valor < minimo:
                minimo = r.valor
        return minimo

    def decompress(self, inicio, fin):
        resultado = []
        idx = self._buscar_primer_solapamiento(inicio)
        for i in range(idx, len(self.rangos)):
            r = self.rangos[i]
            if r.inicio > fin:
                break
            solape_ini = max(r.inicio, inicio)
            solape_fin = min(r.fin, fin)
            for _ in range(solape_fin - solape_ini + 1):
                resultado.append(str(r.valor))
        return ' '.join(resultado)

    def update(self, inicio, fin, valor):
        idx_ini = self._buscar_primer_solapamiento(inicio)
        idx_fin = idx_ini
        while idx_fin < len(self.rangos) and self.rangos[idx_fin].inicio <= fin:
            idx_fin += 1

        # quitar del indice los rangos afectados
        for i in range(idx_ini, idx_fin):
            self._quitar_del_indice(self.rangos[i])

        nuevos_rangos = []

        if idx_ini < len(self.rangos):
            r = self.rangos[idx_ini]
            if r.inicio < inicio:
                nuevos_rangos.append(Rango(r.valor, r.inicio, inicio - 1))

        nuevos_rangos.append(Rango(valor, inicio, fin))

        if idx_fin > idx_ini and idx_fin <= len(self.rangos):
            r = self.rangos[idx_fin - 1]
            if r.fin > fin:
                nuevos_rangos.append(Rango(r.valor, fin + 1, r.fin))

        # agregar al indice los rangos nuevos
        for r in nuevos_rangos:
            self._agregar_al_indice(r)

        cantidad_nueva = len(nuevos_rangos)
        cantidad_vieja = idx_fin - idx_ini

        if cantidad_nueva == cantidad_vieja:
            for i, r in enumerate(nuevos_rangos):
                self.rangos[idx_ini + i] = r
        else:
            self.rangos[idx_ini:idx_fin] = nuevos_rangos

    def merge(self):
        if len(self.rangos) == 0:
            return

        fusionados = [self.rangos[0]]

        for i in range(1, len(self.rangos)):
            ultimo = fusionados[-1]
            actual = self.rangos[i]

            if ultimo.valor == actual.valor and ultimo.fin + 1 == actual.inicio:
                # quitar ambos del indice y agregar el fusionado
                self._quitar_del_indice(ultimo)
                self._quitar_del_indice(actual)
                ultimo.fin = actual.fin
                self._agregar_al_indice(ultimo)
            else:
                fusionados.append(actual)

        self.rangos = fusionados