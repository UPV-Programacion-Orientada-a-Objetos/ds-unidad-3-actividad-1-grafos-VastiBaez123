#include "GrafoDisperso.h"
#include <fstream>
#include <sstream>
#include <algorithm>
#include <queue>
#include <map>
#include <set>

GrafoDisperso::GrafoDisperso() : num_nodos(0), num_aristas(0) {}

GrafoDisperso::~GrafoDisperso() {}

void GrafoDisperso::cargarDatos(const std::string& archivo) {
    std::cout << "[C++ Core] Cargando dataset '" << archivo << "'..." << std::endl;
    std::ifstream infile(archivo);
    if (!infile.is_open()) {
        std::cerr << "Error al abrir el archivo: " << archivo << std::endl;
        return;
    }

  
    
    std::vector<std::vector<int>> adj;
    int max_node = -1;
    int u, v;
    std::string line;

    while (std::getline(infile, line)) {
        if (line.empty() || line[0] == '#') continue;
        std::stringstream ss(line);
        if (ss >> u >> v) {
            max_node = std::max(max_node, std::max(u, v));
            if (adj.size() <= (size_t)max_node) {
                adj.resize(max_node + 1);
            }

            adj[u].push_back(v);
            num_aristas++;
        }
    }
    infile.close();

    num_nodos = adj.size();

    row_ptr.resize(num_nodos + 1);
    values.clear();
    col_indices.clear();

    int current_idx = 0;
    for (int i = 0; i < num_nodos; ++i) {
        row_ptr[i] = current_idx;
        for (int neighbor : adj[i]) {
            col_indices.push_back(neighbor);
            values.push_back(1); // Default weight
            current_idx++;
        }
    }
    row_ptr[num_nodos] = current_idx;

    std::cout << "[C++ Core] Carga completa. Nodos: " << num_nodos << " | Aristas: " << num_aristas << std::endl;
    std::cout << "[C++ Core] Estructura CSR construida." << std::endl;
}

int GrafoDisperso::obtenerGrado(int nodo) {
    if (nodo < 0 || nodo >= num_nodos) return 0;
    return row_ptr[nodo + 1] - row_ptr[nodo];
}

std::vector<int> GrafoDisperso::getVecinos(int nodo) {
    std::vector<int> vecinos;
    if (nodo < 0 || nodo >= num_nodos) return vecinos;
    
    for (int i = row_ptr[nodo]; i < row_ptr[nodo + 1]; ++i) {
        vecinos.push_back(col_indices[i]);
    }
    return vecinos;
}

std::vector<int> GrafoDisperso::bfs(int nodoInicio, int profundidad) {
    std::cout << "[C++ Core] Ejecutando BFS nativo desde " << nodoInicio << " con profundidad " << profundidad << "..." << std::endl;
    std::vector<int> visitados;
    if (nodoInicio < 0 || nodoInicio >= num_nodos) return visitados;

    std::queue<std::pair<int, int>> q; // node, depth
    std::set<int> visited_set;

    q.push({nodoInicio, 0});
    visited_set.insert(nodoInicio);
    visitados.push_back(nodoInicio);

    while (!q.empty()) {
        int u = q.front().first;
        int d = q.front().second;
        q.pop();

        if (d >= profundidad) continue;

        for (int i = row_ptr[u]; i < row_ptr[u + 1]; ++i) {
            int v = col_indices[i];
            if (visited_set.find(v) == visited_set.end()) {
                visited_set.insert(v);
                visitados.push_back(v);
                q.push({v, d + 1});
            }
        }
    }
    
    std::cout << "[C++ Core] Nodos encontrados: " << visitados.size() << std::endl;
    return visitados;
}

int GrafoDisperso::obtenerNumNodos() {
    return num_nodos;
}

int GrafoDisperso::obtenerNumAristas() {
    return num_aristas;
}
