import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from model import Prediccion, SimilitudPearson
from DBLogic import devolver_valoraciones_matriz

# Título de la aplicación
st.title("Sistema de Recomendación: TF-IDF y Similitud Colaborativa")

# Cargar datos del CSV
@st.cache_data
def cargar_datos():
    return pd.read_csv("peliculas.csv")

try:
    datos = cargar_datos()
except FileNotFoundError:
    st.error("No se encontró el archivo 'peliculas.csv'. Asegúrate de que esté en la misma carpeta que este script.")
    st.stop()

st.sidebar.header("Opciones")
opcion = st.sidebar.selectbox(
    "Selecciona una funcionalidad",
    ("TF-IDF y Similitud Coseno", "Similitud Colaborativa")
)

if opcion == "TF-IDF y Similitud Coseno":
    # Muestra información sobre TF-IDF
    st.subheader("TF-IDF y Similitud por Coseno")
    
    # Filtrar datos relevantes
    peliculas = datos[["title", "synopsis"]].dropna()
    peliculas = peliculas.drop_duplicates(subset="title")  # Eliminar títulos duplicados
    
    # Mostrar primeros registros
    st.write("**Películas disponibles:**")
    st.dataframe(peliculas.head(10))

    # Calcular TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(peliculas["synopsis"])

    # Calcular similitudes de coseno
    cos_sim = cosine_similarity(tfidf_matrix)
    df_cos_sim = pd.DataFrame(cos_sim, index=peliculas["title"], columns=peliculas["title"])

    # Verificar que no haya problemas en la matriz
    if df_cos_sim.isnull().values.any():
        st.error("Se encontraron valores nulos en la matriz de similitud. Verifica los datos de entrada.")
        st.stop()

    st.write("**Matriz de Similitud de Coseno:**")
    st.dataframe(df_cos_sim)

    # Seleccionar película para mostrar las más similares
    seleccion = st.selectbox("Selecciona una película para ver las más similares", peliculas["title"])
    similares = df_cos_sim[seleccion].sort_values(ascending=False).iloc[1:4]

    st.write(f"**Películas más similares a {seleccion}:**")
    st.dataframe(similares)

elif opcion == "Similitud Colaborativa":
    st.subheader("Sistema Colaborativo")

    # Obtener datos de la base de datos
    valoraciones = devolver_valoraciones_matriz()

    # Mostrar matriz de valoraciones
    st.write("**Matriz de Valoraciones:**")
    st.dataframe(pd.DataFrame(valoraciones))

    usuario = st.number_input("Selecciona el usuario (indexado desde 0)", min_value=0, max_value=len(valoraciones)-1, value=0)
    pelicula = st.number_input("Selecciona la película (indexada desde 0)", min_value=0, max_value=len(valoraciones[0])-1, value=0)

    vecinos = st.multiselect(
        "Selecciona los vecinos (usuarios similares)",
        options=list(range(len(valoraciones))),
        default=[i for i in range(1, min(3, len(valoraciones)))]
    )

    if st.button("Calcular Predicción"):
        prediccion = Prediccion(usuario, pelicula, vecinos, valoraciones)
        st.write(f"Predicción de la valoración para el Usuario {usuario} en la Película {pelicula}: {prediccion:.2f}")

    st.write("**Similitud de Pearson entre Usuarios:**")
    usuario1 = st.number_input("Usuario 1", min_value=0, max_value=len(valoraciones)-1, value=0)
    usuario2 = st.number_input("Usuario 2", min_value=0, max_value=len(valoraciones)-1, value=1)

    if st.button("Calcular Similitud"):
        similitud = SimilitudPearson(valoraciones[usuario1], valoraciones[usuario2])
        st.write(f"Similitud de Pearson entre Usuario {usuario1} y Usuario {usuario2}: {similitud:.2f}")
