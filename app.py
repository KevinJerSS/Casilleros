import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title="Casilleros Metro Emancipación",
    page_icon="🛒",
    layout="centered"
)

# Inyección de CSS para los colores reales de Metro Cencosud (Amarillo y Rojo)
st.markdown("""
    <style>
    .metro-title {
        background-color: #FFD200; /* Amarillo Metro */
        color: #E2001A; /* Rojo Metro */
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-family: 'Arial', sans-serif;
        font-weight: 900;
        margin-bottom: 25px;
        border: 2px solid #E2001A;
    }
    .info-card {
        background-color: #f4f4f4;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #E2001A; /* Detalle en Rojo Metro */
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="metro-title">Tienda Metro Emancipación<br>Gestión de Casilleros</h1>', unsafe_allow_html=True)

if 'seleccion' not in st.session_state:
    st.session_state.seleccion = None

def obtener_datos_colaborador(modulo, casillero):
    areas = ["Cajas", "Frescos", "Abarrotes", "Prevención", "Almacén", "Electro", "Carnes", "Bazar"]
    area_asignada = areas[(modulo + casillero) % len(areas)]
    
    return {
        "nombre": f"Colaborador M{modulo}-C{casillero}",
        "area": area_asignada,
        # Se actualizó el color del placeholder a rojo para que combine
        "imagen": f"https://via.placeholder.com/150/E2001A/FFFFFF?text=M{modulo}-C{casillero}"
    }

st.write("### Navega por los módulos y selecciona un casillero:")

nombres_modulos = [f"Módulo {i}" for i in range(1, 9)]
tabs = st.tabs(nombres_modulos)

for i, tab in enumerate(tabs):
    num_modulo = i + 1
    with tab:
        # Cuadrícula: 4 filas x 3 columnas
        filas = 4
        columnas = 3
        
        for fila in range(filas):
            cols = st.columns(columnas)
            for col_idx in range(columnas):
                num_casillero = (fila * columnas) + col_idx + 1
                
                with cols[col_idx]:
                    if st.button(f"Casillero {num_casillero}", key=f"btn_m{num_modulo}_c{num_casillero}", use_container_width=True):
                        st.session_state.seleccion = {"modulo": num_modulo, "casillero": num_casillero}

st.divider()

if st.session_state.seleccion:
    mod = st.session_state.seleccion["modulo"]
    casillero = st.session_state.seleccion["casillero"]
    
    colaborador = obtener_datos_colaborador(mod, casillero)
    
    st.subheader(f"Información: Módulo {mod} - Casillero {casillero}")
    
    col_img, col_info = st.columns([1, 2])
    
    with col_img:
        st.image(colaborador["imagen"], width=150)
        
    with col_info:
        st.markdown(f"""
        <div class="info-card">
            <h3 style="color:#E2001A; margin-top:0;">{colaborador["nombre"]}</h3>
            <p><strong>Área asignada:</strong> {colaborador["area"]}</p>
            <p><strong>Estado:</strong> Ocupado</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Selecciona un casillero en la cuadrícula superior.")
