def MitadMenores(A:list)->list:
    # Si hay menos de 3 elementos, devuelve la lista sin modificar
    if len(A)<3:
        return A
    
    menores=[]
    resto=[]

    # El primer elemento de la lista se toma como pivote, luego se separan los elementos según sean menores o no que el primero
    for i in A[1:]:
        if i<A[0]:
            menores.append(i)
        else:
            resto.append(i)

    # Coloca la mitad de cada grupo antes y la otra mitad después del primer elemento. Se usa round para la lista resto y se trunca la lista menores
    #por si ambas tienen un número impar de elementos, y si usaramos la misma operación para las dos, el pivote no quedaría al medio.
    return menores[:len(menores)//2] + resto[:round(len(resto)/2)] + [A[0]] + menores[len(menores)//2:] + resto[round(len(resto)/2):]