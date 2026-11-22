"""02-3. SKOS로 용어 체계 만들기 — 대표어·동의어·상하위어"""
from rdflib import Graph

TTL = """
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix ex:   <http://example.org/terms#> .

ex:Battery skos:prefLabel "2차전지"@ko ; skos:altLabel "배터리"@ko , "축전지"@ko .
ex:Cathode skos:prefLabel "양극재"@ko ; skos:altLabel "양극 소재"@ko ; skos:broader ex:BatteryMaterial .
ex:Anode   skos:prefLabel "음극재"@ko ; skos:broader ex:BatteryMaterial .
ex:BatteryMaterial skos:prefLabel "2차전지 소재"@ko ; skos:related ex:Battery .
"""
g = Graph().parse(data=TTL, format="turtle")


def normalize(word: str) -> str:
    """동의어를 대표어로 바꾸기 (검색어 정규화)"""
    q = """
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    SELECT ?pref WHERE {
      ?c skos:prefLabel ?pref .
      { ?c skos:prefLabel ?w } UNION { ?c skos:altLabel ?w }
      FILTER(STR(?w) = ?word)
    }"""
    rows = list(g.query(q, initBindings={"word": __import__("rdflib").Literal(word)}))
    return str(rows[0].pref) if rows else word


for w in ["배터리", "축전지", "양극 소재", "음극재", "반도체"]:
    print(f"{w:6} → {normalize(w)}")

q_narrow = """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?child WHERE { ?c skos:broader ?p . ?p skos:prefLabel "2차전지 소재"@ko . ?c skos:prefLabel ?child }
"""
print("\n'2차전지 소재'의 하위어:", sorted(str(r.child) for r in g.query(q_narrow)))
