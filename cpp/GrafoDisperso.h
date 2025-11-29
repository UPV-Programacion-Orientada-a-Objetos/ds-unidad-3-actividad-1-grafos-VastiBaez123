#ifndef GRAFO_DISPERSO_H
#define GRAFO_DISPERSO_H

#include "GrafoBase.h"
#include <vector>
#include <string>
#include <iostream>

class GrafoDisperso : public GrafoBase {
private:
    std::vector<int> values;     
    std::vector<int> col_indices; 
    std::vector<int> row_ptr;     
    int num_nodos;
    int num_aristas;

public:
    GrafoDisperso();
    ~GrafoDisperso();

    void cargarDatos(const std::string& archivo) override;
    int obtenerGrado(int nodo) override;
    std::vector<int> bfs(int nodoInicio, int profundidad) override;
    int obtenerNumNodos() override;
    int obtenerNumAristas() override;
    
    std::vector<int> getVecinos(int nodo);
};

#endif
