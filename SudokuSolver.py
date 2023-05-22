import time
import heapq

def celdaVacia(sudo): #Buscamos la siguiente celda vacia
    for i in range(9):
        for j in range(9):
            if sudo[i][j] == 0:
                return (i, j)
    return None

def valorCorrecto(sudo, row, col, num): #Para checar si es valido el numero segun el 3x3 o la columna o la fila
    
    for i in range(9): #Buscamos en la fila.
        if sudo[row][i] == num:
            return False
    
    for j in range(9): #Buscamos en la columna.
        if sudo[j][col] == num:
            return False
    
    fila3x3 = (row // 3) * 3 # Buscamos num en el cuadro 3x3
    col3x3 = (col // 3) * 3
    for i in range(fila3x3, fila3x3 + 3):
        for j in range(col3x3, col3x3 + 3):
            if sudo[i][j] == num:
                return False

    return True #Mi numero sirve

def solveDFS(sudo): #Usamos DFS

    sigCelda = celdaVacia(sudo) #Buscamos la celda vacia
    
    if sigCelda is None: #True si no hay mas celdas vacias.
        return True
    
    row, col = sigCelda #Probamos las combinaciones posibles
    for num in range(1, 10):
        if valorCorrecto(sudo, row, col, num):
            sudo[row][col] = num

            if solveDFS(sudo):
                return True
        #Backtracking
            sudo[row][col] = 0
    #Backtracking
    return False #No solucion

def valoresPosiblesCelda(sudo, row, col): #El nombre lo dice
    vals = set(range(1, 10))
    vals -= set(sudo[row]) # Quitamos valores fila
    vals -= set(sudo[i][col] for i in range(9)) # Quitamos valores columna
    vals -= set(sudo[row//3*3 + i][col//3*3 + j] for i in range(3) for j in range(3)) # Quitamos valores de mi 3x3
    return vals #Valores posibles

def celdaMenor(sudo): #Buscamos la celda con menores valores posibles
    celdaMenosVals = float("inf")
    for row in range(9):
        for col in range(9):
            if sudo[row][col] == 0:
                grado = len(valoresPosiblesCelda(sudo, row, col))
                if grado < celdaMenosVals: #Comparamos cada celda
                    celdaMenosVals = grado
                    filaMenos, colMenos = row, col
    return filaMenos, colMenos #Valores de la celda encontrada

def heuristica(sudo): #Segun menores valores ppsibles en la celda
    return sum(len(valoresPosiblesCelda(sudo, row, col)) for row in range(9) for col in range(9) if sudo[row][col] == 0)

def solveBusquedaInformada(sudo): 
    start_time = time.time() #Para medir el tiempo#Usamos A*
    queue = [(heuristica(sudo), sudo)]
    heapq.heapify(queue)
    while queue:
        _, SudoAct = heapq.heappop(queue)

        if not any(0 in row for row in SudoAct): # Ver si sudoku completo
            return SudoAct

        row, col = celdaMenor(SudoAct) # Celda con menores posibilidades

        valores_posibles = valoresPosiblesCelda(SudoAct, row, col) #Buscamos los valores posibles

        for valor in valores_posibles: #Resolvems segun cada valor posible
            new_SudoAct = [row[:] for row in SudoAct]
            new_SudoAct[row][col] = valor
            aux = heuristica(new_SudoAct)
            heapq.heappush(queue, (aux, new_SudoAct))

    return None

#------------------------------------------------------------------------------------------------------------------------------------------

sudo1 = [
    [0,0,0,2,0,0,0,0,0],
    [8,0,9,0,0,0,1,0,0],
    [0,2,0,0,0,0,0,0,0],
    [6,0,3,0,0,9,0,0,0],
    [0,7,0,6,0,0,0,5,0],
    [0,0,0,0,4,0,9,0,3],
    [0,4,0,0,8,0,0,3,0],
    [0,0,6,9,0,0,0,7,0],
    [0,9,5,0,0,1,0,0,2],
]

sudo2 = [
    [0,0,0,2,0,0,0,0,0],
    [8,0,9,0,0,0,1,0,0],
    [0,2,0,0,0,0,0,0,0],
    [6,0,3,0,0,9,0,0,0],
    [0,7,0,6,0,0,0,5,0],
    [0,0,0,0,4,0,9,0,3],
    [0,4,0,0,8,0,0,3,0],
    [0,0,6,9,0,0,0,7,0],
    [0,9,5,0,0,1,0,0,2],
]

print("-----------------------------------------------------------------------------------------")
print("Solucion con Busqueda no Informada")
start_time = time.time() #Para medir el tiempo
if solveDFS(sudo1):
    print("\tSudoku solucionado:")
    for row in sudo1:
        print("\t",row)
else:
    print("Solucion no encontrada.")
end_time = time.time() #Terminamos timer

print("Tiempo total: {:.5f} segundos".format(end_time - start_time))

print("-----------------------------------------------------------------------------------------")
print("Solucion con Busqueda Informada")
start_time = time.time() #Para medir el tiempo
solution = solveBusquedaInformada(sudo2)
if solution:
    print("\tSudoku solucionado:")
    for row in solution:
        print("\t",row)
else:
    print("Solucion no encontrada.")
end_time = time.time() #Terminamos timer

print("Tiempo total: {:.5f} segundos".format(end_time - start_time))