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
            self._idMap[n.GenreId] = n
        self._grafo.add_nodes_from(DAO.getAllNodes(genre))
        # self.addEdgesPesati()
        self.addEdgesPesati()


    def addEdgesPesati(self):
        self._grafo.clear()
        edges = DAO.getAllEdges()
        for e in edges:
            pop1 = self._idMapPop[self._idMap[e[0]]]
            pop2 = self._idMapPop[self._idMap[e[1]]]
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
