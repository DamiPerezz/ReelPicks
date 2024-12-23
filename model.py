import math
from DBLogic import insertar_valoracion, devolver_valoraciones_matriz
import pandas as pd


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
    # print(formulaDividendo)
    linea = len(formulaDividendo) * "-"
    # print(linea)
    # print(formulaDivisor)
    return ((dividendo/divisor) + CalcularCoef(peliculas[usuario]))    
def InsertarValoracion(usr_id,pelicula_id,valoracion):  
    if((valoracion <= 10) and (valoracion > 0)):
        insertar_valoracion(usr_id,pelicula_id)
    else:
        print("Error al insertar valores")

"""
Encuentra las N películas más similares a la película dada basada en similitudes de coseno.

Args:
    titulo (str): El título de la película base.
    N (int): El número de películas similares a devolver.

Returns:
    DataFrame: Un DataFrame con las N películas más similares y sus puntuaciones de similitud.
"""
def topN_similitudCoseno(titulo, N):
    # Cargar la matriz de similitud precalculada
    cos_sim_df = pd.read_csv("cosine_similarity_matrix.csv", index_col=0)
    
    # Verificar que el título dado está en la matriz
    if titulo not in cos_sim_df.index:
        raise ValueError(f"El título '{titulo}' no está en la base de datos.")
    
    # Ordenar las películas por similitud respecto al título dado
    similares = cos_sim_df[titulo].sort_values(ascending=False)
    
    # Crear una lista para almacenar resultados únicos
    resultados = []
    vistos = set()  # Para rastrear títulos ya incluidos
    
    # Iterar sobre las películas similares
    for idx, similitud in similares.items():
        if idx != titulo and idx not in vistos:  # Excluir la película misma y duplicados
            resultados.append((idx, similitud))
            vistos.add(idx)
        if len(resultados) == N:  # Detener al alcanzar el número deseado
            break
    
    # Convertir a DataFrame
    resultados_df = pd.DataFrame(resultados, columns=["Título", "Similitud"])
    return resultados_df

print(topN_similitudCoseno("Captain America: The Winter Soldier", 10))