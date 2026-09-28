from collections import deque

class Graph:
    def __init__(self, vertices=[], aristas=[]):
        self.vertices = vertices
        self.aristas = aristas
        
class Vertice:
    BLANCO = 0
    GRIS = 1
    NEGRO = 2

    def __init__(self, valor):
        self.valor = valor
        self.adyacentes = []

        self.color = Vertice.BLANCO
        self.distancia = None
        self.padre = None

        self.inicio = None
        self.fin = None


def bfs(grafo, origen):
    for u in grafo:
        u.color = Vertice.BLANCO
        u.distancia = None
        u.padre = None

    origen.color = Vertice.GRIS
    origen.distancia = 0

    cola = deque()
    cola.append(origen)

    while cola:
        u = cola.popleft()

        for v in u.adyacentes:
            if v.color == Vertice.BLANCO:
                v.color = Vertice.GRIS
                v.distancia = u.distancia + 1
                v.padre = u

                cola.append(v)

        u.color = Vertice.NEGRO

def dfs(grafo):
    for u in grafo:
        u.color = Vertice.BLANCO
        u.padre = None
        u.inicio = None
        u.fin = None

    tiempo = 0

    def dfs_visit(u):
        nonlocal tiempo

        tiempo += 1
        u.inicio = tiempo
        u.color = Vertice.GRIS

        for v in u.adyacentes:
            if v.color == Vertice.BLANCO:
                v.padre = u
                dfs_visit(v)

        u.color = Vertice.NEGRO
        tiempo += 1
        u.fin = tiempo

    for u in grafo:
        if u.color == Vertice.BLANCO:
            dfs_visit(u)