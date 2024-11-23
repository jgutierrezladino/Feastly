import streamlit as st

# Configurar la página
st.set_page_config(
    page_title="Mi Aplicación",
    page_icon="📊",
    initial_sidebar_state="collapsed"
)

# Aplicar estilo CSS personalizado
st.markdown(
    """
    <style>
    /* Cambiar color de fondo de la barra lateral y la página principal */
    [data-testid="stSidebar"] {
        background-color: #9D1F13;  /* Rojo */
    }
    .stApp {
        background-color: #ff3816;  /* Rojo más intenso */
    }
    /* Centrar el contenido */
    .centered-container {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Agregar una clase CSS para aumentar el tamaño de fuente
st.markdown(
    """
    <style>
    .increased-font {
        font-size: 1.2em;  /* Ajusta el tamaño de fuente según tus necesidades */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Crear barra lateral con un menú
menu = st.sidebar.radio("Menu", ["Home", "Recomendaciones", "Análisis de Datos"])

# Mostrar contenido según la selección del menú
if menu == "Home":
    with st.container():
        st.markdown("<div class='centered-container'><h1>Feastly</h1></div>", unsafe_allow_html=True)
        st.divider()
        st.markdown("<div class='centered-container'><h2>El futuro de la gastronomía</h2></div>", unsafe_allow_html=True)
        st.image("Logo Feastly.png", width=680)
        
    # Introducción
    with st.container():
        st.write("""
        <p class="increased-font">
        Feastly es un sistema de recomendaciones de restaurantes diseñado para ofrecer una experiencia gastronómica personalizada y de 
        alta calidad. A diferencia de otras plataformas de recomendaciones, Feastly se especializa en sugerir lugares que se ajusten a 
        las preferencias y gustos de cada usuario, basándose en un análisis profundo de datos y las experiencias previas de otros comensales. 
        Además, brindamos información confiable sobre ubicaciones y ambientes para garantizar que cada recomendación se adapte a lo que el 
        usuario realmente desea.
        En un mercado lleno de opciones para descubrir restaurantes, Feastly se posiciona como un asistente culinario personalizado. No nos 
        limitamos a ofrecer una simple lista de opciones; nuestro objetivo es crear experiencias únicas que se alineen con las expectativas y 
        preferencias de cada usuario. 
        </p>
        """, unsafe_allow_html=True)

    # ¿Qué nos diferencia de las demás plataformas?
    with st.container():
        st.divider()
        st.markdown("<div class='centered-container'><h1>¿Qué nos diferencia de las demás plataformas?</h1></div>", unsafe_allow_html=True)
        st.write("""
    * **Selección Personalizada de Restaurantes:** En Feastly, nos aseguramos de sugerir restaurantes que realmente coincidan con los gustos y 
    hábitos de cada usuario. No se trata solo de mostrar opciones, sino de garantizar que cada recomendación cumpla con sus expectativas.
    * **Reseñas Detalladas y Verificadas:** Valoramos la transparencia y la confianza. Cada reseña en Feastly es verificada y detallada, 
    proporcionada por comensales reales que han experimentado cada lugar. Esto nos permite ofrecer una visión precisa de lo que cada restaurante 
    tiene para ofrecer.
    * **Información de Ubicación y Ambiente:** Además de sugerir restaurantes, proporcionamos datos sobre la ubicación y el ambiente de cada 
    establecimiento, ayudando a los usuarios a tomar decisiones informadas sobre dónde disfrutar su próxima comida.
    """)
    
    # Objetivo Principal
    with st.container():
        st.divider()
        st.markdown("<div class='centered-container'><h1>Objetivo Principal</h1></div>", unsafe_allow_html=True)
        st.write("""
        <p class="increased-font">
        Desarrollar una plataforma web que realice recomendaciones de restaurantes mediante machine learning, utilizando las preferencias del 
        usuario en cuanto a tipo de cocina, ubicación y ambiente. El tiempo de respuesta para generar cada recomendación será de 
        menos de 30 segundos, utilizando herramientas en la nube y asegurando un tiempo de implementación no mayor a 6 semanas.
        </p>
        """, unsafe_allow_html=True)


elif menu == "Recomendaciones":
    with st.container():
        st.markdown("<div class='centered-container'><h1>¡Descubre tu próximo favorito!</h1></div>", unsafe_allow_html=True)
        st.write("""
        <p class="increased-font">
        Dinos qué es lo que estás buscando para tu próxima experiencia culinaria. (Solo inglés)
        </p>
        """, unsafe_allow_html=True)
        
        # Agregar el cuadro de texto para la preferencia del usuario
        preferencia = st.text_input("Ejemplo: I feel like Sushi or Pizza")
        st.write("""
        <p class="increased-font">
        ¡Basándonos en tus preferencias, hemos seleccionado 5 lugares que creemos que te encantarán!
        </p>
        """, unsafe_allow_html=True)

        # Agregar la imagen
        st.image("Tarjetas Recomendaciones.png", width=1200)

elif menu == "Análisis de Datos":
    with st.container():
        st.markdown("<div class='centered-container'><h1>Dashboard</h1></div>", unsafe_allow_html=True)
        st.markdown("<div class='centered-container'><h1>EDA</h1></div>", unsafe_allow_html=True)
        st.write("""
        <p class="increased-font">
        Para ver mas en profundidad el Analisis Exploratorio de Datos, puedes visitar nuestro Github:
        </p>
        """, unsafe_allow_html=True)
        st.link_button("Ir a GitHub", "https://github.com/jgutierrezladino/Feastly")
        st.image("Eda1.ong.png", width=900)
        st.image("Eda2.png", width=900)
        
