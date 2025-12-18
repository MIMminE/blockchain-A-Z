# 학습용 간단 블록체인 구현 (module 1)

최소 기능의 블록체인 ( 블록 생성, 해시 계산, 작업 증명)을 구현하여 동작 원리를 이해한다.

**핵심 아이디어**: 각 블록은 이전 블록의 해시를 포함하고, 작업 증명(proof-of-work)을 통해 블록의 해시가 특정 난이도(여기서는 앞자리 '0000') 조건을 만족하도록 논스(nonce)를 증가시킨다.

## 빠른 동작 흐름 요약

1. Blockchain 클래스가 생성되면 생성자에서 제네시스 블록(Genesis Block)을 만든다.
2. `do_create_block`을 호출하면 마지막 블록의 해시를 가져와 새 블록을 만들기 위해 `create_block`을 호출한다.
3. `create_block`는 새 Block 객체를 만들고 `proof_of_work`를 통해 조건을 만족하는 nonce를 찾는다.
4. 조건을 만족하면 블록을 체인에 추가하고, `print_chain`으로 전체 블록체인을 출력할 수 있다.

## 코드 주요 구성 및 동작(함수/메서드별)

1) Block 클래스

- 생성자: index, timestamp, nonce, data, previous_hash를 속성으로 가진다.
- plus_nonce(self): nonce를 1 증가시킨다.
- to_hash(self): 블록의 내용을 정렬된 JSON으로 직렬화한 뒤 SHA-256 해시(16진 문자열)를 반환한다.
    - 이유: 딕셔너리의 키 순서가 달라지면 다른 해시가 나오므로 `sort_keys=True`로 안정적인 직렬화를 보장한다.
    - 입력: 없음(블록 내부 상태 사용).
    - 출력: 문자열(해시값).

2) Blockchain 클래스

- __init__(self): 빈 체인 리스트를 만들고 `create_block`을 호출하여 제네시스 블록을 생성한다. 제네시스 블록의 previous_hash는 문자열 '0'으로 설정된다.
- proof_of_work(self, block: Block): 주어진 블록의 `to_hash()`가 앞 네 자리가 '0000'인 해시를 찾을 때까지 `block.plus_nonce()`로 nonce를 증가시킨다.
    - 난이도: 하드코딩된 조건 `block_hash[:4] == '0000'` (난이도 4자릿수 영).
    - 특징: 단순한 반복 탐색(브루트포스).종료 보장을 위해 nonce는 정수이므로 언젠가 조건을 만족하거나 매우 오랜 시간이 걸릴 수 있음.
    - 시간 복잡도: 기대적으로는 16^4(약 65536) 시도 정도(해시의 무작위성에 따라) — 실제는 확률적.
- do_create_block(self, data="New Block Data"): 마지막 블록의 해시를 읽어와 `create_block` 호출.
- create_block(self, data, previous_hash): 새 Block 객체(논스 0) 생성 후 `proof_of_work` 실행, 완료되면 체인에 append하고 블록을 반환한다.
- print_chain(self): 체인에 있는 모든 블록의 속성(index, timestamp, nonce, data, previous_hash, hash)을 출력한다.

## 예상 출력 예시

- 실제 해시와 nonce 값은 실행 시점마다 바뀝니다(시간, 난수성 때문에). 아래는 출력 포맷 예시입니다.

```
Index: 1
Timestamp: 2025-01-01 12:00:00.000000
Nonce: 5231
Data: Genesis Block
Previous Hash: 0
Hash: 0000a4b3... (앞자리가 0000)
---------------------------
Index: 2
Timestamp: 2025-01-01 12:00:05.123456
Nonce: 214
Data: First Block after Genesis
Previous Hash: 0000a4b3...
Hash: 00009f2c... (앞자리가 0000)
---------------------------
```

- 출력 해석:
    - Index: 블록의 순서(여기선 1부터 시작).
    - Timestamp: 블록 생성 시점(문자열 형식).
    - Nonce: 작업 증명을 통해 찾은 정수값으로, 이 값을 변경하면 해시가 바뀐다.
    - Previous Hash: 이전 블록의 해시 (제네시스는 '0').
    - Hash: 현재 블록의 유효 해시(앞 네 자리가 0000이 되도록 찾음).

실행 결과의 의미(블록체인 원리 관점)

- 제네시스 블록: 체인의 시작 블록으로 previous_hash를 '0'으로 설정해 특수 처리한다.
- 불변성: 이후 블록의 previous_hash가 이전 블록의 해시에 의존하므로 한 블록을 변경하면 이후 블록의 해시들이 모두 달라져 체인의 무결성이 깨진다.
- 작업 증명: 특정 조건(여기선 해시 앞 4글자 0)을 만족시키기 위해 연산(해시 계산)을 반복하는 과정으로, 네트워크적 합의 및 공격 비용을 높이는 역할을 한다.

