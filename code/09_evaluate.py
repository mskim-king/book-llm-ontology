"""06-1. 품질 지표 — 추출 결과를 정답과 비교해 정밀도·재현율·F1 계산"""
GOLD = {  # 사람이 만든 정답 트리플
    ("D화학", "공급한다", "C전자"),
    ("B소재", "공급한다", "E배터리"),
    ("A전자", "본사 위치", "서울"),
    ("A전자", "만든다", "스마트폰 X"),
}
PRED = {  # 시스템(LLM)이 추출한 트리플
    ("D화학", "공급한다", "C전자"),
    ("B소재", "공급한다", "E배터리"),
    ("A전자", "본사 위치", "서울"),
    ("B소재", "공급한다", "F모터스"),   # 원문에 없는 사실(환각)
}
tp = len(GOLD & PRED)
precision = tp / len(PRED)
recall = tp / len(GOLD)
f1 = 2 * precision * recall / (precision + recall)
print(f"맞힌 수(TP) {tp} / 추출 {len(PRED)} / 정답 {len(GOLD)}")
print(f"정밀도 {precision:.2f} · 재현율 {recall:.2f} · F1 {f1:.2f}")
print("놓친 사실:", sorted(GOLD - PRED))
print("틀린 사실:", sorted(PRED - GOLD))
