"""05-1. 스키마 기반 정보 추출 — 온톨로지에서 추출용 프롬프트를 자동으로 만들기"""
from rdflib import OWL, RDF, RDFS
from common import load, label

g = load()
classes = sorted(label(g, c) for c in g.subjects(RDF.type, OWL.Class))
relations = []
for p in g.subjects(RDF.type, OWL.ObjectProperty):
    relations.append(f"- {label(g, p)}: {label(g, g.value(p, RDFS.domain))} → {label(g, g.value(p, RDFS.range))}")

PROMPT = f"""다음 문서에서 사실을 추출해 JSON으로만 답해 줘.

[허용하는 개체 유형]
{", ".join(classes)}

[허용하는 관계] (주어 유형 → 목적어 유형)
{chr(10).join(sorted(relations))}

[규칙]
1. 위 목록에 없는 관계는 만들지 마.
2. 각 사실마다 근거가 된 문장을 원문 그대로 evidence 에 넣어.
3. 문서에 없는 내용은 추측하지 마.

[출력 형식]
{{"triples": [{{"subject": "", "relation": "", "object": "", "evidence": ""}}]}}

[문서]
{{문서}}"""
print(PROMPT)
