import dataclasses
import datetime
import hashlib
import json


@dataclasses.dataclass
class Block:
    def __init__(self, index, timestamp, nonce, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.nonce = nonce
        self.data = data
        self.previous_hash = previous_hash

    def plus_nonce(self):
        self.nonce += 1

    # 파이썬 딕셔너리 형태인 블록을 문자열로 변경하는 것이다. (직렬화), sort_keys=True -> 키를 정렬하여 알파벳 순으로 정렬
    # 내용은 같지만 순서가 다른 JSON 객체는 아예 다른 값으로 취급되고, 해시값도 완전히 달라지므로 정렬이 중요하다.
    def to_hash(self):
        encoded_block = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain: list[Block] = []
        self.create_block(data='Genesis Block',
                          previous_hash='0')  # 제네시스 블록 생성에 대한 부분이다. , 임의의 시작값 1, 이전 블록이 없으므로 0 으로 설정

    def proof_of_work(self, block: Block):
        check_proof = False

        while check_proof is False:
            block_hash = block.to_hash()

            # 3. 난이도 체크: 앞자리가 '0000'인지 확인
            if block_hash[:4] == '0000':
                check_proof = True
            else:
                block.plus_nonce()

    def do_create_block(self, data="New Block Data"):
        previous_block = self.chain[-1]
        previous_block_hash = previous_block.to_hash()

        return self.create_block(data, previous_block_hash)

    def create_block(self, data, previous_hash):
        block = Block(
            index=len(self.chain) + 1,
            timestamp=str(datetime.datetime.now()),
            nonce=0,
            data=data,
            previous_hash=previous_hash
        )
        self.proof_of_work(block)
        self.chain.append(block)
        return block

    def print_chain(self):
        for block in self.chain:
            print(f'Index: {block.index}')
            print(f'Timestamp: {block.timestamp}')
            print(f'Nonce: {block.nonce}')
            print(f'Data: {block.data}')
            print(f'Previous Hash: {block.previous_hash}')
            print(f'Hash: {block.to_hash()}')
            print('---------------------------')

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # 1. 이전 해시값 검증
            if current_block.previous_hash != previous_block.to_hash():
                return False

            # 2. 현재 블록의 해시값 검증
            if current_block.to_hash()[:4] != '0000':
                return False

        return True

if __name__ == '__main__':
    blockchain = Blockchain()
    block = blockchain.do_create_block('First Block after Genesis')
    blockchain.print_chain()

    valid = blockchain.is_valid()
    print(f'Blockchain valid: {valid}')
