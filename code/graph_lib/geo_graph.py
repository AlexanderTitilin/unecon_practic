from .graph import Graph
from dataclasses import dataclass
from math import dist, sqrt


@dataclass(frozen=True)
class Node:
    x: float
    y: float

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, o):
        return self.x == o.x and self.y == o.y and self.y == o.y

    def __str__(self):
        return f"({self.x},{self.y})"

    def dist(self, other):
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y)**2)



class GeoGraph(Graph):
    def __init__(self):
        super().__init__()
