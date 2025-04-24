## 🚢 Optimización del Retiro de Contenedores en Puertos (Ramificación y Poda)

El retiro eficiente de contenedores en los puertos es un desafío logístico clave para garantizar la fluidez en la cadena de suministro. Luego de que un barco llega y descarga su carga, los contenedores quedan apilados en patios de almacenamiento temporales. Sin embargo, las restricciones físicas de acceso —al estar los contenedores apilados— implican que para acceder a uno ubicado más abajo, deben retirarse primero los que lo bloquean.

Este proyecto desarrolla un algoritmo que, mediante **ramificación y poda**, encuentra la **forma óptima de retirar contenedores específicos**, minimizando la cantidad total de movimientos y respetando las restricciones de apilamiento.

---

### 🧠 Descripción del problema

En el patio de un puerto, los contenedores son almacenados en **pilas verticales**, organizadas en varias filas. Cada fila se comporta como una **estructura tipo pila (LIFO)**: solo se puede retirar el contenedor que está en la parte superior. Para acceder a un contenedor ubicado más abajo, es necesario mover temporalmente los superiores a otras filas.

El objetivo es retirar, en un orden específico, aquellos contenedores que deben ser despachados primero —por ejemplo, por destino, urgencia o tipo de carga— **minimizando el número total de movimientos necesarios**.

---

### ⚙️ Metodología

En este repositorio encontrarás el desarrollo de un algoritmo de búsqueda inteligente basado en **ramificación y poda**, que evita la exploración de todas las combinaciones posibles (fuerza bruta) y se enfoca en caminos prometedores.

El proceso funciona así:

- Cada estado representa una **configuración del patio de contenedores**, los contenedores ya retirados, el **costo acumulado** (número de movimientos) y la **secuencia de acciones realizadas**.
- Se utiliza una **cola de prioridad** (`heapq`) que permite expandir primero los caminos con menor costo.
- Se aplican **reglas de poda** que descartan caminos:
  - Cuando el costo actual supera la mejor solución encontrada.
  - Cuando no hay suficientes contenedores disponibles para completar la secuencia deseada.
- Se establece un límite de exploración (`max_depth`) para controlar la complejidad computacional.

---

### 🧲 Detalles del modelo

- `initial_yard`: Lista de listas que representa las **filas de contenedores apilados**.
- `goal_train`: Lista con el **orden exacto de los contenedores a retirar**.
- El **costo** se incrementa por cada contenedor que debe moverse para acceder al deseado.
- Los nuevos estados se generan con la función `generate_children_verbose_generic`, que simula cada movimiento de manera explícita.

---

### 📊 Resultados

En el caso base simulado:

```python
initial_yard = [
    ['C', 'B', 'A', 'B', 'C', 'A'],
    ['A', 'B', 'C', 'A', 'B', 'C'],
    ['B', 'C', 'A', 'C', 'A', 'B'],
    ['C', 'C', 'B', 'B', 'A', 'A'],
    ['B', 'A', 'C', 'B', 'C', 'A'],
    ['A', 'C', 'B', 'C', 'A', 'B']
]

goal_train = ['A', 'A', 'A', 'A', 'B', 'B', 'B', 'C', 'C']
```
![etapa](https://github.com/user-attachments/assets/3541ae49-78ac-4ffa-8b35-ca03d2346f9a)

El algoritmo encontró una **solución óptima** que permite retirar los contenedores requeridos en el orden deseado, utilizando el **mínimo número de movimientos**. Además, devuelve la **secuencia detallada de pasos** para ejecutarlo de forma operativa.

---

### 📌 Archivos principales

- `State`: Clase que representa un estado intermedio del patio.
- `generate_children_verbose_generic`: Función que genera todos los movimientos válidos desde un estado.
- `branch_and_bound_limited`: Algoritmo principal que ejecuta la lógica de ramificación y poda.
- `create_yard`, `count_types_generic`: Funciones auxiliares para simular el entorno del puerto y contar los contenedores disponibles.

---

### 🚧 Próximas etapas

- Visualización paso a paso de la estrategia de retiro.
- Inclusión de pesos, tiempos de entrega o prioridades por tipo de carga o cliente.
- Comparación con soluciones heurísticas u optimización entera tradicional.

