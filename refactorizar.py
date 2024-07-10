import matplotlib.pyplot as plt #se utiliza para crear gráficos y visualizaciones.
import numpy as np # se utiliza para operaciones numéricas, especialmente con matrices.
from collections import deque #una cola de doble extremo que permite añadir y 
#eliminar elementos desde ambos extremos, útil para el algoritmo de búsqueda en amplitud (BFS)

class Cuadricula:
    def __init__(self):#defino mi constructor es un atributo propio de la clase
        self.tamano_cuadricula = 6
        self.cuadricula = np.zeros((self.tamano_cuadricula, self.tamano_cuadricula))
        self.obstaculos=[]
    
    def crear_cuadricula(self, inicio, fin): #solicita coordenada inicio y fin
        self.cuadricula[inicio] = 2 #inicio marcado con 2
        self.cuadricula[fin] = 3 #inicio marcado con 3
    
    def mostrar_cuadricula(self):
        _, ax = plt.subplots()#figura y conjunto de ejes
        ax.matshow(self.cuadricula, cmap='Greys')#muestra la matriz en una escala de grises.

        for i in range(self.tamano_cuadricula):#recorre cada [] matriz
            for j in range(self.tamano_cuadricula):
                if self.cuadricula[i, j] == 2: #Dependiendo del valor de la celda se dibuja un texto 'I' para inicio
                    ax.text(j, i, 'I', va='center', ha='center', color='green')
                elif self.cuadricula[i, j] == 3:
                    ax.text(j, i, 'F', va='center', ha='center', color='red')
                elif self.cuadricula[i, j] == 1:
                    ax.text(j, i, 'O', va='center', ha='center', color='black')
                elif self.cuadricula[i, j] == 4:
                    ax.text(j, i, 'R', va='center', ha='center', color='purple')
        
        plt.show()
    
    def obtener_cuadricula(self):
        return self.cuadricula
    
    def actualizar_cuadricula(self, nueva_cuadricula):
        self.cuadricula = nueva_cuadricula    

    def solicitar_coordenada(self, mensaje):
        while True:
            try:
                coord_input = input(mensaje)
                x, y = map(int, coord_input.split(','))
                if 0 <= x < self.tamano_cuadricula and 0 <= y < self.tamano_cuadricula:
                    return (x, y)# si son validas rompe y fin de la fun
                else:
                    print(f"Por favor, ingrese coordenadas válidas en el rango 0-{self.tamano_cuadricula - 1}.")
            except ValueError:
                print("Entrada inválida. Por favor, ingrese coordenadas en el formato x,y.")

    def agregar_obstaculo(self):
        while True:
            obs_input = input("Ingrese la posición del obstáculo (formato: x,y) o 'fin' para terminar: ")
            if obs_input.lower() == 'fin':
                break
            try:
                obs_x, obs_y = map(int, obs_input.split(','))
                if 0 <= obs_x < self.tamano_cuadricula and 0 <= obs_y < self.tamano_cuadricula:
                    if self.cuadricula[obs_x, obs_y] == 0:  # Verificar que la celda esté disponible
                        self.obstaculos.append((obs_x, obs_y))
                    else:
                        print("No se puede agregar un obstáculo en la posición de inicio y fin")
                else:
                    print(f"Por favor, ingrese coordenadas válidas en el rango 0-{self.tamano_cuadricula - 1}.")
            except ValueError:
                print("Entrada inválida. Por favor, ingrese coordenadas en el formato x,y.")

        for x, y in self.obstaculos:
            self.cuadricula[x, y] = 1

    def eliminar_obstaculo(self):
        while True:
            if not self.obstaculos:
                print("No hay obstáculos para eliminar.")
                return
            print("\nObstáculos actuales:")
            for i, (x, y) in enumerate(self.obstaculos):
                print(f"{i}: ({x}, {y})")
            try:
                indice = int(input("Ingrese el índice del obstáculo que desea eliminar o 'fin' para terminar: "))
                if 0 <= indice < len(self.obstaculos):
                    x, y = self.obstaculos.pop(indice)
                    self.cuadricula[x, y] = 0  # Eliminar el obstáculo de la cuadrícula
                    print(f"Obstáculo en ({x}, {y}) eliminado.")
                    self.mostrar_cuadricula()
                else:
                    print("Índice no válido.")
            except ValueError:
                break        
            


class ResolverBFS:
    def __init__(self, cuadricula):
        self.cuadricula = cuadricula
        self.tamano_cuadricula = len(cuadricula)
        self.camino = None
    
    def es_movimiento_valido(self, x, y):
        return 0 <= x < self.tamano_cuadricula and 0 <= y < self.tamano_cuadricula and self.cuadricula[x, y] != 1

    def encontrar_camino(self, inicio, fin):
        direcciones = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        cola = deque([[inicio]])
        visitados = set()
        visitados.add(inicio)

        while cola:
            camino = cola.popleft()
            x, y = camino[-1]

            if (x, y) == fin:
                self.camino = camino
                return camino  # Retornar el camino encontrado

            for dx, dy in direcciones:
                nx, ny = x + dx, y + dy
                if self.es_movimiento_valido(nx, ny) and (nx, ny) not in visitados:
                    cola.append(camino + [(nx, ny)])
                    visitados.add((nx, ny))

        return []

    def trazar_camino(self):
        if self.camino is None:
            return self.cuadricula
        for x, y in self.camino:
            if self.cuadricula[x, y] == 0:
                self.cuadricula[x, y] = 4
        return self.cuadricula


mi_cuadricula = Cuadricula()#objetos
inicio = mi_cuadricula.solicitar_coordenada("Ingrese la posición de inicio (formato: x,y): ")
fin = mi_cuadricula.solicitar_coordenada("Ingrese la posición de fin (formato: x,y): ")
mi_cuadricula.crear_cuadricula(inicio, fin)
mi_cuadricula.mostrar_cuadricula()
mi_cuadricula.agregar_obstaculo()
mi_cuadricula.mostrar_cuadricula()

mi_resolver_bfs = ResolverBFS(mi_cuadricula.obtener_cuadricula())
camino = mi_resolver_bfs.encontrar_camino(inicio, fin)
if camino:
    mi_cuadricula.actualizar_cuadricula(mi_resolver_bfs.trazar_camino())
    mi_cuadricula.mostrar_cuadricula()
    print('Camino encontrado:', camino)
else:
    print('No se encontró un camino')
mi_cuadricula.eliminar_obstaculo()
