from flask import Flask, jsonify
from blockchain import Blockchain, Block


app = Flask(__name__)

blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    block = blockchain.do_create_block("New Block Data")
    response = {
        'index': block.index,
        'timestamp': block.timestamp,
        'nonce': block.nonce,
        'data': block.data,
        'previous_hash': block.previous_hash,
        'hash': block.to_hash()
    }
    return jsonify(response), 200

@app.route("/chain", methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append({
            'index': block.index,
            'timestamp': block.timestamp,
            'nonce': block.nonce,
            'data': block.data,
            'previous_hash': block.previous_hash,
            'hash': block.to_hash()
        })
    response = {
        'length': len(chain_data),
        'chain': chain_data
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run()