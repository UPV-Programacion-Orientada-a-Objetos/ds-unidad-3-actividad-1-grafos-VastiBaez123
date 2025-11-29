#ifndef GRAFO_DISPERSO_H
#define GRAFO_DISPERSO_H

#include "GrafoBase.h"
#include <vector>
#include <string>
#include <iostream>

class GrafoDisperso : public GrafoBase {
private:
    // CSR Format
    std::vector<int> values;      // Edge weights (assumed 1 for unweighted)
    std::vector<int> col_indices; // Column indices
    std::vector<int> row_ptr;     // Row pointers
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
    
    // Helper to get neighbors for Cython/Visualization if needed
    std::vector<int> getVecinos(int nodo);
};

#endif
