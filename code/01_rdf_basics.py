"""02-1. RDF와 트리플 — 트리플 만들기, Turtle로 저장하기"""
from rdflib import Graph, Literal, Namespace, RDF, RDFS

EX = Namespace("http://example.org/onto#")
g = Graph()
g.bind("ex", EX)

# 트리플 3개: (주어, 관계, 목적어)
g.add((EX.AElec, RDF.type, EX.Company))
g.add((EX.AElec, RDFS.label, Literal("A전자", lang="ko")))
g.add((EX.BMat, EX.suppliesTo, EX.AElec))

print(f"트리플 수: {len(g)}\n")
print(g.serialize(format="turtle"))

# 특정 패턴 찾기: 무엇이 A전자에 공급하는가?
for s, p, o in g.triples((None, EX.suppliesTo, EX.AElec)):
    print("공급사:", s.split("#")[-1])
