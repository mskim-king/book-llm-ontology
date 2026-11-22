"""02-4. SHACL로 데이터 검증하기"""
from pyshacl import validate
from rdflib import Graph

SHAPES = """
@prefix sh:  <http://www.w3.org/ns/shacl#> .
@prefix ex:  <http://example.org/onto#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:CompanyShape a sh:NodeShape ;
    sh:targetClass ex:Company ;
    sh:property [ sh:path rdfs:label ; sh:minCount 1 ; sh:message "회사에는 이름(label)이 있어야 합니다" ] ;
    sh:property [ sh:path ex:foundedYear ; sh:maxCount 1 ; sh:datatype xsd:integer ;
                  sh:minInclusive 1800 ; sh:message "설립연도는 1800 이상의 정수 하나여야 합니다" ] ;
    sh:property [ sh:path ex:suppliesTo ; sh:class ex:Company ; sh:message "공급 대상은 회사여야 합니다" ] .
"""

BAD_DATA = """
@prefix ex:  <http://example.org/onto#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
ex:Company a <http://www.w3.org/2002/07/owl#Class> .
ex:Seoul a ex:City ; rdfs:label "서울"@ko .
ex:EElec a ex:Company ;                     # 이름 없음
    ex:foundedYear 1750 ;                   # 범위 위반
    ex:suppliesTo ex:Seoul .                # 회사가 아닌 대상
"""

for title, data in [("오류가 있는 데이터", BAD_DATA)]:
    conforms, _, text = validate(Graph().parse(data=data, format="turtle"),
                                 shacl_graph=Graph().parse(data=SHAPES, format="turtle"))
    print(f"[{title}] 규칙 준수: {conforms}")
    msgs = sorted({line.split("Message:")[1].strip() for line in text.splitlines() if "Message:" in line})
    for m in msgs:
        print("  -", m)

from common import load
conforms, _, _ = validate(load(), shacl_graph=Graph().parse(data=SHAPES, format="turtle"))
print(f"\n[책 예제 데이터 company.ttl] 규칙 준수: {conforms}")
