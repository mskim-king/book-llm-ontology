"""06-2. 논리적 일관성 검사 — SPARQL로 모순·이상 데이터 찾기"""
from rdflib import Literal
from common import load, EX

g = load()
# 검사를 위해 일부러 잘못된 사실 세 가지를 추가 (실제 데이터에는 없음)
g.add((EX.DChem, EX.worksFor, EX.AElec))        # 회사가 회사에 '근무'
g.add((EX.BMat, EX.suppliesTo, EX.BMat))        # 자기 자신에게 공급
g.add((EX.CElec, EX.foundedYear, Literal(2015)))  # 설립연도가 두 개

PREFIX = "PREFIX ex: <http://example.org/onto#>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
CHECKS = {
    "사람과 회사로 동시에 쓰인 개체": """
SELECT DISTINCT ?name WHERE {
  ?x ex:worksFor ?any .               # 근무한다의 주어 → 사람이어야 함
  ?x a/rdfs:subClassOf* ex:Company .  # 그런데 회사이기도 함
  ?x rdfs:label ?name . }""",
    "자기 자신과의 관계": """
SELECT ?name WHERE { ?x ex:suppliesTo ?x . ?x rdfs:label ?name . }""",
    "값이 하나여야 하는데 여러 개": """
SELECT ?name (COUNT(?y) AS ?n) WHERE {
  ?x ex:foundedYear ?y ; rdfs:label ?name .
} GROUP BY ?name HAVING (COUNT(?y) > 1)""",
    "공급 관계의 순환 (A→…→A)": """
SELECT DISTINCT ?name WHERE {
  ?x ex:suppliesTo/ex:suppliesTo+ ?x . ?x rdfs:label ?name . }""",
}
for title, q in CHECKS.items():
    rows = [" ".join(str(v) for v in r) for r in g.query(PREFIX + q)]
    print(f"[{'❌' if rows else '✅'}] {title}: {', '.join(rows) if rows else '문제 없음'}")
