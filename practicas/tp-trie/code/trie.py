class Trie:
	root=None

class TrieNode:
    parent=None
    children=None   
    key=None
    isEndOfWord=False


def insert(T:Trie, element):
    #Crea la raíz si el Trie está vacío
    if T.root is None:
        T.root=TrieNode()

    current=T.root

    #Recorre cada letra de la palabra
    for i in element:
        node=findKey(current, i)

        #Si la letra no existe, crea el nodo
        if node is None:
            node=TrieNode()
            node.key=i
            node.parent=current

            #Agrega el nodo a los hijos
            if current.children is None:
                current.children=[node]
            else:
                current.children.append(node)

        #Avanza al nodo de la letra
        current=node

    current.isEndOfWord=True

 
def findKey(node:TrieNode, key):
    #devuelve el nodo con la key buscada dentro de children
    if node is None or node.children is None:
        return None
    
    for child in node.children:
        if child.key == key:
            return child
    return None

def search(T:Trie, element):
    #Recorre el Trie siguiendo cada letra
    current=T.root
    
    for i in element:
        node=findKey(current, i)
        
        #La palabra no existe
        if node is None:
            return False
        
        current=node
    
    #Verifica que sea una palabra completa
    return current.isEndOfWord
 
 
def delete(T:Trie, element):
    #Recorre el Trie buscando la palabra
    current=T.root      
 
    for i in element:
        node=findKey(current, i)
        
        #La palabra no existe
        if node is None:
            return False

        #Si el nodo no tiene hijos, se puede eliminar
        if not node.isEndOfWord and (node.children is None or len(node.children)==0):
            
            #Busca y elimina el nodo de su padre
            for j in range(len(node.parent.children)):
                if node.parent.children[j] == node:
                    node.parent.children.pop(j)
                    break
        
        current=node
 
    #No era una palabra completa
    if not current.isEndOfWord:
        return False
 
    #Desmarca el final de la palabra
    current.isEndOfWord=False

    return True
 
 
def prefijoLongitud(T:Trie, p, n:int)->list:

    result=[]

    #El prefijo no puede superar la longitud buscada
    if len(p) > n:
        return result
 
    current=T.root
    
    #Busca el prefijo en el Trie
    for i in p:
        node=findKey(current, i)
        
        #El prefijo no existe
        if node is None:
            return result
        
        current=node

    #Busca palabras hasta alcanzar longitud n
    prefijoLongitudR(current, p, n - len(p), result)

    return result
 
 
def prefijoLongitudR(node:TrieNode, subcadena, resto:int, result:list):
    
    #Si llegó a longitud n, verifica si es palabra
    if resto == 0:
        if node.isEndOfWord:
            result.append(subcadena)
        return
    
    #No hay más letras para continuar
    if node.children is None:
        return
    
    #Explora todos los hijos posibles
    for child in node.children:
        prefijoLongitudR(child,subcadena + child.key,resto - 1,result)

 
def mismoDoc(T1:Trie, T2:Trie)->bool:

    #Obtiene las palabras de ambos Tries
    words1=getPalabras(T1)
    words2=getPalabras(T2)
 
    #Si tienen distinta cantidad, no son iguales
    if len(words1) != len(words2):
        return False
 
    #Verifica que todas las palabras coincidan
    for w1 in words1:
        if not w1 in words2:
            return False
 
    return True
 

def getPalabras(T):
    #Obtiene todas las palabras del Trie
    result=[]
    palabrasR(T.root, "", result)
    return result
 

def palabrasR(node, subcadena, result):
    
    if node is None:
        return
    #Guarda la palabra si llegó a su final
    if node.isEndOfWord:
        result.append(subcadena)

    if node.children is None:
        return
    
    #Recorre todos los hijos
    for child in node.children:
        palabrasR(child, subcadena + child.key, result)

def palindromo(T):
    #Obtiene todas las palabras del trie
    words=getPalabras(T)
    for w in words:
        #Invierte cada palabra y la busca. Si encuentra alguna coincidencia, devuelve True
        r=w[::-1]
        if r in words:
            return True
    return False


def autoCompletar(T, cadena):

    current=T.root
    #Busca la cadena introducida y llega hasta su última letra
    for i in cadena:
        node=findKey(current, i)
        if node is None:
            return ""
        current=node
 
    subcadena=""

    while current is not None:
        #Avanza mientras haya un único camino posible
        if current.children is not None:
            lenChildren=len(current.children)
        else: 
            lenChildren=0
 
        if current.isEndOfWord and lenChildren > 0:
            #Palabra completa con más caminos: se devuelve lo que se tiene para evitar ambiguedad
            return subcadena
 
        if current.isEndOfWord and lenChildren == 0:
            #Única hoja alcanzada: completado único encontrado
            return subcadena
 
        if lenChildren != 1:
            #más de 1 hijo: ambigüedad, se devuelve lo obtenido hasta ahí
            return subcadena
 
        #Queda un solo camino a recorrer porque len(children) es 1
        current=current.children[0]
        subcadena += current.key
 