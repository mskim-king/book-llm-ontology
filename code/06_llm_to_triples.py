"""04-2. 관계 추출과 트리플 생성 — LLM 출력(JSON)을 검증해 지식그래프에 넣기

실제 LLM 호출 대신, LLM이 돌려준 것으로 가정한 JSON 예시를 사용합니다.
"""
import json
from rdflib import Literal, RDFS
from common import load, EX

# 원문 (가상의 뉴스 문장)
TEXT = "D화학은 올해부터 C전자에 신규 소재를 공급한다. B소재는 E배터리와 양극재 공급 계약을 맺었다. 한편 A전자는 서울에 본사를 두고 있다."

# LLM이 돌려준 것으로 가정한 결과 (프롬프트는 04-2 페이지 참고)
LLM_OUTPUT = json.loads("""
{"triples": [
  {"subject": "D화학", "relation": "공급한다", "object": "C전자", "evidence": "D화학은 올해부터 C전자에 신규 소재를 공급한다"},
  {"subject": "B소재", "relation": "공급한다", "object": "E배터리", "evidence": "B소재는 E배터리와 양극재 공급 계약을 맺었다"},
  {"subject": "A전자", "relation": "본사 위치", "object": "서울", "evidence": "A전자는 서울에 본사를 두고 있다"},
  {"subject": "B소재", "relation": "공급한다", "object": "F모터스", "evidence": "B소재는 F모터스에 공급한다"}
]}
""")

g = load()
label_to_node = {str(o): s for s, _, o in g.triples((None, RDFS.label, None))}
relation_map = {"공급한다": EX.suppliesTo, "경쟁한다": EX.competesWith, "근무한다": EX.worksFor}

accepted, review = [], []
for t in LLM_OUTPUT["triples"]:
    reasons = []
    if t["relation"] not in relation_map:
        reasons.append("온톨로지에 없는 관계")
    if t["evidence"] not in TEXT:
        reasons.append("근거 문장이 원문에 없음(환각 의심)")
    for key in ("subject", "object"):
        if t[key] not in label_to_node:
            reasons.append(f"새 개체 '{t[key]}' (등록 필요)")
    (review if reasons else accepted).append((t, reasons))

print("✅ 자동 반영")
for t, _ in accepted:
    s, o = label_to_node[t["subject"]], label_to_node[t["object"]]
    is_new = (s, relation_map[t["relation"]], o) not in g
    g.add((s, relation_map[t["relation"]], o))
    print(f"   {t['subject']} -{t['relation']}→ {t['object']}  ({'새 사실' if is_new else '이미 있음'})")

print("\n🧑‍🔬 사람 검토 대기")
for t, reasons in review:
    print(f"   {t['subject']} -{t['relation']}→ {t['object']}  : {', '.join(reasons)}")
