import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._nodi = None
        self._idMap = {}
        self._idMapPop = {}
        for i in DAO.getAllPopolarita():
            self._idMapPop[i[0]] = i[1]

    def get_all_generi(self):
        return DAO.getAllGenres()

    def buildGrafo(self,genre):
        self._grafo.clear()
        self._nodi = DAO.getAllNodes(genre)
        for n in self._nodi:
            self._idMap[n.ArtistId] = n
        self._grafo.add_nodes_from(self._nodi)
        # self.addEdgesPesati()
        self.addEdgesPesati(genre)


    def addEdgesPesati(self,g):
        #self._grafo.clear()
        edges = DAO.getAllEdges(g)
        for e in edges:
            pop1 = self._idMapPop.get(e[0], 0)
            pop2 = self._idMapPop.get(e[1], 0)
            if pop1 > pop2:
                self._grafo.add_edge(self._idMap[e[0]], self._idMap[e[1]], weight= pop1+pop2)
            elif pop1 < pop2:
                self._grafo.add_edge(self._idMap[e[1]], self._idMap[e[0]], weight=pop1 + pop2)
            else:
                self._grafo.add_edge(self._idMap[e[0]], self._idMap[e[1]], weight=pop1 + pop2)
                self._grafo.add_edge(self._idMap[e[1]], self._idMap[e[0]], weight=pop1 + pop2)

    def get_numnodi(self):
        return len(self._grafo.nodes())
    def get_numarchi(self):
        return len(self._grafo.edges())

    def get_artista_piu_influente(self):
        if len(self._grafo.nodes()) == 0:
            return None, 0
        best = None
        best_infl = None
        for n in self._grafo.nodes():
            # influenza = peso archi USCENTI − peso archi ENTRANTI
            usciti = self._grafo.out_degree(n, weight="weight")
            entrati = self._grafo.in_degree(n, weight="weight")
            infl = usciti - entrati
            if best_infl is None or infl > best_infl:
                best_infl = infl
                best = n
        return best, best_infl

    def get_top5_archi(self):
        archi = []
        for u, v, data in self._grafo.edges(data=True):
            archi.append((u, v, data["weight"]))
        archi.sort(key=lambda x: x[2], reverse=True)  # ordine decrescente per peso
        return archi[:5]
