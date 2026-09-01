class AVLTree:
    def __init__(self):
        self.root=None

class AVLNode:
    def __init__(self):
        self.key=None
        self.value=None
        self.leftnode=None
        self.rightnode=None
        self.parent=None
        self.bf=None


def rotateLeft(AVL: AVLTree, node: AVLNode) -> AVLNode:
    
    # Hijo derecho de node
    right=node.rightnode
 
    if right.bf == 1 and node.bf == -2:
        # Doble rotación: derecha sobre right
        bfNieto=right.leftnode.bf
        newR=rotateRight(AVL, right)  
 
        # Actualizar factores según el nieto
        if bfNieto == 0:
            node.bf=0
            right.bf=0
        elif bfNieto == -1:
            node.bf=1
            right.bf=0
        else:  
            node.bf=0
            right.bf=-1

        newR.bf=0

    else: 
        # Rotación simple: newR es el hijo derecho
        newR=right
        
        if right.bf == 0:  # Sólo pasa en borrado
            node.bf=-1
            newR.bf=1
        else:  
            node.bf=0
            newR.bf=0

    # Reubicar el subárbol izquierdo de newR
    node.rightnode=newR.leftnode
    if newR.leftnode is not None:
        newR.leftnode.parent=node
 
    # Reemplazar node por newR en el árbol
    if node == AVL.root:
        AVL.root=newR
        newR.parent=None
    elif node == node.parent.rightnode:
        node.parent.rightnode=newR
        newR.parent=node.parent
    else:
        node.parent.leftnode=newR
        newR.parent=node.parent
 
    # node pasa a ser hijo izquierdo de newR
    newR.leftnode=node
    node.parent=newR
 
    return newR
 
 
def rotateRight(AVL: AVLTree, node: AVLNode) -> AVLNode:
   
    # Hijo izquierdo de node
    left=node.leftnode
 
    if left.bf == -1 and node.bf == 2:
        # Doble rotación: izquierda sobre left
        bfNieto=left.rightnode.bf
        newL=rotateLeft(AVL, left)  
 
        # Actualizar factores según el nieto
        if bfNieto == 0:
            node.bf=0
            left.bf=0
        elif bfNieto == 1:
            node.bf=-1
            left.bf=0
        else:  
            node.bf=0
            left.bf=1

        newL.bf=0

    else:
        # Rotación simple: newL es el hijo izquierdo
        newL=left
        
        if left.bf == 0:  # Sólo pasa en borrado
            node.bf=1
            newL.bf=-1
        else:  
            node.bf=0
            newL.bf=0
 
    # Reubicar el subárbol derecho de newL
    node.leftnode=newL.rightnode
    if newL.rightnode is not None:
        newL.rightnode.parent=node
 
    # Reemplazar node por newL en el árbol
    if node == AVL.root:
        AVL.root=newL
        newL.parent=None
    elif node == node.parent.leftnode:
        node.parent.leftnode=newL
        newL.parent=node.parent
    else:
        node.parent.rightnode=newL
        newL.parent=node.parent
 
    # node pasa a ser hijo derecho de newL
    newL.rightnode=node
    node.parent=newL
 
    return newL


def calculateBalance(AVL:AVLTree)->AVLTree:
    # Calcula todos los factores de balance
    if AVL.root is not None:
        calcularH(AVL.root)  
    return AVL


def calcularH(node:AVLNode)->int:
    if node is None:
        return 0
    
    # Calcula alturas de ambos subárboles
    hLeft=calcularH(node.leftnode)
    hRight=calcularH(node.rightnode)
    
    # Factor de balance = altura izquierda - derecha
    node.bf=hLeft-hRight

    return 1 + max(hRight, hLeft)
    

def reBalance(AVL:AVLTree)->AVLTree:
    
    # Primero calcula los factores de todos los nodos
    T=calculateBalance(AVL)
    
    # Rebalancea desde la raíz
    reBalanceR(T, T.root)

    return T


def reBalanceR(T:AVLTree, node:AVLNode):
    if node is not None:
        # Desequilibrio hacia la izquierda
        if node.bf==2:
            node=rotateRight(T, node)

        # Desequilibrio hacia la derecha
        elif node.bf==-2:
            node=rotateLeft(T, node)

        # Recorre ambos subárboles
        reBalanceR(T, node.rightnode)
        reBalanceR(T, node.leftnode)


def insert(AVL:AVLTree, element, key:int)-> int:
    #Se hace igual que con Binary Tree, pero se maneja el rebalanceo con las funciones ya hechas
    newNode=AVLNode()
    newNode.key=key
    newNode.value=element
    newNode.bf=0 #porque un nuevo nodo siempre se inserta como hoja(en principio)

    if AVL.root is None:
        AVL.root=newNode
        
    else:
        insertR(newNode, AVL.root)
        rebalancePath(AVL, newNode.parent)

    return newNode.key

def insertR(newNode: AVLNode, current: AVLNode)->AVLNode:
    if newNode.key > current.key:
        if current.rightnode is None:
            current.rightnode=newNode
            newNode.parent=current
            current.bf-=1
            return
        else:
            insertR(newNode, current.rightnode)
            return
    else:
        if current.leftnode is None:
            current.leftnode=newNode
            newNode.parent=current
            current.bf+=1
            return newNode.key
        else:
            insertR(newNode, current.leftnode)
            return


def delete(AVL:AVLTree, element)->int:
    #Implementación como Binary Tree
    if (key:=search(AVL, element)) is not None:
        return deleteKey(AVL, key)

def search(AVL:AVLTree, element)->int:
    #se implementa como en Binary Tree
    if AVL is not None:
        return searchR(AVL.root, element)
    return None

def searchR(current:AVLNode, element)->int:
    if current is None:
        return None

    if current.value == element:
        return current.key
    
    if (found := searchR(current.rightnode, element)) is not None:
        return found
    
    return searchR(current.leftnode, element)

def deleteKey(AVL: AVLTree, key: int) -> int:
    #Funciona como en Binary Tree pero se tiene en cuenta el rebalanceo con las 
    #funciones definidas antes
    if AVL.root is None:
        return None
    
    key=deleteKeyR(AVL, AVL.root, key)
    reBalance(AVL)
    
    return key

def deleteKeyR(AVL: AVLTree, current: AVLNode, key: int):
    if current == None: 
        return None
    
    if current.key == key:
        
        if current.leftnode == None or current.rightnode == None:

            if current.leftnode != None:
                hijito=current.leftnode
            else: 
                hijito=current.rightnode
            
            if current.parent == None: 
                AVL.root=hijito

                if hijito != None: 
                    hijito.parent=None
                    
            else: 

                if current.parent.leftnode == current:
                    current.parent.leftnode=hijito

                else: 
                    current.parent.rightnode=hijito

                if hijito is not None:
                   hijito.parent=current.parent

            return key

        else: 
            hijito2=min_nodo(current.rightnode)
            current.key=hijito2.key
            deleteKeyR(AVL, hijito2, hijito2.key)
        
        return key

    elif key < current.key:
        return deleteKeyR(AVL, current.leftnode, key)
    
    else: 
        return deleteKeyR(AVL, current.rightnode, key)

def min_nodo(node: AVLNode) -> AVLNode:
    while node.leftnode != None:
        node=node.leftnode
    return node

def generarAVL(treeA:AVLTree, treeB:AVLTree, keyX:int)->AVLTree:

    htreeA=height(treeA.root)
    htreeB=height(treeB.root)

    node=AVLNode()
    node.key=keyX

    AVL=AVLTree() 

    if abs(htreeA-htreeB)<=1:
               
        AVL.root=node

        node.leftnode=treeA.root
        if treeA.root is not None:
            node.leftnode.parent=node
        node.rightnode=treeB.root
        if treeB.root is not None:
            node.rightnode.parent=node

        return AVL

    if htreeA>htreeB:

        AVL.root=treeA.root

        node.rightnode=treeB.root

        if treeB.root is not None:
            node.rightnode.parent=node

        current=treeA.root

        hCurrent=htreeA
        while hCurrent > htreeB+1:
            hCurrent -= 1
            if current.bf==1:
                hCurrent -= 1
            current = current.rightnode

        node.leftnode=current.rightnode

        if current.rightnode is not None:
            current.rightnode.parent=node

        current.rightnode=node
        node.parent=current

        if current.bf <= 0:
            node.bf=hCurrent-1 - (htreeB)
            if current.bf == -1:
                current.bf=(hCurrent-1) - (htreeB+1)
            else:
                current.bf=(hCurrent) - (htreeB+1)

        else:
            node.bf=hCurrent-2 - (htreeB)
            current.bf=(hCurrent-1) - (htreeB+1)

    else:

        AVL.root=treeB.root

        node.leftnode=treeA.root

        if treeA.root is not None:
            node.leftnode.parent=node

        current=treeB.root

        hCurrent=htreeB

        while hCurrent > htreeA+1:
            hCurrent -= 1
            if current.bf==-1:
                hCurrent -= 1
            current=current.leftnode

        node.rightnode=current.leftnode

        if current.leftnode is not None:
            current.leftnode.parent=node

        current.leftnode=node
        node.parent=current

        if current.bf >= 0:
            node.bf=(htreeA) - (hCurrent-1)
            if current.bf == 1:
                current.bf=(htreeA+1)-(hCurrent-1) 
            else:
                current.bf=(htreeA+1)-(hCurrent)

        else:
            node.bf=(htreeA)-(hCurrent-2)
            current.bf=(htreeA+1)-(hCurrent-1)

    rebalancePath(AVL, current)
    return AVL


def height(current:AVLNode)->int:
    if current is None:
        return 0

    if current.bf<=0:
        return 1 + height(current.rightnode)
    
    return 1 + height(current.leftnode)


def rebalancePath(T:AVLTree, node:AVLNode):
    if node is not None: 

        # Desequilibrio hacia la izquierda
        if node.bf==2:
            node=rotateRight(T, node)
            grew=False   # la rotacion restaura la altura previa

        # Desequilibrio hacia la derecha
        elif node.bf==-2:
            node=rotateLeft(T, node)
            grew=False

        elif node.bf==0:
            grew=False   # la rama corta se empareja, la altura no cambio

        else: #node.bf quedo en 1 o -1
            grew = True 
            

        if grew and node.parent is not None:
            if node.parent.leftnode is node:
                node.parent.bf += 1
            else:
                node.parent.bf -= 1

            rebalancePath(T, node.parent)

    return
def check_bf(node):

    if node is None:
        return 0

    hleft = check_bf(node.leftnode)
    hright = check_bf(node.rightnode)

    expected_bf = hleft - hright

    assert node.bf == expected_bf, (
        f"Error en nodo {node.key}: "
        f"bf guardado = {node.bf}, "
        f"bf esperado = {expected_bf}"
    )

    return 1 + max(hleft, hright)


def check_avl(node):

    if node is None:
        return 0

    hleft = check_avl(node.leftnode)
    hright = check_avl(node.rightnode)

    assert abs(hleft - hright) <= 1, (
        f"El nodo {node.key} no cumple AVL: "
        f"altura izquierda = {hleft}, "
        f"altura derecha = {hright}"
    )

    return 1 + max(hleft, hright)


def check_parent(node):

    if node is None:
        return

    if node.leftnode is not None:
        assert node.leftnode.parent == node
        check_parent(node.leftnode)

    if node.rightnode is not None:
        assert node.rightnode.parent == node
        check_parent(node.rightnode)


def check_bst(node, minimo=None, maximo=None):

    if node is None:
        return

    if minimo is not None:
        assert node.key > minimo

    if maximo is not None:
        assert node.key < maximo

    check_bst(node.leftnode, minimo, node.key)
    check_bst(node.rightnode, node.key, maximo)


def inorder(node):

    if node is None:
        return []

    return (
        inorder(node.leftnode)
        + [node.key]
        + inorder(node.rightnode)
    )


# ============================================================
# TEST
# ============================================================

def test_generarAVL_A_mas_alto():

    # ========================================================
    # A
    #
    #          30
    #         /  \
    #       20    40
    #            /
    #           35
    #
    # altura = 3
    # ========================================================

    A = AVLTree()

    n30 = AVLNode()
    n30.key = 30
    n30.bf = -1

    n20 = AVLNode()
    n20.key = 20
    n20.bf = 0

    n40 = AVLNode()
    n40.key = 40
    n40.bf = 1

    n35 = AVLNode()
    n35.key = 35
    n35.bf = 0

    n30.leftnode = n20
    n30.rightnode = n40

    n20.parent = n30
    n40.parent = n30

    n40.leftnode = n35
    n35.parent = n40

    A.root = n30


    # ========================================================
    # B
    #
    #       60
    #
    # altura = 1
    # ========================================================

    B = AVLTree()

    n60 = AVLNode()
    n60.key = 60
    n60.bf = 0

    B.root = n60


    # ========================================================
    # GENERAMOS EL AVL
    #
    # X = 50
    #
    # 30, 20, 40, 35 < 50 < 60
    # ========================================================

    T = generarAVL(A, B, 50)


    # ========================================================
    # DEBEN ESTAR TODOS LOS ELEMENTOS
    # ========================================================

    assert inorder(T.root) == [20, 30, 35, 40, 50, 60]


    # ========================================================
    # DEBE SER BST
    # ========================================================

    check_bst(T.root)


    # ========================================================
    # DEBE SER AVL
    # ========================================================

    check_avl(T.root)


    # ========================================================
    # LOS BF GUARDADOS DEBEN SER CORRECTOS
    # ========================================================

    check_bf(T.root)


    # ========================================================
    # LOS PARENT DEBEN SER CORRECTOS
    # ========================================================

    assert T.root.parent is None

    check_parent(T.root)


    print("TEST A MÁS ALTO: OK")


# ============================================================
# EJECUTAR TEST
# ============================================================

if __name__ == "__main__":

    test_generarAVL_A_mas_alto()

    print("TODOS LOS TESTS PASARON")
def set_bf(node):

    if node is None:
        return 0

    hleft = set_bf(node.leftnode)
    hright = set_bf(node.rightnode)

    node.bf = hleft - hright

    return 1 + max(hleft, hright)


def test_generarAVL_B_mas_alto():

    # ========================================================
    # A
    #
    #       10
    #      /  \
    #     5    15
    #
    # altura = 2
    # ========================================================

    A = AVLTree()

    n10 = AVLNode()
    n10.key = 10

    n5 = AVLNode()
    n5.key = 5

    n15 = AVLNode()
    n15.key = 15

    n10.leftnode = n5
    n10.rightnode = n15

    n5.parent = n10
    n15.parent = n10

    A.root = n10

    set_bf(A.root)


    # ========================================================
    # B
    #
    #                         100
    #                       /     \
    #                     60       140
    #                    /  \     /   \
    #                  40    80  120   160
    #                 / \      \       /
    #               30  50     90    150
    #
    # B es AVL y altura = 4
    # ========================================================

    B = AVLTree()

    n100 = AVLNode()
    n60 = AVLNode()
    n140 = AVLNode()

    n40 = AVLNode()
    n80 = AVLNode()

    n120 = AVLNode()
    n160 = AVLNode()

    n30 = AVLNode()
    n50 = AVLNode()

    n90 = AVLNode()

    n150 = AVLNode()


    n100.key = 100
    n60.key = 60
    n140.key = 140

    n40.key = 40
    n80.key = 80

    n120.key = 120
    n160.key = 160

    n30.key = 30
    n50.key = 50

    n90.key = 90

    n150.key = 150


    # -------------------------
    # enlaces
    # -------------------------

    n100.leftnode = n60
    n100.rightnode = n140

    n60.parent = n100
    n140.parent = n100


    n60.leftnode = n40
    n60.rightnode = n80

    n40.parent = n60
    n80.parent = n60


    n140.leftnode = n120
    n140.rightnode = n160

    n120.parent = n140
    n160.parent = n140


    n40.leftnode = n30
    n40.rightnode = n50

    n30.parent = n40
    n50.parent = n40


    n80.rightnode = n90
    n90.parent = n80


    n160.leftnode = n150
    n150.parent = n160


    B.root = n100


    # ========================================================
    # CALCULAMOS LOS BF AUTOMÁTICAMENTE
    # ========================================================

    set_bf(B.root)


    # ========================================================
    # PRIMERO VERIFICAMOS QUE B REALMENTE SEA AVL
    # ========================================================

    check_avl(B.root)
    check_bf(B.root)


    # ========================================================
    # X
    #
    # Todos los elementos de A < 20
    # Todos los elementos de B > 20
    # ========================================================

    T = generarAVL(A, B, 20)


    # ========================================================
    # TODOS LOS ELEMENTOS
    # ========================================================

    assert inorder(T.root) == [
        5,
        10,
        15,
        20,
        30,
        40,
        50,
        60,
        80,
        90,
        100,
        120,
        140,
        150,
        160
    ]


    # ========================================================
    # BST
    # ========================================================

    check_bst(T.root)


    # ========================================================
    # AVL
    # ========================================================

    check_avl(T.root)


    # ========================================================
    # BF
    # ========================================================

    check_bf(T.root)


    # ========================================================
    # PARENT
    # ========================================================

    assert T.root.parent is None

    check_parent(T.root)


    print("TEST B MÁS ALTO: OK")

# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":

    test_generarAVL_B_mas_alto()

    print("TODOS LOS TESTS PASARON")