from libcpp.vector cimport vector
from libcpp.string cimport string

cdef extern from "../cpp/GrafoBase.h":
    cdef cppclass GrafoBase:
        pass

cdef extern from "../cpp/GrafoDisperso.h":
    cdef cppclass GrafoDisperso(GrafoBase):
        GrafoDisperso() except +
        void cargarDatos(string archivo)
        int obtenerGrado(int nodo)
        vector[int] bfs(int nodoInicio, int profundidad)
        int obtenerNumNodos()
        int obtenerNumAristas()
        vector[int] getVecinos(int nodo)
