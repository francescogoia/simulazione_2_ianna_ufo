import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._idMap = {}
        self._grafo = nx.Graph()
        self._years = DAO.getAllYears()
        self._shapes = DAO.getAllShapes()

    def _crea_grafo(self, forma, anno):
        self._grafo.clear()
        self._nodes = DAO.getAllNodes(forma, anno)
        self._grafo.add_nodes_from(self._nodes)
        edges = DAO.getAllEdges(forma, anno)
        for e in edges:
            self._grafo.add_edge(e[0], e[1], weight=e[2])

    def get_dettagli_grafo(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_top_citta_adiacenti(self):
        result = []
        for n in self._nodes:
            vicini = self._grafo.neighbors(n)
            totP = 0
            for v in vicini:
                totP += self._grafo[n][v]["weight"]
            result.append((n, totP))
        result.sort(key=lambda x: x[1], reverse=True)
        return result[:5]



    def _handle_path(self, partenza, max_distanza, min_num_citta):
        self._bestPath = []
        self._bestMaxDistanza = 0
        self._bestMinCitta = 0
        self._ricorsione(partenza, [], max_distanza, min_num_citta)
        return self._bestPath, self._bestMaxDistanza, self._bestMinCitta

    def _ricorsione(self, nodo, parziale, max_distanza, min_num_citta):
        distanza_parziale, n_citta_parziale = self._get_info_parziale(parziale)
        if n_citta_parziale >= min_num_citta and distanza_parziale <= max_distanza:         # se parziale rispetta i vincoli
            if n_citta_parziale > self._bestMinCitta and distanza_parziale > self._bestMaxDistanza:     # se parziale migliora la miglio soluzione attuale
                self._bestMinCitta = n_citta_parziale
                self._bestMaxDistanza = distanza_parziale
                self._bestPath = copy.deepcopy(parziale)
        vicini = self._grafo.neighbors(nodo)
        vicini_ordinati = []
        for v in vicini:
            peso_arco = self._grafo[nodo][v]["weight"]
            vicini_ordinati.append((nodo, v, peso_arco))
        vicini_ordinati.sort(key=lambda x: x[2])
        for v in vicini_ordinati:
            if self._filtroNodo(v[1], parziale):
                if len(parziale) > 0:
                    if v[2] > parziale[-1][2]:
                        parziale.append((v[0], v[1], v[2]))
                        self._ricorsione(v[1], parziale, max_distanza, min_num_citta)
                        parziale.pop()
                else:
                    parziale.append((v[0], v[1], v[2]))
                    self._ricorsione(v[1], parziale, max_distanza, min_num_citta)
                    parziale.pop()



    def _get_info_parziale(self, parziale):
        totP = 0
        set_citta = set()
        for a in parziale:
            totP += a[2]
            set_citta.add(a[0])
            set_citta.add(a[1])
        return totP, len(set_citta)

    def _filtroNodo(self, v, parziale):
        for a in parziale:
            if a[0] == v or a[1] == v:
                return False
        return True



