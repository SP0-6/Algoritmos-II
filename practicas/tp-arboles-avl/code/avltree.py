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
 
    if right.bf == 1:
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
 
    if left.bf == -1:
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
        reBalance(AVL)

    return newNode.key

def insertR(newNode: AVLNode, current: AVLNode):
    if newNode.key > current.key:
        if current.rightnode is None:
            current.rightnode=newNode
            newNode.parent=current
            
            return
        else:
            insertR(newNode, current.rightnode)
            return
    else:
        if current.leftnode is None:
            current.leftnode=newNode
            newNode.parent=current
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

    if abs(htreeA-htreeB)<=1:
        AVL=AVLTree()        
        AVL.root=node

        node.bf=htreeA-htreeB
        node.leftnode=treeA.root
        node.leftnode.parent=node
        node.rightnode=treeB.root
        node.rightnode.parent=node

        return AVL

    if htreeA>htreeB:

        node.bf=treeB.root.bf-1
        node.rightnode=treeB.root

        if treeB.root is not None:
            node.rightnode.parent=node

        current=treeA.root

        for _ in range(1, htreeA-htreeB):
            current = current.rightnode

        hCurrent=htreeA-htreeB

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
            current.bf=(hCurrent) - (htreeB+1)

        return treeA
    else:
        node.bf=treeA.root.bf-1
        node.leftnode=treeA.root

        if treeA.root is not None:
            node.leftnode.parent=node

        current=treeB.root

        for _ in range(1, htreeB-htreeA):
            current = current.leftnode

        hCurrent=htreeB-htreeA

        node.rightnode=current.leftnode
        if current.leftnode is not None:
            current.leftnode.parent=node

        current.leftnode=node
        node.parent=current

        if current.bf >= 0:
            node.bf=hCurrent-1 - (htreeA)
            if current.bf == 1:
                current.bf=(hCurrent-1) - (htreeA+1)
            else:
                current.bf=(hCurrent) - (htreeA+1)

        else:
            node.bf=hCurrent-2 - (htreeA)
            current.bf=(hCurrent) - (htreeA+1)
    pass



def height(current:AVLNode)->int:
    if current is None:
        return 0

    if current.bf<=0:
        return 1 + height(current.rightnode)
    
    return 1 + height(current.leftnode)