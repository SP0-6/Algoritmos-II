def ContieneSuma(A:list, n:int)->bool:
    # Si hay menos de dos elementos, no puede existir un par
    if len(A)<2:
        return False

    # Ordena la lista para poder utilizar dos punteros (la función sort de python ordena con complejidad n*log n)
    A.sort()

    menor=0
    mayor=len(A)-1

    # Compara el menor y el mayor elemento mientras no se crucen
    while menor!=mayor:
        
        # Si la suma es menor que n, aumenta el menor
        if A[menor]+A[mayor]<n:
            menor+=1

        # Si la suma es mayor que n, disminuye el mayor
        elif A[menor]+A[mayor]>n:
            mayor-=1

        # Si la suma coincide con n, encontró un par
        else:
            return True
        
    # No se encontró ningún par que sume n
    return False