<!--
**상태**: 🔵 검토 중
**분류**: 03. 지식그래프와 질의
**태그**: #지식그래프 #질의 #Cypher
**작성일**: 2026-11-22
-->
> 📅 **최종 확인**: 2026-11-22

Cypher는 그래프 데이터베이스에서 널리 쓰는 질의 언어입니다. `(노드)-[:관계]->(노드)`처럼 **그림을 그리듯** 패턴을 적는 것이 특징입니다. 이 페이지에서는 03-2의 SPARQL 질문을 Cypher로 바꿔 적으며 차이를 비교합니다.

## 요약

- Cypher는 노드를 `( )`, 관계를 `-[ ]->`로 적어 **패턴을 그림처럼** 표현합니다.
- 노드와 관계 모두에 **속성**을 붙일 수 있습니다.
- Cypher를 바탕으로 한 국제 표준 그래프 질의 언어 **GQL**(ISO/IEC 39075)도 발표되었습니다.

## 데이터 만들기

예제 데이터를 그래프DB에 넣는 Cypher 문입니다.

```cypher
CREATE (a:Company {name: "A전자", founded: 1990}),
       (c:Company {name: "C전자", founded: 2001}),
       (b:Company {name: "B소재", founded: 2008}),
       (d:Company {name: "D화학", founded: 1975}),
       (b)-[:SUPPLIES_TO]->(a),
       (d)-[:SUPPLIES_TO]->(b),
       (d)-[:SUPPLIES_TO]->(c),
       (a)-[:COMPETES_WITH]->(c)
```

## SPARQL과 나란히 보기

| 질문 | SPARQL | Cypher |
|---|---|---|
| 2000년 이후 설립 회사 | `?c ex:foundedYear ?y . FILTER(?y >= 2000)` | `MATCH (c:Company) WHERE c.founded >= 2000 RETURN c.name` |
| A전자 직접 공급사 | `?s ex:suppliesTo ex:AElec` | `MATCH (s)-[:SUPPLIES_TO]->(:Company {name:"A전자"}) RETURN s.name` |
| 공급망 전체 (몇 단계든) | `?s ex:suppliesTo+ ex:AElec` | `MATCH (s)-[:SUPPLIES_TO*1..]->(:Company {name:"A전자"}) RETURN DISTINCT s.name` |

## 예제: 경쟁사에도 납품하는 공급망 기업

03-2의 ⑤번 질문을 Cypher로 적으면 다음과 같습니다.

```cypher
MATCH (s:Company)-[:SUPPLIES_TO*1..]->(a:Company {name: "A전자"}),
      (a)-[:COMPETES_WITH]-(rival:Company),
      (s)-[:SUPPLIES_TO]->(rival)
RETURN DISTINCT s.name
```

`(a)-[:COMPETES_WITH]-(rival)`처럼 **화살표 없이** 적으면 방향과 상관없이 찾습니다. RDF에서 대칭 관계를 OWL로 정의했던 것과 같은 효과입니다. 위 데이터에서는 03-2와 같이 **D화학**을 돌려주도록 작성했습니다.

[[TIP("알림")]]

이 책의 자동 검사 환경에는 그래프DB가 없어서, 이 페이지의 Cypher 문은 실행 결과를 싣지 않았습니다. 같은 질문의 실행 결과는 03-2의 SPARQL 예제에서 확인할 수 있습니다. Neo4j 등에서 직접 실행해 보세요.

[[/TIP]]

## 관계에 속성 붙이기

그래프DB의 장점은 관계에 바로 속성을 붙일 수 있다는 점입니다.

```cypher
MATCH (b:Company {name: "B소재"})-[r:SUPPLIES_TO]->(a:Company {name: "A전자"})
SET r.since = 2023, r.share = 0.4      // 2023년부터, 물량 비중 40% (가상)
RETURN b.name, r.since, r.share, a.name
```

## 실무 체크포인트

- [ ] 관계 이름 규칙(대문자 + 밑줄 등)을 정했는가
- [ ] 반복 경로(`*1..`)에는 최대 깊이를 정해 너무 긴 탐색을 막았는가
- [ ] RDF 데이터와 연결해야 한다면 변환 방법을 정했는가

## 근거·출처

| 구분 | 출처 | 비고 |
|---|---|---|
| 언어 | [openCypher](https://opencypher.org/) | Cypher 명세 |
| 표준 | [ISO/IEC 39075 GQL](https://www.iso.org/standard/76120.html) | 국제 표준 그래프 질의 언어 |
| 도구 | [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/current/) | 문법 참고 |

## 관련 페이지

- 03-1. 트리플스토어 vs 그래프 데이터베이스
- 03-2. SPARQL 기초
- 📚 05-2. GraphRAG 이해와 구현
