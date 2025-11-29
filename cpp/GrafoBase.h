#ifndef GRAFO_BASE_H
#define GRAFO_BASE_H

#include <vector>
#include <string>

class GrafoBase {
public:
    virtual ~GrafoBase() {}
    virtual void cargarDatos(const std::string& archivo) = 0;
    virtual int obtenerGrado(int nodo) = 0;
    virtual std::vector<int> bfs(int nodoInicio, int profundidad) = 0;
    virtual int obtenerNumNodos() = 0;
    virtual int obtenerNumAristas() = 0;
};

#endif
