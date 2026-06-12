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
    "Cajas", "Promociones", "Panaderia", "Almacén", "Sin asignar"
]

# --- PANEL DE ADMINISTRACIÓN (BARRA LATERAL) ---
with st.sidebar:
    st.markdown('<h2 style="color:#FFD200;">⚙️ Administrar Casilleros</h2>', unsafe_allow_html=True)
    st.write("Agrega o edita la información de un colaborador aquí:")
    
    # Reemplazamos los selectbox por sliders (deslizadores táctiles)
    mod_edit = st.selectbox("Módulo:", options=list(range(1, 9)))
    cas_edit = st.selectbox("Casillero:", options=list(range(1, 13)))
    
    nuevo_nombre = st.text_input("Nombre del Colaborador:")
    # Reemplazamos el selectbox por botones de selección
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
            
    with st.sidebar:
    # ... (tu código previo de selección de módulo/casillero) ...
    
        st.divider()
        st.markdown("### 📥 Descargar Reporte General")
        
        # 1. Obtenemos el DataFrame completo sin filtrar
        datos_completos = st.session_state.df_colaboradores
        
        # 2. Convertimos todo el DataFrame a CSV
        csv_completo = datos_completos.to_csv(index=False).encode('utf-8-sig')
        
        # 3. Botón de descarga para todos los módulos
        st.download_button(
            label="Descargar",
            data=csv_completo,
            file_name="Reporte_General_Casilleros.csv",
            mime="text/csv",
            use_container_width=True
        )

# --- INTERFAZ PRINCIPAL ---
st.markdown('<h1 class="metro-title">Tienda Metro Emancipación</h1>', unsafe_allow_html=True)
st.write("### Gestión de Casilleros de Hombre:")

# 7. Generación de las Pestañas y los Botones Inteligentes
modulos_nombres = [f"Módulo {i}" for i in range(1, 9)]
pestanas = st.tabs(modulos_nombres)

for i, tab in enumerate(pestanas):
    num_modulo = i + 1
    with tab:
        filas = 4
        columnas = 3
        
        for fila in range(filas):
            cols = st.columns(columnas)
            for col_idx in range(columnas):
                num_casillero = (fila * columnas) + col_idx + 1
                
                # Obtenemos los datos desde Pandas
                datos_cas = st.session_state.df_colaboradores[
                    (st.session_state.df_colaboradores['Modulo'] == num_modulo) & 
                    (st.session_state.df_colaboradores['Casillero'] == num_casillero)
                ].iloc[0]
                
                nombre = datos_cas['Nombre']
                ocupado = nombre != "Vacío"
                
                with cols[col_idx]:
                    # Verificamos si es el seleccionado
                    es_el_seleccionado = False
                    if 'seleccion' in st.session_state and st.session_state.seleccion:
                        if st.session_state.seleccion['modulo'] == num_modulo and \
                           st.session_state.seleccion['casillero'] == num_casillero:
                            es_el_seleccionado = True

                    # Etiqueta dinámica (salto de línea si está seleccionado)
                    if es_el_seleccionado and ocupado:
                        label = f"{num_casillero}\n{nombre}"
                    else:
                        label = f"{num_casillero}" + (" 👤" if ocupado else "")
                    
                    # Creación del botón
                    if st.button(label, key=f"btn_{num_modulo}_{num_casillero}", use_container_width=True):
                        # Guardamos en memoria qué botón se tocó y recargamos
                        st.session_state.seleccion = {
                            "modulo": num_modulo,
                            "casillero": num_casillero
                        }
# 8. Mostrar la Información del Casillero Seleccionado (Tarjeta Inferior)                       
st.divider()

if 'seleccion' in st.session_state and st.session_state.seleccion:
    mod = st.session_state.seleccion["modulo"]
    cas = st.session_state.seleccion["casillero"]
    
    # Buscar datos de la base actual
    datos_cas = st.session_state.df_colaboradores[
        (st.session_state.df_colaboradores['Modulo'] == mod) & 
        (st.session_state.df_colaboradores['Casillero'] == cas)
    ].iloc[0]
    
    if datos_cas["Nombre"] != "Vacío":
        st.markdown(f"""
            <div class="info-card">
                <h3 class="info-name" style="margin: 0; padding-bottom: 10px;">👤 {datos_cas["Nombre"]}</h3>
                <p style="margin: 5px 0;"><b>Módulo:</b> {mod} | <b>Casillero:</b> {cas}</p>
                <p style="margin: 5px 0; color: #FFD200;"><b>Área asignada:</b> {datos_cas["Area"]}</p>
                <p style="margin: 5px 0; color: #4CAF50;"><b>Estado:</b> Ocupado</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info(f"El Casillero {cas} del Módulo {mod} se encuentra actualmente Vacío y disponible.")
else:
    st.info("Selecciona un casillero en la cuadrícula superior para ver los detalles.")
