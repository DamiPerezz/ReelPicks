import streamlit as st
import pandas as pd
from DBLogic import LoginLogica, CrearUsuarioLogica

# Título de la aplicación
st.title("Sistema de Recomendación")

# Cargar datos del CSV
@st.cache_data
def cargar_datos():
    return pd.read_csv("peliculas.csv")

datos = cargar_datos()

# Sidebar con opciones
if "usuario" not in st.session_state:
    opcion = st.sidebar.radio(
        "Selecciona una opción", ("Inicio", "Iniciar sesión", "Registrar usuario")
    )
else:
    opcion = st.sidebar.radio(
        f"Bienvenido, {st.session_state.usuario['nombre']}",
        ("Inicio", "Perfil", "TF-IDF y Similitud Coseno", 
         "Similitud Colaborativa", "Buscar Películas Similares", "Cerrar sesión")
    )

# Lógica de inicio de sesión y registro
if opcion == "Iniciar sesión":
    st.subheader("Iniciar sesión")
    email = st.text_input("Email:")
    password = st.text_input("Contraseña:", type="password")

    if st.button("Iniciar sesión"):
        usuario = LoginLogica(email, password)
        if usuario:
            st.session_state.usuario = {"id": usuario[0], "nombre": usuario[1]}
            st.success(f"Bienvenido {usuario[1]}!")
            st.rerun()  # Recargar la página
        else:
            st.error("Credenciales incorrectas.")

elif opcion == "Registrar usuario":
    st.subheader("Registrar usuario")
    nombre = st.text_input("Nombre:")
    email = st.text_input("Email:")
    password = st.text_input("Contraseña:", type="password")

    if st.button("Registrar"):
        if nombre and email and password:
            try:
                CrearUsuarioLogica(nombre, email, password)
                st.success("Usuario registrado con éxito. Ahora puedes iniciar sesión.")
            except Exception as e:
                st.error(f"Error al registrar usuario: {e}")
        else:
            st.error("Por favor, completa todos los campos.")

elif opcion == "Cerrar sesión":
    del st.session_state.usuario  # Eliminar datos de sesión
    st.success("Has cerrado sesión.")
    st.rerun()

# Mostrar contenido según el estado de sesión
if "usuario" in st.session_state:
    if opcion == "Inicio":
        st.subheader("¡Bienvenido!")
        st.write("Accede a las funcionalidades desde el menú lateral.")

    elif opcion == "Perfil":
        st.subheader("Perfil de usuario")
        usuario_id = st.session_state.usuario["id"]
        usuario_nombre = st.session_state.usuario["nombre"]
        st.write(f"Nombre: {usuario_nombre}")

    elif opcion == "TF-IDF y Similitud Coseno":
        st.subheader("TF-IDF y Similitud por Coseno")
        peliculas = datos[["title", "synopsis"]].dropna().drop_duplicates(subset="title")
        st.write("**Películas disponibles:**")
        st.dataframe(peliculas.head(10))

        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(peliculas["synopsis"])
        cos_sim = cosine_similarity(tfidf_matrix)
        df_cos_sim = pd.DataFrame(cos_sim, index=peliculas["title"], columns=peliculas["title"])
        st.write("**Matriz de Similitud de Coseno:**")
        st.dataframe(df_cos_sim)

        seleccion = st.selectbox("Selecciona una película para ver las más similares", peliculas["title"])
        similares = df_cos_sim[seleccion].sort_values(ascending=False).iloc[1:4]
        st.write(f"**Películas más similares a {seleccion}:**")
        st.dataframe(similares)

    elif opcion == "Similitud Colaborativa":
        st.subheader("Sistema Colaborativo")

        from DBLogic import devolver_valoraciones_matriz, leer_nombre_peliculas, insertar_valoracion
        from model import Prediccion, SimilitudPearson

        # Cargar nombres de películas
        peliculas_dict = leer_nombre_peliculas()
        peliculas_nombres = list(peliculas_dict.keys())

        # Barra de búsqueda para seleccionar película
        seleccion_pelicula = st.selectbox("Busca y selecciona una película:", peliculas_nombres)

        if seleccion_pelicula:
            pelicula_id = peliculas_dict[seleccion_pelicula]

            # Valoración de la película
            valoracion = st.slider("Valora la película (1-5):", min_value=1, max_value=5, value=3)

            if st.button("Guardar valoración"):
                usuario_id = st.session_state.usuario["id"]
                try:
        
                    insertar_valoracion(usuario_id, pelicula_id, valoracion)
                    st.success(f"Insertando {usuario_id} en pelicula {pelicula_id} con {valoracion}")
                except Exception as e:
                    st.error(f"Error al guardar la valoración: {e}")

        # Visualización de la matriz de valoraciones
        valoraciones = devolver_valoraciones_matriz()
        st.write("**Matriz de Valoraciones:**")
        st.dataframe(pd.DataFrame(valoraciones))

        # Cálculo de predicción y similitud
        usuario = st.number_input("Selecciona el usuario (indexado desde 0)", min_value=0, max_value=len(valoraciones)-1, value=0)
        pelicula = st.number_input("Selecciona la película (indexada desde 0)", min_value=0, max_value=len(valoraciones[0])-1, value=0)
        vecinos = st.multiselect("Selecciona los vecinos (usuarios similares)",
                                    options=list(range(len(valoraciones))),
                                    default=[i for i in range(1, min(3, len(valoraciones)))])

        if st.button("Calcular Predicción"):
            prediccion = Prediccion(usuario, pelicula, vecinos, valoraciones)
            st.write(f"Predicción de la valoración para el Usuario {usuario} en la Película {pelicula}: {prediccion:.2f}")

        st.write("**Similitud de Pearson entre Usuarios:**")
        usuario1 = st.number_input("Usuario 1", min_value=0, max_value=len(valoraciones)-1, value=0)
        usuario2 = st.number_input("Usuario 2", min_value=0, max_value=len(valoraciones)-1, value=1)

        if st.button("Calcular Similitud"):
            similitud = SimilitudPearson(valoraciones[usuario1], valoraciones[usuario2])
            st.write(f"Similitud de Pearson entre Usuario {usuario1} y Usuario {usuario2}: {similitud:.2f}")

    elif opcion == "Buscar Películas Similares":
        st.subheader("Buscar Películas Similares por Nombre")

        from DBLogic import leer_peliculas_con_valoraciones, obtener_nombres_peliculas
        from model import obtener_peliculas_similares

        peliculas_dict = leer_peliculas_con_valoraciones()
        peliculas_nombres = list(peliculas_dict.keys())

        seleccion_pelicula = st.selectbox("Busca y selecciona una película:", peliculas_nombres)

        if seleccion_pelicula:
            pelicula_id = peliculas_dict[seleccion_pelicula]
            st.write(f"**ID de la película seleccionada:** {pelicula_id}")

            num_similares = st.slider("Número de películas similares:", min_value=1, max_value=10, value=5)
            similares_ids = None
            if st.button("Buscar"):
                similares_ids = obtener_peliculas_similares(pelicula_id, num_similares)
            if similares_ids:
                # Obtener los nombres de las películas similares
                similares_nombres = obtener_nombres_peliculas(similares_ids)
                st.write(f"**Películas similares a '{seleccion_pelicula}':**")
                for similar in similares_nombres:
                    st.write(f"- {similar}")

else:
    st.write("Inicia sesión o regístrate para acceder al contenido.")
