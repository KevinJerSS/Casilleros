import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE LA PÁGINA Y TEMA OSCURO
st.set_page_config(
    page_title="Casilleros Metro Emancipación",
    page_icon="🛒",
    layout="wide" 
)

# CSS para Modo Oscuro y Colores Metro
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    
    .metro-title {
        background-color: #1E1E1E; 
        color: #FFD200; 
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-family: 'Arial', sans-serif;
        font-weight: 900;
        margin-bottom: 25px;
        border: 2px solid #E2001A; 
        box-shadow: 0px 4px 10px rgba(226, 0, 26, 0.2);
    }
    
    .info-card {
        background-color: #1E1E1E;
        color: #FFFFFF;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #E2001A; 
        box-shadow: 0px 4px 6px rgba(0,0,0,0.5);
    }
    
    .info-name {
        color: #E2001A; 
        margin-top: 0;
        font-weight: bold;
        font-size: 1.5em;
    }
    </style>
""", unsafe_allow_html=True)

# 2. INICIALIZAR BASE DE DATOS EN MEMORIA (SIN COLUMNA DE IMAGEN)
if 'df_colaboradores' not in st.session_state:
    datos_iniciales = []
    for m in range(1, 9):
        for c in range(1, 13):
            datos_iniciales.append({
                "Modulo": m,
                "Casillero": c,
                "Nombre": "Vacío", 
                "Area": "Sin asignar"
            })
    st.session_state.df_colaboradores = pd.DataFrame(datos_iniciales)

if 'seleccion' not in st.session_state:
    st.session_state.seleccion = None

# --- PANEL DE ADMINISTRACIÓN (BARRA LATERAL) ---
with st.sidebar:
    st.markdown('<h2 style="color:#FFD200;">⚙️ Administrar Casilleros</h2>', unsafe_allow_html=True)
    st.write("Agrega o edita la información de un colaborador aquí:")
    
    # Formularios de entrada
    mod_edit = st.selectbox("Módulo:", options=list(range(1, 9)))
    cas_edit = st.selectbox("Casillero:", options=list(range(1, 13)))
    
    nuevo_nombre = st.text_input("Nombre del Colaborador:")
    nueva_area = st.selectbox("Área:", ["Cajas", "Frescos", "Abarrotes", "Prevención", "Almacén", "Electro", "Carnes", "Bazar", "Sin asignar"])
    
    if st.button("Guardar Cambios", use_container_width=True):
        # Actualizar el DataFrame en la memoria
        idx = st.session_state.df_colaboradores[
            (st.session_state.df_colaboradores['Modulo'] == mod_edit) & 
            (st.session_state.df_colaboradores['Casillero'] == cas_edit)
        ].index
        
        st.session_state.df_colaboradores.loc[idx, 'Nombre'] = nuevo_nombre
        st.session_state.df_colaboradores.loc[idx, 'Area'] = nueva_area
        
        st.success(f"¡Casillero {cas_edit} del Módulo {mod_edit} actualizado!")

# --- INTERFAZ PRINCIPAL ---
st.markdown('<h1 class="metro-title">Tienda Metro Emancipación<br>Gestión de Casilleros</h1>', unsafe_allow_html=True)
st.write("### Navega por los módulos y selecciona un casillero:")

# Creación de pestañas para los 8 Módulos
nombres_modulos = [f"Módulo {i}" for i in range(1, 9)]
tabs = st.tabs(nombres_modulos)

for i, tab in enumerate(tabs):
    num_modulo = i + 1
    with tab:
        filas, columnas = 4, 3
        for fila in range(filas):
            cols = st.columns(columnas)
            for col_idx in range(columnas):
                num_casillero = (fila * columnas) + col_idx + 1
                
                # Buscar estado actual para pintar diferente si está ocupado
                ocupado = st.session_state.df_colaboradores[
                    (st.session_state.df_colaboradores['Modulo'] == num_modulo) & 
                    (st.session_state.df_colaboradores['Casillero'] == num_casillero)
                ].iloc[0]['Nombre'] != "Vacío"
                
                label = f"Casillero {num_casillero}" + (" 👤" if ocupado else "")
                
                with cols[col_idx]:
                    if st.button(label, key=f"btn_m{num_modulo}_c{num_casillero}", use_container_width=True):
                        st.session_state.seleccion = {"modulo": num_modulo, "casillero": num_casillero}

st.divider()

# --- MOSTRAR LA INFORMACIÓN DEL CASILLERO SELECCIONADO (SIN IMAGEN) ---
if st.session_state.seleccion:
    mod = st.session_state.seleccion["modulo"]
    casillero = st.session_state.seleccion["casillero"]
    
    # Extraer datos actualizados
    datos_cas = st.session_state.df_colaboradores[
        (st.session_state.df_colaboradores['Modulo'] == mod) & 
        (st.session_state.df_colaboradores['Casillero'] == casillero)
    ].iloc[0]
    
    st.subheader(f"Información: Módulo {mod} - Casillero {casillero}")
    
    estado = "Ocupado" if datos_cas["Nombre"] != "Vacío" else "Disponible"
    
    # Renderizamos únicamente la tarjeta de información a lo ancho
    st.markdown(f"""
    <div class="info-card">
        <p class="info-name">{datos_cas["Nombre"]}</p>
        <p><strong>Área asignada:</strong> {datos_cas["Area"]}</p>
        <p><strong>Estado:</strong> {estado}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("Selecciona un casillero en la cuadrícula superior.")
