import streamlit as st
import pandas as pd
import os

# --- NOMBRE DEL ARCHIVO DE BASE DE DATOS ---
ARCHIVO_DATOS = "datos_casilleros.csv"

# 1. CONFIGURACIÓN DE LA PÁGINA Y TEMA OSCURO 
st.set_page_config(
    page_title="Casilleros Metro Emancipación",
    page_icon="🛒",
    layout="wide" 
)

# CSS para Modo Oscuro y Colores Metro
st.markdown("""
    <style>
    
    /* Tarjeta de información */
    .info-card {
        background-color: var(--background-color);
        color: var(--text-color);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #E2001A;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .info-name {
        color: #E2001A;
        font-size: 1.4rem;
        font-weight: bold;
    }
    
    /* Título */
    .metro-title {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-weight: 900;
        margin-bottom: 20px;
        border: 2px solid #E2001A;
    }
    
    /* Tema oscuro */
    [data-theme="dark"] .metro-title {
        background-color: #1E1E1E;
        color: #FFD200;
    }
    
    [data-theme="dark"] .info-card {
        background-color: #1E1E1E;
        color: white;
    }
    
    /* Tema claro */
    [data-theme="light"] .metro-title {
        background-color: #FFF8E1;
        color: #C62828;
    }
    
    [data-theme="light"] .info-card {
        background-color: white;
        color: #222;
        border: 1px solid #DDD;
    }
    
    /* Botones */
    div.stButton > button {
        width: 100%;
        height: 65px;
        border-radius: 10px;
        font-weight: bold;
    }
    
    </style>
""", unsafe_allow_html=True)

# 2. CARGA O CREACIÓN DE LA BASE DE DATOS PERMANENTE
if 'df_colaboradores' not in st.session_state:
    # Si el archivo ya existe en tu computadora, lo lee y carga los datos
    if os.path.exists(ARCHIVO_DATOS):
        # Leer CSV con punto y coma
        st.session_state.df_colaboradores = pd.read_csv(
            ARCHIVO_DATOS,
            encoding='utf-8-sig'
        )

        # Limpiar nombres de columnas
        st.session_state.df_colaboradores.columns = (
            st.session_state.df_colaboradores.columns
            .str.strip()
        )
        
    else:
        # Crear casilleros vacíos la primera vez
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

        # Guardar CSV inicial
        st.session_state.df_colaboradores.to_csv(
            ARCHIVO_DATOS,
            sep=';',
            index=False,
            encoding='utf-8-sig'
        )

if 'seleccion' not in st.session_state:
    st.session_state.seleccion = None

# --- LISTA DE ÁREAS METRO EMANCIPACIÓN ---
lista_areas = [
    "Abarrotes", "Bazar", "Electro", "Frutas y verduras", 
    "Embutidos", "Carnes", "Pollo brasa", "Confiteria", 
    "Cajas", "Promociones", "Panaderia", "Sin asignar"
]

# --- PANEL DE ADMINISTRACIÓN (BARRA LATERAL) ---
with st.sidebar:
    st.markdown('<h2 style="color:#FFD200;">⚙️ Administrar Casilleros</h2>', unsafe_allow_html=True)
    st.write("Agrega, edita o elimina la información de un colaborador aquí:")
    
    mod_edit = st.selectbox("Módulo:", options=list(range(1, 9)))
    cas_edit = st.selectbox("Casillero:", options=list(range(1, 13)))
    
    nuevo_nombre = st.text_input("Nombre del Colaborador:")
    nueva_area = st.selectbox("Área:", lista_areas)
    
    # Creamos dos columnas para alinear los botones
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("Guardar", use_container_width=True):
            # 1. Actualiza el dato en la memoria
            idx = st.session_state.df_colaboradores[
                (st.session_state.df_colaboradores['Modulo'] == mod_edit) & 
                (st.session_state.df_colaboradores['Casillero'] == cas_edit)
            ].index
            
            st.session_state.df_colaboradores.loc[idx, 'Nombre'] = nuevo_nombre
            st.session_state.df_colaboradores.loc[idx, 'Area'] = nueva_area
            
            # 2. Guarda en el CSV físico
            st.session_state.df_colaboradores.to_csv(ARCHIVO_DATOS, index=False)
            st.success(f"¡Actualizado!")

    with col_btn2:
        if st.button("Eliminar", use_container_width=True):
            # 1. Devuelve el casillero a su estado inicial
            idx = st.session_state.df_colaboradores[
                (st.session_state.df_colaboradores['Modulo'] == mod_edit) & 
                (st.session_state.df_colaboradores['Casillero'] == cas_edit)
            ].index
            
            st.session_state.df_colaboradores.loc[idx, 'Nombre'] = "Vacío"
            st.session_state.df_colaboradores.loc[idx, 'Area'] = "Sin asignar"
            
            # 2. Guarda en el CSV físico
            st.session_state.df_colaboradores.to_csv(ARCHIVO_DATOS, index=False)
            st.warning(f"¡Vaciado!")

# --- INTERFAZ PRINCIPAL ---
st.markdown('<h1 class="metro-title">Tienda Metro Emancipación</h1>', unsafe_allow_html=True)
st.write("### Gestión de Casilleros de Hombre:")

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
                
                label = f"{num_casillero}" + (" 👤" if ocupado else "")
                
                with cols[col_idx]:
                    if st.button(label, key=f"btn_m{num_modulo}_c{num_casillero}", use_container_width=True):
                        st.session_state.seleccion = {"modulo": num_modulo, "casillero": num_casillero}
                
st.divider()

# --- MOSTRAR LA INFORMACIÓN DEL CASILLERO SELECCIONADO ---
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
    
    st.markdown(f"""
    <div class="info-card">
        <p class="info-name">{datos_cas["Nombre"]}</p>
        <p><strong>Área asignada:</strong> {datos_cas["Area"]}</p>
        <p><strong>Estado:</strong> {estado}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("Selecciona un casillero en la cuadrícula superior.")
