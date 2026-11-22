"""08-1. 금융 온톨로지 — 공급망에서 '핵심 노드' 찾기 (가상 데이터)

한 회사에 문제가 생기면 공급 관계를 따라 영향을 받을 수 있는 하류 회사를 셉니다.
"""
from common import load

g = load()
Q = """
PREFIX ex: <http://example.org/onto#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?name ?dname WHERE {
  ?s a ex:Company ; rdfs:label ?name .
  OPTIONAL { ?s ex:suppliesTo+ ?d . ?d rdfs:label ?dname . }
}"""
downstream: dict[str, set[str]] = {}
for r in g.query(Q):
    downstream.setdefault(str(r.name), set())
    if r.dname is not None:
        downstream[str(r.name)].add(str(r.dname))

print("회사 | 영향받는 하류 회사 수 | 목록")
for name, ds in sorted(downstream.items(), key=lambda x: (-len(x[1]), x[0])):
    print(f"{name} | {len(ds)} | {', '.join(sorted(ds)) or '-'}")
