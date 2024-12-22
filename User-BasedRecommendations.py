import math

peliculas = [
    [5, 3, 4, 4, None],  # Vera
    [3, 1, 2, 3, 3],     # Usuario1
    [4, 3, 4, 3, 5],     # Usuario2
    [3, 3, 1, 5, 4],     # Usuario3
    [1, 5, 5, 2, 1]      # Usuario4
]

peliculas2 = [ 
    [1,2,1,None],
    [4,3,3,5],
    [3,4,5,3],
    [2,2,3,2]
]

peliculas3 = [ 
    [1,5,4],
    [3,2,5],
    [4,None,4],
    [2,1,3]
]
import math

def CalcularCoef(usr):
    i = 0
    acum = 0
    its = 0
    while i < len(usr):
        if usr[i] is not None:
            acum += usr[i]
            its += 1
        i += 1
    return (acum / its) if its > 0 else 0  

def SimilitudPearson(usr1, usr2):
    i = 0
    dividendo = 0
    raiz = 0
    raiz2 = 0
    r1 = CalcularCoef(usr1)
    r2 = CalcularCoef(usr2)
    if len(usr1) == len(usr2):
        while i < len(usr1):
            if usr1[i] is not None and usr2[i] is not None:
                dividendo += (usr1[i] - r1) * (usr2[i] - r2)
                raiz += (usr1[i] - r1) ** 2
                raiz2 += (usr2[i] - r2) ** 2
            i += 1
        if raiz == 0 or raiz2 == 0:  
            return 0
        return dividendo / (math.sqrt(raiz) * math.sqrt(raiz2))
    return None 

def Prediccion(usuario,pelicula,vecinos,peliculas):
    dividendo = 0
    divisor = 0
    i = 0
    formulaDividendo = ""
    formulaDivisor = ""
    while(i<len(vecinos)):
        similitud = SimilitudPearson(peliculas[usuario], peliculas[vecinos[i]])
        if i == len(vecinos)-1:
            formulaDividendo = formulaDividendo + f"[{similitud} * ({peliculas[vecinos[i]][pelicula]}) - {CalcularCoef(peliculas[vecinos[i]])}]"
            formulaDivisor = formulaDivisor + f"{similitud}"
        else:
            formulaDividendo = formulaDividendo + f"[{similitud} * ({peliculas[vecinos[i]][pelicula]}) - {CalcularCoef(peliculas[vecinos[i]])}] + "
            formulaDivisor = formulaDivisor + f"{similitud} + "
        dividendo = dividendo + (similitud) * (peliculas[vecinos[i]][pelicula] - CalcularCoef(peliculas[vecinos[i]]))
        divisor = divisor + similitud
        i=i+1
    print(formulaDividendo)
    linea = len(formulaDividendo) * "-"
    print(linea)
    print(formulaDivisor)
    return ((dividendo/divisor) + CalcularCoef(peliculas[usuario]))    

peliculas3 = [ 
    [1, 5, 4],
    [3, 2, 5],
    [4, None, 4],
    [2, 2, 3]
]

print("Similitudes con Vera:")
for i in range(1, len(peliculas)):
    coef = SimilitudPearson(peliculas[0], peliculas[i])  # Vera es el usuario 0
    print(f"Similitud con usuario {i}: {coef}")

topVecinos = [1,2]

usuario_vera = 0  # Índice de Vera en la matriz
columna_e5 = 4    # Índice de e5

# Llamada a Prediccion
prediccion_e5 = Prediccion(usuario_vera, columna_e5, topVecinos, peliculas)
print(f"Predicción para e5 (Vera): {prediccion_e5}")

# topsim = {"similitud" : 0, "index" : 0}
# while(i<len(peliculas)):
#     coef = CalcularCoef(peliculas[i])
#     similitud = SimilitudPearson(peliculas[0], peliculas[i])
#     if similitud > topsim['similitud']:
#         topsim["similitud"] = similitud
#         topsim['index'] = i
#     print(f"Similitud de Pearson con usuario {i}={similitud}")
#     i=i+1
# print(f"El usuario con mayor similitud es {topsim['index']} con {topsim['similitud']} ")

# TopVecinos = [1,2] 
# pelicula = 4

# print("Prediccion:")

# print(Prediccion(0,pelicula,TopVecinos))