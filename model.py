import math
from DBLogic import insertar_valoracion, LoginLogica, CrearUsuarioLogica, ObtenerValoracionesLogica, devolver_valoraciones_matriz, ObtenerDatosValoraciones
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

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

def Prediccion(usuario, pelicula, vecinos, peliculas):
    dividendo = 0
    divisor = 0
    i = 0
    while i < len(vecinos):
        similitud = SimilitudPearson(peliculas[usuario], peliculas[vecinos[i]])
        dividendo += similitud * (peliculas[vecinos[i]][pelicula] - CalcularCoef(peliculas[vecinos[i]]))
        divisor += similitud
        i += 1
    if divisor == 0:
        return None
    return ((dividendo / divisor) + CalcularCoef(peliculas[usuario]))    

def InsertarValoracion(usr_id, pelicula_id, valoracion):  
    if (valoracion <= 10) and (valoracion > 0):
        insertar_valoracion(usr_id, pelicula_id, valoracion)
    else:
        print("Error al insertar valores")

def obtener_peliculas_similares(pelicula_id, n_similares=5):
    valoraciones = ObtenerDatosValoraciones()
    if not valoraciones:
        return ['No se encontraron datos de valoraciones. Verifica la base de datos.']
    
    pelicula_usuario = {}
    usuarios = set()
    for pelicula, usuario, valoracion in valoraciones:
        if pelicula not in pelicula_usuario:
            pelicula_usuario[pelicula] = {}
        pelicula_usuario[pelicula][usuario] = valoracion
        usuarios.add(usuario)

    if pelicula_id not in pelicula_usuario:
        return [f"No se pudo encontrar valoraciones para la película con ID {pelicula_id}."]

    usuarios = list(usuarios)
    usuario_index = {usuario: idx for idx, usuario in enumerate(usuarios)}
    peliculas = list(pelicula_usuario.keys())
    pelicula_index = {pelicula: idx for idx, pelicula in enumerate(peliculas)}
    matriz = np.zeros((len(peliculas), len(usuarios)))

    for pelicula, ratings in pelicula_usuario.items():
        for usuario, rating in ratings.items():
            matriz[pelicula_index[pelicula]][usuario_index[usuario]] = rating

    similitudes = cosine_similarity(matriz)
    try:
        pelicula_idx = pelicula_index[pelicula_id]
        similitudes_pelicula = similitudes[pelicula_idx]
        peliculas_similares_idx = np.argsort(similitudes_pelicula)[::-1][1:n_similares+1]
        peliculas_similares = [peliculas[idx] for idx in peliculas_similares_idx]
        return peliculas_similares
    except KeyError:
        return [f"Error procesando similitudes para la película con ID {pelicula_id}."]
