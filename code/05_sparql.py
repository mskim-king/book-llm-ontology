"""03-2. SPARQL 기초 — 조회, 필터, 집계, 여러 단계 관계 따라가기"""
from common import load

g = load()
PREFIX = "PREFIX ex: <http://example.org/onto#>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"

QUERIES = {
    "① 모든 회사와 설립연도 (오래된 순)": """
SELECT ?name ?year WHERE {
  ?c a ex:Company ; rdfs:label ?name ; ex:foundedYear ?year .
} ORDER BY ?year""",
    "② 2000년 이후 설립된 회사": """
SELECT ?name WHERE {
  ?c a ex:Company ; rdfs:label ?name ; ex:foundedYear ?y .
  FILTER(?y >= 2000)
}""",
    "③ 산업별 회사 수": """
SELECT ?industry (COUNT(?c) AS ?n) WHERE {
  ?c ex:inIndustry/rdfs:label ?industry .
} GROUP BY ?industry ORDER BY DESC(?n)""",
    "④ A전자의 공급망 (2단계까지 거슬러 올라가기)": """
SELECT ?supplier ?step WHERE {
  { ?s ex:suppliesTo ex:AElec . BIND(1 AS ?step) }
  UNION
  { ?s ex:suppliesTo/ex:suppliesTo ex:AElec . BIND(2 AS ?step) }
  ?s rdfs:label ?supplier .
} ORDER BY ?step""",
    "⑤ A전자의 경쟁사에도 납품하는 A전자 공급망 기업": """
SELECT DISTINCT ?name WHERE {
  ?s ex:suppliesTo+ ex:AElec .
  ex:AElec ex:competesWith ?rival .
  ?s ex:suppliesTo ?rival .
  ?s rdfs:label ?name .
}""",
}

for title, q in QUERIES.items():
    print(title)
    for row in g.query(PREFIX + q):
        print("   ", " | ".join(str(v) for v in row))
    print()
