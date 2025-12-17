import datetime
import hashlib

if __name__ == '__main__':
    print(datetime.datetime.now())

    hexdigest = hashlib.sha256('hello'.encode('utf-8')).hexdigest()
    print(hexdigest)

    print("hello world")


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')  # 제네시스 블록 생성에 대한 부분이다. , 임의의 시작값 1, 이전 블록이 없으므로 0 으로 설정

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        return block

    def proof_of_work(self):
        previous_block = self.get_previous_block()
        previous_proof = previous_block['proof']
        new_proof = 1
        check_proof = False

        while not check_proof:
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def get_previous_block(self):
        return self.chain[-1]
