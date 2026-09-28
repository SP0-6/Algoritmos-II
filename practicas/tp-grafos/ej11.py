from Graph import Graph, Vertice

def vertice_global(grafo:Graph):

    for u in grafo.vertices:
        u.color = Vertice.BLANCO

    for u in grafo.vertices:
        if u.color == Vertice.BLANCO:
            candidato = u
            dfs_visit(candidato)

    for u in grafo.vertices:
        u.color = Vertice.BLANCO

    dfs_visit(candidato)

    for u in grafo.vertices:
        if u.color == Vertice.BLANCO:
            return False

    return True

    
def dfs_visit(u):

    u.color = Vertice.GRIS

    for v in u.adyacentes:
        if v.color == Vertice.BLANCO:
            dfs_visit(v)

    u.color = Vertice.NEGRO


        