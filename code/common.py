"""예제 공통: 데이터 불러오기와 출력 도우미"""
from pathlib import Path
from rdflib import Graph, Namespace

EX = Namespace("http://example.org/onto#")
DATA = Path(__file__).parent / "data"


def load(name: str = "company.ttl") -> Graph:
    g = Graph()
    g.parse(DATA / name, format="turtle")
    g.bind("ex", EX)
    return g


def label(g: Graph, node) -> str:
    from rdflib import RDFS
    v = g.value(node, RDFS.label)
    return str(v) if v else str(node).split("#")[-1]
