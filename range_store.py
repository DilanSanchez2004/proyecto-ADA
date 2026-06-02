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