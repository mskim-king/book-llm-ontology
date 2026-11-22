"""05-2. GraphRAG 이해와 구현 — 질문 → 개체 찾기 → 그래프 탐색 → 근거 구성 → 프롬프트

LLM 호출 직전까지(근거 구성과 프롬프트 생성)를 실행합니다.
"""
from rdflib import OWL, RDF, RDFS
from common import load, label

g = load()
QUESTION = "A전자의 공급망에 문제가 생기면 영향을 받을 수 있는 다른 회사는?"

# 1) 개체 찾기: 질문에 들어 있는 이름(label)을 지식그래프 노드와 연결
#    - 클래스(회사·산업 등)는 제외하고 실제 개체만
#    - 더 긴 이름에 포함되는 짧은 이름은 제외 ("A전자" 안의 "전자")
classes = set(g.subjects(RDF.type, OWL.Class))
hits = {str(o): s for s, _, o in g.triples((None, RDFS.label, None))
        if str(o) in QUESTION and s not in classes}
entities = [node for name, node in hits.items()
            if not any(name != other and name in other for other in hits)]
print("1) 찾은 개체:", [label(g, e) for e in entities])

# 2) 그래프 탐색: 개체에서 2단계까지 이웃 사실 모으기
#    온톨로지에 정의된 '관계'(owl:ObjectProperty)만 따라감 → 라벨·유형·스키마 정의는 제외
RELATIONS = set(g.subjects(RDF.type, OWL.ObjectProperty))
facts, frontier = set(), set(entities)
for hop in range(2):
    nxt = set()
    for node in frontier:
        for s, p, o in list(g.triples((node, None, None))) + list(g.triples((None, None, node))):
            if p not in RELATIONS:
                continue
            facts.add((s, p, o))
            nxt.update({s, o})
    frontier = nxt - frontier
print(f"2) 모은 사실: {len(facts)}개")

# 3) 근거 구성: 사람이 읽을 수 있는 문장으로 바꾸고 번호를 붙임
lines = sorted(f"{label(g, s)} -{label(g, p)}→ {label(g, o)}" for s, p, o in facts)
context = "\n".join(f"[{i}] {line}" for i, line in enumerate(lines, 1))
print("3) 근거:\n" + context)

# 4) 프롬프트: 근거만 사용하고 번호로 인용하게 함
PROMPT = f"""아래 [근거]만 사용해 질문에 답해 줘. 문장마다 근거 번호를 [1]처럼 붙이고,
근거로 답할 수 없는 부분은 "근거 없음"이라고 써 줘.

[근거]
{context}

[질문]
{QUESTION}"""
print("\n4) LLM에 보낼 프롬프트:\n" + PROMPT)
