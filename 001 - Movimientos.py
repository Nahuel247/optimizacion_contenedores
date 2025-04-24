
#######################################################################################
# PROYECTO: Optimización del Retiro de Contenedores en Puertos (Ramificación y Poda)
########################################################################################

# Autor: Nahuel Canelo
# Correo: nahuelcaneloaraya@gmail.com


############################
#   IMPORTAMOS LIBRERÍAS
############################

from itertools import combinations
import heapq
import copy


############################
#     DEFINIMOS FUNCIONES
############################

# Creamos una foto del estado en un momento dado
class State:
    def __init__(self, yard, car, cost, path):
        self.yard = yard
        self.car = car
        self.cost = cost
        self.path = path

    # Comparamos dos objetos entre si
    def __lt__(self, other):
        return self.cost < other.cost


# Función para hacer una copia del patio
def create_yard(filas):
    return copy.deepcopy(filas)


# Creamos un inventario de contenedores disponibles por tipo en el patio (yard) en un momento dado.
def count_types_generic(yard):
    count = {}
    for fila in yard:
        for v in fila:
            count[v] = count.get(v, 0) + 1
    return count


# Creamos una función que ramifica el árbol de decisiones
def generate_children_verbose_generic(state, goal_car, num_filas):
    yard, car, cost, path = state.yard, state.car, state.cost, state.path
    # yard: patio actual, car: pila parcial formado, cost: costo acumulado hasta este punto, path: movimientos realizados hasta ahora
    children = []  # Inicializa una lista vacía donde se van a guardar los nuevos estados hijos generados desde este punto.
    target_type = goal_car[len(car)] if len(car) < len(goal_car) else None

    for i, fila in enumerate(yard):  # Recorre cada fila del patio con su índice.
        if not fila:
            continue
        if fila[0] == target_type:  # revisa si la primera caja de la fila es el que necesitamos
            new_yard = copy.deepcopy(
                yard)  # Crea una copia independiente del patio actual para no modificar el original.
            new_car = car + [fila[0]]  # Agrega el contenedor extraido
            new_yard[i] = fila[
                          1:]  # Actualiza esa fila del patio removiendo la primera caja (el que se acaba de sacar).
            new_path = path + [
                f"Sacar {target_type} directamente de Fila {i + 1}"]  # Agrega al historial de movimientos una descripción de esta acción.
            children.append(State(new_yard, new_car, cost, new_path))  # crea un nuevo estado
        else:

            try:
                pos = fila.index(target_type)  # Si la caja no está al inicio, entra dentro de la fila

                # Calcula todas las formas posibles de mover las cajas que bloquean el que queremos
                for dest_indices in combinations([j for j in range(num_filas) if j != i], pos):
                    new_yard = copy.deepcopy(yard)
                    description_lines = []

                    # Hacemos la simulación de los movimientos de dónde vamos a dejar las cajas
                    for k in range(pos):
                        moved = new_yard[i][k]
                        dest_fila = dest_indices[k]
                        new_yard[dest_fila] = [moved] + new_yard[dest_fila]
                        description_lines.append(f"Mover {moved} de Fila {i + 1} a Fila {dest_fila + 1}")

                    new_yard[i] = new_yard[i][pos:]

                    #
                    if new_yard[i] and new_yard[i][0] == target_type:
                        new_car = car + [
                            target_type]  # Actualizamos el estado del auto agregando el carro que acabas de liberar y sacar.
                        new_yard[i] = new_yard[i][1:]  # Quitamos el carro que acabas de sacar del frente de su fila.
                        description_lines.append(f"Sacar {target_type} desde Fila {i + 1}")
                        children.append(State(new_yard, new_car, cost + pos,
                                              path + ["; ".join(description_lines)]))  # creamos un nuevo estado
            except ValueError:
                continue
    return children


# Construimos una función que recorre todas las formas posibles de rellenar un auto de forma inteligente y optima
# initial_yard es el estado inicial del patio
# goal es la pila que se quiere armar
# max_depth=5000 Controla cuantos estados se van a evaluar
def branch_and_bound_limited(initial_yard, goal_car, max_depth=5000):
    num_filas = len(initial_yard)  # número de filas en el patio
    best_cost = float('inf')  # mejor costo encontrado hasta el momento (el menor)
    best_solution = None  # mejor estado alcanzado
    queue = []  # Para guardar los estados que aún no se han evaluado en la ramificación
    initial_state = State(initial_yard, [], 0, [])  # nodo raiz del árbol de decisiones
    heapq.heappush(queue, initial_state)  # ir agregando las ramas
    steps = 0

    while queue and steps < max_depth:  # revisara ramas mientras no sean mayor a max_depth
        current = heapq.heappop(queue)  # extrae aquel carro con el menor costo de armado
        steps += 1

        if current.cost >= best_cost:  # Evalua si el costo del carro actual es mayor que el mejor encontrado
            continue  # si es mayor se lo salta si es más caro

        # Vamos a evaluar si ya construimos la pila completa, con el orden deseado, y si es la forma de menor costo. Si es así,
        # lo guardamos.

        if current.car == goal_car:  # Verifica si la pila parcial (current.car) ya es igual al objetivo (goal)
            if current.cost < best_cost:  # Compara el costo de la solución actual (current.cost) con el mejor costo encontrado hasta ahora (best_cost).
                best_cost = current.cost  # best_cost: el menor costo conocido hasta ahora.
                best_solution = current  # el estado que generó ese costo (incluye el carro completo, los movimientos, el patio restante, etc.).
            continue

        left = count_types_generic(
            current.yard)  # Contamos las cajas que quedan en el patio según tipo con la función count_types...
        required = {k: goal_car.count(k) - current.car.count(k) for k in
                    set(goal_car)}  # determinar cuantos cajas faltan, por tipo, para completar la pila

        # Verificamos si con lo que está en el patio podemos armar la pila
        if any(left.get(k, 0) < required[k] for k in required):
            continue

        # Llamamos a la función generate_children... para generar todos los posibles movimientos en el siguiente turno desde el estado actual
        children = generate_children_verbose_generic(current, goal_car, num_filas)
        for child in children:  # cada child representa un nuevo estado
            heapq.heappush(queue, child)  # agregamos cada child a la cola de prioridad

    return best_solution, steps


########################
#    EJECUTAMOS
########################

# Definimos estado inicial del patio
new_yard = create_yard([
    ['C', 'B', 'A', 'B', 'C', 'A'],
    ['A', 'B', 'C', 'A', 'B', 'C'],
    ['B', 'C', 'A', 'C', 'A', 'B'],
    ['C', 'C', 'B', 'B', 'A', 'A'],
    ['B', 'A', 'C', 'B', 'C', 'A'],
    ['A', 'C', 'B', 'C', 'A', 'B']
])

# Definimos la pila con los paquetes que queremos agregar
small_goal = ['A', 'A', 'A', 'A', 'B', 'B', 'B', 'C', 'C']

# Ejecutamos
result_limited, total_steps = branch_and_bound_limited(new_yard, small_goal, max_depth=5000)

result_limited.path, result_limited.cost, total_steps

