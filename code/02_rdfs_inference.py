"""02-2. RDFS와 OWL — 클래스 계층에 따른 추론 (SPARQL 속성 경로 이용)"""
from common import load, label, EX

g = load()

# 직접 적힌 유형만 보면 김민준은 '직원'
q_direct = """
SELECT ?type WHERE { ex:Minjun a ?type }
"""
print("직접 적힌 유형:", [label(g, r.type) for r in g.query(q_direct)])

# rdfs:subClassOf* 로 상위 클래스까지 따라가면 '사람'이기도 함
q_infer = """
SELECT DISTINCT ?type WHERE { ex:Minjun a/rdfs:subClassOf* ?type }
"""
print("추론 포함 유형:", sorted(label(g, r.type) for r in g.query(q_infer)))

# 대칭 속성(owl:SymmetricProperty): A전자-경쟁-C전자 → C전자-경쟁-A전자
q_sym = """
SELECT ?x ?y WHERE {
  { ?x ex:competesWith ?y } UNION { ?y ex:competesWith ?x }
}
"""
pairs = sorted((label(g, r.x), label(g, r.y)) for r in g.query(q_sym))
print("경쟁 관계(대칭 반영):", pairs)
