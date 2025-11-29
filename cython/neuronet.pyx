# distutils: language = c++


from libcpp.vector cimport vector
from libcpp.string cimport string
from neuronet_lib cimport GrafoDisperso

cdef class PyGrafoDisperso:
    cdef GrafoDisperso* c_grafo

    def __cinit__(self):
        self.c_grafo = new GrafoDisperso()

    def __dealloc__(self):
        del self.c_grafo

    def cargar_datos(self, archivo: str):
        cdef string c_archivo = archivo.encode('utf-8')
        self.c_grafo.cargarDatos(c_archivo)

    def obtener_grado(self, nodo: int):
        return self.c_grafo.obtenerGrado(nodo)

    def bfs(self, nodo_inicio: int, profundidad: int):
        return self.c_grafo.bfs(nodo_inicio, profundidad)

    def obtener_num_nodos(self):
        return self.c_grafo.obtenerNumNodos()

    def obtener_num_aristas(self):
        return self.c_grafo.obtenerNumAristas()
    
    def obtener_vecinos(self, nodo: int):
        return self.c_grafo.getVecinos(nodo)
