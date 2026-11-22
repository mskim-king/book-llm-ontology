<!--
**상태**: 🔵 검토 중
**분류**: 90. 부록
**태그**: #부록 #도구
**작성일**: 2026-11-22
-->
> 📅 **최종 확인**: 2026-11-22

온톨로지와 지식그래프 작업에 쓰는 대표적인 도구를 용도별로 정리했습니다. 제품의 기능·라이선스·가격은 자주 바뀌므로, 도입 전에 공식 사이트에서 확인하세요.

## 요약

- 처음 배울 때는 **파이썬(rdflib) + 편집기(Protégé)**면 충분합니다.
- 데이터가 커지면 **트리플스토어 또는 그래프DB**를 도입합니다.
- 이 책의 예제는 모두 **rdflib과 pyshacl**만으로 실행됩니다.

## 용도별 도구

| 용도 | 도구 | 특징 | 이 책에서 |
|---|---|---|---|
| 온톨로지 편집 | Protégé | 스탠퍼드에서 만든 무료 OWL 편집기, 추론기 연동 | — |
| 파이썬 RDF 처리 | rdflib | RDF 읽기·쓰기, SPARQL 실행 | 모든 예제 |
| 데이터 검증 | pySHACL | 파이썬 SHACL 검사기 | 02-4 |
| RDFS·OWL 추론 | OWL-RL (파이썬) | RDFS·OWL RL 수준 추론 | 02-2 소개 |
| 트리플스토어 | Apache Jena Fuseki | 오픈소스 SPARQL 서버 | 03-1 소개 |
| 트리플스토어 | GraphDB, Virtuoso 등 | 추론·대용량 지원 제품 | 03-1 소개 |
| 그래프DB | Neo4j, Memgraph 등 | 속성 그래프, Cypher | 03-3 |
| 공개 지식그래프 | Wikidata | 누구나 편집하는 대규모 지식그래프, SPARQL 질의 서비스 | — |

## 설치 (이 책 예제)

```bash
pip install rdflib pyshacl
python code/01_rdf_basics.py
```

저장소의 `code/requirements.txt`에 필요한 라이브러리가 정리되어 있습니다.

## 예제 코드 목록

| 파일 | 내용 | 페이지 |
|---|---|---|
| `01_rdf_basics.py` | 트리플 만들기, Turtle 저장 | 02-1 |
| `02_rdfs_inference.py` | 클래스 계층·대칭 관계 추론 | 02-2 |
| `03_skos.py` | 동의어 → 대표어 정규화 | 02-3 |
| `04_shacl.py` | SHACL 데이터 검증 | 02-4 |
| `05_sparql.py` | SPARQL 다섯 가지 질문 | 03-2 |
| `06_llm_to_triples.py` | LLM 추출 결과 검증·반영 | 04-2 |
| `07_schema_prompt.py` | 온톨로지에서 추출 프롬프트 생성 | 05-1 |
| `08_graphrag.py` | GraphRAG 근거 구성 | 05-2 |
| `09_evaluate.py` | 정밀도·재현율·F1 | 07-1 |
| `10_consistency.py` | 모순 검사 | 07-2 |
| `11_supply_risk.py` | 공급망 핵심 노드 | 08-1 |
| `12_hybrid_rag.py` | 벡터·그래프·하이브리드 검색과 라우터 | 06-1 |

모든 예제는 GitHub Actions로 자동 실행 검사를 합니다.

## 근거·출처

| 도구 | 공식 사이트 |
|---|---|
| Protégé | [protege.stanford.edu](https://protege.stanford.edu/) |
| rdflib | [rdflib.readthedocs.io](https://rdflib.readthedocs.io/) |
| pySHACL | [github.com/RDFLib/pySHACL](https://github.com/RDFLib/pySHACL) |
| OWL-RL | [github.com/RDFLib/OWL-RL](https://github.com/RDFLib/OWL-RL) |
| Apache Jena Fuseki | [jena.apache.org](https://jena.apache.org/documentation/fuseki2/) |
| Neo4j | [neo4j.com](https://neo4j.com/) |
| Wikidata | [wikidata.org](https://www.wikidata.org/) |

## 관련 페이지

- 90-2. 용어집
- 📚 03-1. 트리플스토어 vs 그래프 데이터베이스
- 📚 09-1. 기법·도구 업데이트 노트
