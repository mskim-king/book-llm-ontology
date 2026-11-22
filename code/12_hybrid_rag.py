"""06-1. RAG 한눈에 보기 — 벡터식 문서 검색 vs 그래프 검색 vs 하이브리드

실제 서비스에서는 임베딩 모델로 문서를 벡터로 바꿔 검색합니다.
이 예제는 외부 서비스 없이 실행되도록 '글자 2개 묶음(bigram) 겹침'으로 유사도를 흉내 냅니다.
"""
from pathlib import Path
from rdflib import OWL, RDF, RDFS
from common import load, label

g = load()
DOCS = [line.split(" | ", 1) for line in (Path(__file__).parent / "data/docs.txt").read_text().splitlines()
        if line and not line.startswith("#")]


def bigrams(text: str) -> set[str]:
    t = text.replace(" ", "")
    return {t[i:i + 2] for i in range(len(t) - 1)}


def doc_search(q: str, k: int = 2) -> list[str]:
    """벡터 검색 흉내: 질문과 가장 비슷한 문서 k개"""
    qb = bigrams(q)
    scored = sorted(DOCS, key=lambda d: len(qb & bigrams(d[0] + d[1])) / (len(qb) or 1), reverse=True)
    return [f"(문서) {title}: {body}" for title, body in scored[:k]]


def graph_search(q: str, hops: int = 2) -> list[str]:
    """그래프 검색: 질문 속 개체에서 관계를 따라 사실 수집 (08_graphrag.py와 같은 방식)"""
    classes = set(g.subjects(RDF.type, OWL.Class))
    rels = set(g.subjects(RDF.type, OWL.ObjectProperty))
    hits = {str(o): s for s, _, o in g.triples((None, RDFS.label, None)) if str(o) in q and s not in classes}
    frontier = {n for name, n in hits.items() if not any(name != o and name in o for o in hits)}
    facts = set()
    for _ in range(hops):
        nxt = set()
        for node in frontier:
            for s, p, o in list(g.triples((node, None, None))) + list(g.triples((None, None, node))):
                if p in rels:
                    facts.add((s, p, o)); nxt |= {s, o}
        frontier = nxt
    return sorted(f"(그래프) {label(g, s)} -{label(g, p)}→ {label(g, o)}" for s, p, o in facts)


def route(q: str) -> str:
    """간단한 라우터: 질문 유형에 따라 검색 방식 선택 (실무에서는 작은 LLM이 이 역할을 하기도 함)"""
    relation_words = ["공급", "경쟁", "영향", "관계", "거래"]
    describe_words = ["무엇", "설명", "소개", "특징", "계획"]
    r, d = any(w in q for w in relation_words), any(w in q for w in describe_words)
    return "hybrid" if r and d else "graph" if r else "vector"


QUESTIONS = [
    "양극재는 무엇인가?",
    "D화학과 공급 관계로 연결된 회사는?",
    "D화학의 생산 차질이 A전자에 영향을 줄 수 있는지, 관련 소식과 함께 설명해 줘",
]
for q in QUESTIONS:
    mode = route(q)
    ctx = (doc_search(q) if mode in ("vector", "hybrid") else []) + \
          (graph_search(q) if mode in ("graph", "hybrid") else [])
    print(f"질문: {q}\n방식: {mode}")
    for c in ctx:
        print("  ", c)
    print()
