import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import time
import os
import sys

# Ensure the compiled module is in the path if not installed globally
sys.path.append(os.getcwd())

try:
    import neuronet
except ImportError:
    st.error("No se pudo importar el módulo 'neuronet'. Asegúrate de haber compilado la extensión con 'python setup.py build_ext --inplace'.")
    st.stop()

st.set_page_config(page_title="NeuroNet", layout="wide")

st.title("NeuroNet: Análisis y Visualización de Redes Masivas")
st.markdown("### Sistema Híbrido C++ / Python (Cython)")

# Sidebar for controls
st.sidebar.header("Panel de Control")

# Initialize Session State for the Graph
if 'grafo' not in st.session_state:
    st.session_state.grafo = None
if 'graph_loaded' not in st.session_state:
    st.session_state.graph_loaded = False

# 1. Data Ingestion
st.sidebar.subheader("1. Ingesta de Datos")
uploaded_file = st.sidebar.file_uploader("Cargar Dataset (Formato SNAP)", type=["txt"])

# Use a default file if available for testing
default_file_path = "web-Google.txt"
load_button = st.sidebar.button("Cargar Grafo")

if load_button:
    file_path = None
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with open("temp_dataset.txt", "wb") as f:
            f.write(uploaded_file.getbuffer())
        file_path = "temp_dataset.txt"
    elif os.path.exists(default_file_path):
        file_path = default_file_path
    else:
        st.sidebar.error("Por favor carga un archivo o asegura que 'web-Google.txt' exista.")

    if file_path:
        st.session_state.grafo = neuronet.PyGrafoDisperso()
        start_time = time.time()
        with st.spinner('Cargando datos en el motor C++...'):
            st.session_state.grafo.cargar_datos(file_path)
        end_time = time.time()
        
        st.session_state.graph_loaded = True
        st.sidebar.success(f"Grafo cargado en {end_time - start_time:.4f}s")
        st.sidebar.info(f"Nodos: {st.session_state.grafo.obtener_num_nodos()}")
        st.sidebar.info(f"Aristas: {st.session_state.grafo.obtener_num_aristas()}")

if st.session_state.graph_loaded and st.session_state.grafo:
    # 2. Topological Analysis
    st.header("Análisis Topológico")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Consultar Nodo")
        node_id = st.number_input("ID del Nodo", min_value=0, value=0, step=1)
        if st.button("Obtener Grado"):
            grado = st.session_state.grafo.obtener_grado(node_id)
            st.metric(label=f"Grado del Nodo {node_id}", value=grado)

    # 3. Simulation / Traversal
    st.header("Simulación de Recorrido (BFS)")
    col_sim1, col_sim2 = st.columns([1, 3])
    
    with col_sim1:
        start_node = st.number_input("Nodo Inicio", min_value=0, value=0)
        depth = st.number_input("Profundidad Máxima", min_value=1, max_value=5, value=2)
        run_bfs = st.button("Ejecutar BFS")

    if run_bfs:
        start_time = time.time()
        visited_nodes = st.session_state.grafo.bfs(start_node, depth)
        end_time = time.time()
        
        st.success(f"BFS completado en {end_time - start_time:.6f}s. Nodos encontrados: {len(visited_nodes)}")
        
        # Visualization
        if len(visited_nodes) > 1000:
            st.warning("El subgrafo es demasiado grande para visualizar (>1000 nodos). Se muestran los primeros 100.")
            nodes_to_draw = visited_nodes[:100]
        else:
            nodes_to_draw = visited_nodes
            
        # Build NetworkX graph for visualization
        G_vis = nx.DiGraph()
        
        # We need to fetch edges for these nodes to draw them
        # This is a bit inefficient if we don't have a bulk edge getter, but fine for visualization
        for u in nodes_to_draw:
            vecinos = st.session_state.grafo.obtener_vecinos(u)
            for v in vecinos:
                if v in nodes_to_draw:
                    G_vis.add_edge(u, v)
        
        st.subheader("Visualización del Subgrafo")
        fig, ax = plt.subplots(figsize=(10, 8))
        try:
            pos = nx.spring_layout(G_vis, seed=42)
        except ImportError:
            st.warning("Scipy no detectado correctamente. Usando layout alternativo.")
            pos = nx.shell_layout(G_vis)
        
        # Draw nodes
        nx.draw_networkx_nodes(G_vis, pos, node_size=300, node_color='skyblue', alpha=0.9, ax=ax)
        # Draw edges
        nx.draw_networkx_edges(G_vis, pos, width=1.0, alpha=0.5, arrowstyle='->', arrowsize=10, ax=ax)
        # Draw labels
        nx.draw_networkx_labels(G_vis, pos, font_size=8, font_family="sans-serif", ax=ax)
        
        ax.set_title(f"Subgrafo BFS desde Nodo {start_node} (Profundidad {depth})")
        ax.axis('off')
        st.pyplot(fig)

else:
    st.info("Carga un dataset para comenzar.")

