#######################################################################################
# PROYECTO: Optimización del Retiro de Contenedores en Puertos (Ramificación y Poda)
########################################################################################

# Autor: Nahuel Canelo
# Correo: nahuelcaneloaraya@gmail.com



## ===============================##

import time
import re

def simular_movimientos(yard_inicial, movimientos, pila_objetivo, pausa=1.5):
    print("\n--- SIMULACIÓN DE MOVIMIENTOS ---\n")
    yard = create_yard(yard_inicial)
    pila_armada = []

    for paso, instruccion in enumerate(movimientos, 1):
        print(f"🚧 Paso {paso}: {instruccion}")

        submovs = instruccion.split(";")
        for mov in submovs:
            mov = mov.strip()

            # Caso "Mover X de Fila Y a Fila Z"
            match = re.match(r"Mover (\w) de Fila (\d+) a Fila (\d+)", mov)
            if match:
                carro = match.group(1)
                origen = int(match.group(2)) - 1
                destino = int(match.group(3)) - 1

                if carro in yard[origen]:
                    yard[origen].remove(carro)
                    yard[destino] = [carro] + yard[destino]
                continue

            # Caso "Sacar X desde Fila Y" o "Sacar X directamente de Fila Y"
            match_sacar = re.match(r"Sacar (\w) (?:desde|directamente de) Fila (\d+)", mov)
            if match_sacar:
                carro = match_sacar.group(1)
                fila = int(match_sacar.group(2)) - 1
                if yard[fila] and yard[fila][0] == carro:
                    pila_armada.append(carro)
                    yard[fila] = yard[fila][1:]

        # Mostrar el estado actual del patio y la pila en construcción
        print("🎯 Pila objetivo:", pila_objetivo)
        print(" Pila armado :", pila_armada)
        print("📦 Estado actual del patio:")
        for i, fila in enumerate(yard):
            print(f"Fila {i+1}: {fila}")
        print("\n----------------------------\n")
        time.sleep(pausa)

    # Al final, resumen
    print("✅ Simulación finalizada")
    if pila_armada == pila_objetivo:
        print("🎉 La pila armada coincide perfectamente con la pila objetivo.")
    else:
        print("⚠️ La pila armada NO coincide con la pila objetivo.")
        print("pila final   :", pila_armada)
        print("🎯 pila objetivo:", pila_objetivo)

simular_movimientos(new_yard, result_limited.path, small_goal, pausa=1)
