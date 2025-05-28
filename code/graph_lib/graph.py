from collections import defaultdict, namedtuple
from random import random, choice
from collections import deque
from itertools import combinations


class Graph:
    def __init__(self):
        self._adjacency_list = defaultdict(set)
        self._vertecies = set()
        self._k_edges = 0

    def add_vertex(self, vertex):
        self._vertecies.add(vertex)

    def add_vertecies(self, verticies):
        for v in verticies:
            self.add_vertex(v)

    def k_vertecies(self):
        return len(self._vertecies)

    def k_edges(self):
        return self._k_edges

    def density(self):
        max_edges = self.k_vertecies() * (self.k_vertecies() - 1) // 2
        return self._k_edges / max_edges

    def verticies(self):
        return self._vertecies

    def add_edge(self, a, b):
        self._adjacency_list[a].add(b)
        self._adjacency_list[b].add(a)
        self.add_vertex(a)
        self.add_vertex(b)
        self._k_edges += 1

    def remove_edge(self,a,b):
        if a in self._vertecies and b in self._vertecies and b in self._adjacency_list[a]:
            self._adjacency_list[a].remove(b)
            self._adjacency_list[b].remove(a)
            self._k_edges -= 1

    def has_edge(self, a, b):
        return b in self._adjacency_list[a]

    def add_edges(self, edges):
        for (a, b) in edges:
            self.add_edge(a, b)

    def neib(self, v):
        return self._adjacency_list[v]

    def dfs(self, start=1):
        if len(self._vertecies) > 0:
            visited = {start}
            stack = [start]
            while stack:
                a = stack.pop()
                yield a
                for b in self._adjacency_list[a]:
                    if b not in visited:
                        visited.add(b)
                        stack.append(b)

    def bfs(self, start=1):
        if len(self._vertecies) > 0:
            visited = {start}
            queue = deque([start])
            while queue:
                a = queue.popleft()
                yield a
                for b in self._adjacency_list[a]:
                    if b not in visited:
                        visited.add(b)
                        queue.append(b)

    def bfs_edges(self, start=1):
        if len(self._vertecies) > 0:
            visited = {start}
            queue = deque([start])
            while queue:
                a = queue.popleft()
                for b in self._adjacency_list[a]:
                    if b not in visited:
                        yield (a, b)
                        visited.add(b)
                        queue.append(b)

    def dfs_edges(self, start=1):
        visited = set()

        def dfs(u, parent=None):
            visited.add(u)
            if parent is not None:
                yield (parent, u)
            for v in self._adjacency_list[u]:
                if v not in visited:
                    yield from dfs(v, u)

        if len(self._vertecies) > 0:
            yield from dfs(start)

    def is_connected(self):
        verticies = list(self.dfs(start=choice(tuple(self._vertecies))))
        return len(verticies) == len(self._vertecies)

    def deg(self, vertex):
        if vertex not in self._vertecies:
            raise Exception()
        return len(self._adjacency_list[vertex])

    def deg_list(self):
        return [self.deg(v) for v in self._vertecies]

    def diameter(self):
        diam_lst = [len(tuple(self.bfs(v))) - 1 for v in self._vertecies]
        return max(diam_lst)

    def dist(self, v, g):
        d = defaultdict(lambda: None)
        d[v] = 0
        for u1 in self.bfs(v):
            for u2 in self.neib(u1):
                if d[u2] is None:
                    d[u2] = d[u1] + 1
        return d[g]

    def mean_dist(self):
        dists = filter(lambda x: x is not None, map(
            lambda e: self.dist(*e), combinations(self._vertecies, 2)))
        return 2*sum(dists) / (self.k_vertecies() * (self.k_vertecies()-1))

    def k_triangles(self):
        triplets = set()
        k = 0
        for v in self._vertecies:
            if self.deg(v) >= 2:
                for v1 in self.neib(v):
                    for v2 in self.neib(v):
                        triplet = frozenset((v, v1, v2))
                        if self.has_edge(v1, v2) and triplet not in triplets:
                            k += 1
                            triplets.add(triplet)
        return k

    def k_forks(self):
        k = 0
        for v in self._vertecies:
            k += self.k_local_forks(v)
        return k

    def cluster_k(self):
        if self.k_forks() == 0:
            return 0
        return 3 * self.k_triangles() / self.k_forks()

    def k_local_triangles(self, v):
        k = 0
        if self.deg(v) >= 2:
            for v1 in self.neib(v):
                for v2 in self.neib(v):
                    if v1 < v2 and self.has_edge(v1, v2):
                        k += 1
        return k

    def k_local_forks(self, v):
        k = 0
        if self.deg(v) >= 2:
            for v1 in self.neib(v):
                for v2 in self.neib(v):
                    if v1 < v2 and not self.has_edge(v1, v2):
                        k += 1
        return k

    def local_cluster_k(self, v):
        if self.k_local_forks(v) > 0:
            return self.k_local_triangles(v) / self.k_local_forks(v)
        return 0

    def mean_cluster_k(self):
        return sum(self.local_cluster_k(v) for v in self._vertecies) / self.k_vertecies()

    def deg_distribution(self):
        result = []
        t = namedtuple("DegDistrNode", ("k", "p"))
        for d in set(self.deg_list()):
            k_d = len([1 for v in self.verticies() if self.deg(v) == d])
            result.append(t(d, k_d/self.k_vertecies()))
        return result

    def closeness(self, v):
        d = [self.dist(v, u)
             for u in self.verticies() if self.dist(v, u) is not None]
        if sum(d) == 0:
            return 0
        return (self.k_vertecies() - 1) / sum(d)

    def connected_components(self):
        visited = set()
        components = []
        for v in self.verticies():
            if v not in visited:
                component = []
                for u in self.bfs(v):
                    visited.add(u)
                    component.append(u)
                components.append(component)
        return components

    def find_bridges(self):
        time = 0
        enter = {}
        ret = {}
        visited = set()
        bridges = []

        def dfs(v, parent):
            nonlocal time
            time += 1
            enter[v] = time
            ret[v] = time
            visited.add(v)
            for u in self.neib(v):
                if u == parent:
                    continue
                if u in visited:
                    ret[v] = min(ret[v], enter[u])
                else:
                    dfs(u, v)
                    ret[v] = min(ret[v], ret[u])
                    if ret[u] > enter[v]:
                        bridges.append((u, v))
        for v in self.verticies():
            if v not in visited:
                dfs(v, None)
        return bridges

    def __str__(self):
        v = f"verticies-{self._vertecies}"
        a = f"list--{self._adjacency_list}"
        return f"{v}\n{a}"
