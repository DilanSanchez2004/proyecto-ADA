# Documento Técnico — Proyecto Final ADA I
## Motor de Consultas sobre Datos Comprimidos por Rangos

**Curso:** Análisis y Diseño de Algoritmos I — 2026-I  
**Docente:** Mateo Echeverry Correa, Ing.

---

## Integrantes del equipo

| Nombre completo | Código | Correo institucional |
|---|---|---|
| Dilan Joseph Sanchez Silva | 2380492 | sanchez.dilan@correounivalle.edu.co |
| Juan José González Trujillo | 2459536 | integrante2@correounivalle.edu.co |

---

## 1. Descripción general del problema resuelto

El proyecto implementa un **motor de consultas sobre secuencias comprimidas por rangos**. En lugar de almacenar cada posición individualmente, la secuencia se representa como una lista de rangos no solapados de la forma `(valor, inicio, fin)`, donde un rango indica que todas las posiciones entre `inicio` y `fin` tienen el mismo valor.

Por ejemplo, la secuencia `1 1 1 1 1 3 3 3 2 2 2 2` se representa como:

```
1  1  5
3  6  8
2  9  12
```

El programa lee esta representación comprimida desde `entrada.txt`, procesa un conjunto de operaciones **sin expandir nunca la secuencia completa**, y escribe los resultados en `salida.txt`. La solución está diseñada para trabajar con secuencias cuyo dominio puede alcanzar hasta 10⁹ posiciones, hasta 1 000 000 de rangos iniciales y 200 000 consultas.

---

## 2. Formato de entrada y salida

### 2.1 Entrada (`entrada.txt`)

```
N
valor inicio fin
valor inicio fin
...
Q
OPERACION parametros
OPERACION parametros
...
```

- `N`: cantidad de rangos iniciales.
- Cada rango tiene `valor`, posición `inicio` y posición `fin`.
- `Q`: cantidad de operaciones a procesar en orden.

### 2.2 Salida (`salida.txt`)

Cada operación que produce resultado genera una línea con el formato:

```
OPERACION parametros = resultado
```

Las operaciones `UPDATE` y `MERGE` generan `= OK`. El orden de salida coincide exactamente con el orden de las operaciones en `entrada.txt`.

---

## 3. Diseño general de la solución

La solución se organiza en dos módulos:

- **`range_store.py`** — contiene las clases `TablaHash`, `Rango` y `AlmacenRangos` con toda la lógica algorítmica.
- **`main.py`** — responsable de la lectura de `entrada.txt`, el despacho de operaciones y la escritura de `salida.txt`.

Al cargar los rangos, `main.py` llama `_agregar_al_indice` por cada rango para inicializar el índice de frecuencias desde el inicio. Los rangos se almacenan en una **lista ordenada por posición de inicio**, invariante que se mantiene tras cada `UPDATE`. Esto permite aplicar búsqueda binaria en todas las operaciones de consulta.

---

## 4. Estructuras de datos implementadas

| Estructura | Uso en el problema | Operaciones principales | Justificación | Complejidad |
|---|---|---|---|---|
| `TablaHash` | Índice de frecuencias (operación `FREQUENCY`) | `get`, `set`, `sumar` | Acceso O(1) promedio sin usar `dict` nativo | O(1) prom. |
| `Rango` (clase) | Representación de cada intervalo comprimido | Constructor, `__repr__` | Encapsula valor + límites sin expandir la secuencia | O(1) |
| Lista de `Rango` (`almacen.rangos`) | Almacén principal de rangos ordenados por inicio | `append`, slice, indexación | Permite búsqueda binaria al estar ordenada | O(log N) búsqueda |

### 4.1 TablaHash

Implementación propia con **encadenamiento por listas** (cada bucket es una lista de pares `(clave, valor)`). La función de hash es `clave % capacidad`. Se usa exclusivamente para el índice de frecuencias: almacena cuántas posiciones tiene cada valor a lo largo de todos los rangos, permitiendo responder `FREQUENCY` en O(1) promedio **sin recorrer la lista de rangos**.

### 4.2 Clase Rango

Estructura que encapsula los tres atributos de un rango: `valor`, `inicio` y `fin`. Evita el uso de tuplas anónimas y permite `__repr__` legible para depuración.

### 4.3 Lista de rangos (`almacen.rangos`)

Lista Python usada como arreglo base (permitido por el enunciado). Los rangos se mantienen ordenados por `inicio` en todo momento, lo que habilita la búsqueda binaria. **No se usan `dict`, `set`, `heapq`, `sorted`, ni ninguna otra estructura nativa prohibida.**

---

## 5. Operaciones soportadas

| Operación | Descripción |
|---|---|
| `VALUE pos` | Retorna el valor en la posición `pos`. Usa búsqueda binaria sobre los rangos ordenados. |
| `SUM ini fin` | Suma todos los `valor × longitud` de cada rango solapado con `[ini, fin]`. |
| `UPDATE ini fin val` | Asigna `val` a todas las posiciones en `[ini, fin]`, dividiendo o recortando los rangos existentes. Actualiza el índice de frecuencias. |
| `FREQUENCY val` | Retorna cuántas posiciones tienen el valor `val`, consultando el índice `TablaHash` en O(1). |
| `MAX_RANGE ini fin` | Retorna el valor máximo entre todos los rangos solapados con `[ini, fin]`. Implementado con **dividir y vencer**. |
| `MIN_RANGE ini fin` | Retorna el valor mínimo entre todos los rangos solapados con `[ini, fin]`. Implementado con **dividir y vencer**. |
| `DECOMPRESS ini fin` | Expande la subsecuencia `[ini, fin]` generando cada posición. Solo se expande el fragmento solicitado, nunca la secuencia completa. |
| `COUNT_RANGES` | Retorna la cantidad actual de rangos en la lista en O(1). |
| `MERGE` | Fusiona rangos adyacentes que tengan el mismo valor, reduciendo el tamaño de la lista. |
| `TOP_K_FREQ k` | Retorna los `k` valores con mayor frecuencia acumulada. Implementado con **QuickSelect (dividir y vencer)**. |
| `TOP_K_VAL k` | Retorna los `k` rangos con mayor valor. Implementado con **QuickSelect (dividir y vencer)**. |

---

## 6. Análisis de complejidad temporal

N = cantidad de rangos; Q = cantidad de consultas; k = rangos solapados en una consulta; L = posiciones expandidas en `DECOMPRESS`; V = valores distintos en el índice.

| Operación | Complejidad esperada | Variables | Justificación |
|---|---|---|---|
| `VALUE pos` | O(log N) | N = rangos | Búsqueda binaria sobre lista ordenada por inicio |
| `SUM ini fin` | O(k + log N) | k = rangos solapados | Búsqueda binaria para el primer solapamiento, luego recorre solo los k rangos afectados |
| `UPDATE ini fin val` | O(k + log N) | k = rangos modificados | Localiza con búsqueda binaria y reemplaza solo los rangos afectados; actualiza el índice |
| `FREQUENCY val` | O(1) prom. | — | Acceso directo al índice TablaHash; sin recorrido de rangos |
| `MAX_RANGE ini fin` | O(k + log N) | k = rangos solapados | Dividir y vencer con poda: descarta mitades fuera del intervalo en O(log N) |
| `MIN_RANGE ini fin` | O(k + log N) | k = rangos solapados | Igual que MAX_RANGE |
| `DECOMPRESS ini fin` | O(k + L) | L = posiciones expandidas | k rangos solapados; cada posición se genera exactamente una vez |
| `COUNT_RANGES` | O(1) | — | Retorna `len(rangos)` directamente |
| `MERGE` | O(N) | N = rangos actuales | Recorrido lineal único para fusionar consecutivos iguales |
| `TOP_K_FREQ k` | O(V) prom. | V = valores distintos | QuickSelect sobre los pares del índice; O(V) promedio, O(V²) peor caso |
| `TOP_K_VAL k` | O(N) prom. | N = rangos | QuickSelect sobre la lista de rangos; O(N) promedio, O(N²) peor caso |

---

## 7. Análisis de uso de memoria

La solución utiliza **O(N)** memoria para almacenar los N rangos en la lista. Nunca se construye una estructura de tamaño proporcional al dominio (hasta 10⁹ posiciones).

El índice `TablaHash` ocupa **O(V)** donde V es la cantidad de valores distintos observados, que en la práctica es mucho menor que el dominio total.

`UPDATE` puede aumentar el número de rangos en como máximo 2 unidades por operación (si divide un rango en tres partes), por lo que tras Q operaciones el tamaño máximo es **O(N + Q)**. `MERGE` reduce este tamaño fusionando rangos adyacentes iguales.

---

## 8. Estrategia de dividir y vencer

El proyecto implementa **dos estrategias distintas** de dividir y vencer.

### 8.1 MAX_RANGE y MIN_RANGE

#### Operación que la utiliza
`MAX_RANGE` y `MIN_RANGE`, implementados mediante `_max_dyv` y `_min_dyv` en `AlmacenRangos`.

#### Descripción del problema
Dado el intervalo de consulta `[inicio, fin]`, encontrar el valor máximo (o mínimo) entre todos los rangos de la lista que se solapan con ese intervalo.

#### Caso base
- Cuando `izq > der` (subproblema vacío): retorna `None`.
- Cuando `rangos[izq].inicio > fin` o `rangos[der].fin < inicio` (**poda**): toda la mitad queda fuera del intervalo, retorna `None` sin explorarla.
- Cuando `izq == der` (un solo rango): verifica solapamiento y retorna su valor o `None`.

#### División
Se calcula `mid = (izq + der) // 2` y se divide el arreglo en dos mitades: `rangos[izq..mid]` y `rangos[mid+1..der]`.

#### Combinación
Se retorna el máximo (o mínimo) entre los resultados de ambas mitades, ignorando los `None`.

#### Complejidad temporal
En el peor caso (todos los rangos solapan): T(N) = 2·T(N/2) + O(1) → **O(N)** por el Teorema Maestro.  
Con la poda, cuando la consulta afecta solo k rangos el costo real es **O(k + log N)**.

#### Comparación con solución ingenua
La solución ingenua recorre todos los rangos de forma lineal: **O(N)** siempre. La solución con dividir y vencer poda ramas enteras en O(log N) cuando detecta que toda una mitad queda fuera del intervalo, reduciendo el costo práctico a **O(k + log N)** cuando k << N.

---

### 8.2 TOP_K_FREQ y TOP_K_VAL — QuickSelect

#### Operación que la utiliza
`TOP_K_FREQ k` y `TOP_K_VAL k`, implementados mediante `_quickselect` en `AlmacenRangos`.

#### Descripción del problema
Dado un arreglo de pares y un entero k, encontrar los k elementos mayores sin ordenar todo el arreglo.

#### Caso base
Cuando `left == right`: el subproblema tiene un solo elemento, se retorna directamente.

#### División
Se elige un pivote (`arr[right]`) y se particiona el arreglo en dos mitades: elementos mayores o iguales al pivote a la izquierda, menores a la derecha. Se obtiene el índice `pivot_index` del pivote tras la partición.

#### Combinación (descarte)
- Si `pivot_index == k-1`: los primeros k elementos son los k mayores, problema resuelto.
- Si `pivot_index > k-1`: los k mayores están todos en la mitad izquierda, se recursiona solo en `[left, pivot_index-1]`.
- Si `pivot_index < k-1`: se recursiona solo en `[pivot_index+1, right]`.

No hay combinación de resultados parciales: en cada paso se **descarta la mitad que no contiene al k-ésimo**, que es el principio de dividir y vencer aplicado a selección.

#### Complejidad temporal
- Promedio: **O(V)** para `TOP_K_FREQ` y **O(N)** para `TOP_K_VAL`, donde V = valores distintos y N = rangos.
- Peor caso teórico: O(V²) / O(N²). Se mitiga con `random.shuffle` antes de aplicar QuickSelect.

#### Comparación con solución ingenua
Ordenar todo el arreglo para luego tomar los k primeros cuesta **O(N log N)**. QuickSelect evita ordenar completamente y logra **O(N) promedio**, lo que es especialmente ventajoso cuando k << N.

---

## 9. Casos de prueba utilizados

| Tipo | Descripción | Operaciones cubiertas | Resultado |
|---|---|---|---|
| Pequeño | 5 rangos, 7 operaciones (ejemplo del enunciado) | `VALUE`, `SUM`, `UPDATE`, `FREQUENCY`, `MAX_RANGE`, `DECOMPRESS`, `COUNT_RANGES` | Salida coincide con ejemplo del enunciado |
| Mediano | 1 000 rangos, 500 operaciones mezcladas con `UPDATE`s | Todas las operaciones incluyendo `MERGE`, `MIN_RANGE`, `TOP_K_FREQ`, `TOP_K_VAL` | Resultados verificados manualmente |
| Grande | 100 000 rangos, 50 000 operaciones (generado por `generar_prueba.py`) | `VALUE`, `SUM`, `UPDATE`, `FREQUENCY`, `MAX_RANGE`, `COUNT_RANGES`, `TOP_K_FREQ`, `TOP_K_VAL` | Ejecuta en < 0.5 s total |

---

## 10. Casos límite considerados

| Caso límite | Cómo se prueba | Comportamiento esperado |
|---|---|---|
| Rangos consecutivos con el mismo valor | `UPDATE` seguido de `MERGE` | `MERGE` los fusiona y el índice de frecuencias queda consistente |
| `UPDATE` que divide un rango en tres | `UPDATE 3 4 99` sobre rango `[1-10]=5` | Se generan `[1-2]=5`, `[3-4]=99`, `[5-10]=5` sin pérdida de datos |
| `UPDATE` que cubre varios rangos | Asignar mismo valor a rangos adyacentes distintos | `COUNT_RANGES` aumenta temporalmente; `MERGE` lo reduce |
| Consulta sobre una sola posición | `VALUE` en el extremo izquierdo y derecho | Búsqueda binaria retorna correctamente el valor límite |
| Consulta que cruza varios rangos | `SUM` / `MAX_RANGE` / `MIN_RANGE` sobre intervalo grande | Acumula/compara solo los rangos solapados sin expandir |
| Rangos muy grandes (posiciones hasta 10⁹) | `VALUE` y `SUM` sobre posiciones extremas | No se construye ninguna estructura proporcional a 10⁹ |
| Secuencia con un único rango | Todas las operaciones sobre 1 rango | Búsqueda binaria con un solo elemento funciona correctamente |
| `FREQUENCY` sobre valor inexistente | `FREQUENCY` con un valor que no aparece en ningún rango | `TablaHash` retorna 0 sin error |
| `TOP_K_FREQ` con k mayor al número de valores distintos | `TOP_K_FREQ 9999` con pocos valores | Retorna todos los disponibles sin error de índice |
| `TOP_K_VAL` sobre lista vacía | `TOP_K_VAL` antes de cargar rangos | Retorna lista vacía sin error |

---

## 11. Conclusiones

- La representación comprimida por rangos permite trabajar con secuencias de hasta 10⁹ posiciones usando solo **O(N)** de memoria, donde N es la cantidad de rangos activos.
- La combinación de lista ordenada + búsqueda binaria reduce el costo de la mayoría de consultas de **O(N)** a **O(log N + k)**, siendo k los rangos solapados.
- El índice `TablaHash` propio para frecuencias elimina la necesidad de recorrer toda la lista en `FREQUENCY`, logrando **O(1) promedio** sin usar `dict` nativo.
- La estrategia de dividir y vencer en `MAX_RANGE` y `MIN_RANGE` introduce poda efectiva: descarta mitades del arreglo que quedan completamente fuera del intervalo, mejorando el desempeño práctico frente a la solución ingenua lineal.
- QuickSelect en `TOP_K_FREQ` y `TOP_K_VAL` selecciona los k elementos mayores en **O(N) promedio** sin ordenar el arreglo completo, siendo superior a la alternativa ingenua de **O(N log N)**.
- `UPDATE` es la operación más costosa (O(k + log N)) pero mantiene la invariante de orden de la lista, condición necesaria para que todas las demás operaciones sean eficientes.
