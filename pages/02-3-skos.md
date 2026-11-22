<!--
**상태**: 🔵 검토 중
**분류**: 02. 표준과 언어
**태그**: #표준 #SKOS
**작성일**: 2026-11-22
-->
> 📅 **최종 확인**: 2026-11-22

SKOS(Simple Knowledge Organization System)는 **용어집·분류 체계·시소러스**를 표현하는 W3C 표준입니다. 엄격한 논리 규칙이 필요 없는 용어 관리에 알맞아서, 온톨로지 프로젝트를 **가볍게 시작할 때** 가장 많이 씁니다.

## 요약

- SKOS는 **개념(Concept)**을 중심으로 대표어·동의어·상하위어·관련어를 표현합니다.
- 검색어 정규화, 태그 정리, 사내 용어 통일에 바로 쓸 수 있습니다.
- LLM에게 **우리 조직의 공식 용어**를 알려 줄 때도 유용합니다.

## SKOS 핵심 어휘

| 어휘 | 뜻 | 예시 |
|---|---|---|
| `skos:prefLabel` | 대표어 (언어별로 하나) | 2차전지 |
| `skos:altLabel` | 동의어·약어·다른 표기 | 배터리, 축전지 |
| `skos:broader` / `skos:narrower` | 상위어 / 하위어 | 양극재 → 2차전지 소재 |
| `skos:related` | 관련어 | 2차전지 소재 ~ 2차전지 |
| `skos:definition` | 정의 문장 | "충전해 반복 사용하는 전지" |
| `skos:ConceptScheme` | 용어 체계 전체 | 「배터리 산업 용어집」 |

## 예시: 배터리 산업 용어 체계

```turtle
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix ex:   <http://example.org/terms#> .

ex:Battery skos:prefLabel "2차전지"@ko ;
           skos:altLabel "배터리"@ko , "축전지"@ko .

ex:Cathode skos:prefLabel "양극재"@ko ;
           skos:altLabel "양극 소재"@ko ;
           skos:broader ex:BatteryMaterial .

ex:Anode   skos:prefLabel "음극재"@ko ;
           skos:broader ex:BatteryMaterial .

ex:BatteryMaterial skos:prefLabel "2차전지 소재"@ko ;
                   skos:related ex:Battery .
```

## 코드: 동의어를 대표어로 바꾸기

검색창에 "배터리"를 입력해도 "2차전지" 문서를 찾으려면, 입력한 말을 대표어로 바꿔야 합니다. 전체 코드는 `code/03_skos.py`입니다.

```python
def normalize(word: str) -> str:
    """동의어를 대표어로 바꾸기"""
    q = """
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    SELECT ?pref WHERE {
      ?c skos:prefLabel ?pref .
      { ?c skos:prefLabel ?w } UNION { ?c skos:altLabel ?w }
      FILTER(STR(?w) = ?word)
    }"""
    rows = list(g.query(q, initBindings={"word": Literal(word)}))
    return str(rows[0].pref) if rows else word

for w in ["배터리", "축전지", "양극 소재", "음극재", "반도체"]:
    print(f"{w:6} → {normalize(w)}")
```

**실행 결과**

```text
배터리    → 2차전지
축전지    → 2차전지
양극 소재  → 양극재
음극재    → 음극재
반도체    → 반도체

'2차전지 소재'의 하위어: ['양극재', '음극재']
```

용어집에 없는 "반도체"는 그대로 돌려줍니다. 이런 단어를 모아 두면 **용어집에 추가할 후보 목록**이 됩니다.

[[TIP("요령: LLM 프롬프트에 용어집 넣기")]]

LLM에게 보고서 요약을 맡길 때 "다음 용어집의 대표어로만 써 줘"라며 SKOS의 대표어·동의어 목록을 함께 주면, 문서마다 용어가 들쭉날쭉한 문제를 줄일 수 있습니다.

[[/TIP]]

## SKOS와 OWL 언제 무엇을 쓰나

| 상황 | 추천 |
|---|---|
| 용어 통일, 검색어 확장, 태그 관리 | SKOS |
| 개념 사이에 논리 규칙과 추론이 필요 | OWL |
| 둘 다 필요 | SKOS로 용어를 관리하고, OWL 클래스와 연결 |

## 실무 체크포인트

- [ ] 개념마다 대표어(prefLabel)를 언어별로 하나만 정했는가
- [ ] 약어·옛 표기·자주 틀리는 표기를 동의어(altLabel)로 등록했는가
- [ ] 용어집에 없는 검색어를 모아 정기적으로 반영하는가

## 근거·출처

| 구분 | 출처 | 비고 |
|---|---|---|
| 표준 | [SKOS Simple Knowledge Organization System Reference (W3C)](https://www.w3.org/TR/skos-reference/) | 어휘 정의 |
| 표준 | [SKOS Primer (W3C)](https://www.w3.org/TR/skos-primer/) | 입문 |

## 관련 페이지

- 02-2. RDFS와 OWL
- 📚 01-3. 택소노미·시소러스와의 차이
- 📚 04-1. 문서에서 개념 추출
