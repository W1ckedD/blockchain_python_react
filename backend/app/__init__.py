import os
import random
import requests

from flask import Flask, jsonify, request
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub

app = Flask(__name__)

blockchain = Blockchain()
for i in range(3):
    blockchain.add_block(i)

pubsub = PubSub(blockchain)

@app.route('/')
def index():
    return '<h1>Index page</h1>'

@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())

@app.route('/blockchain/mine', methods=['GET', 'POST'])
def route_blockchain_mine():
    if request.method == 'GET':
        return '''
        <form action="/blockchain/mine" method="POST">
            <button type="submit">Mine</button>
        </form>
        '''
    elif request.method == 'POST':
        blockchain.add_block('dummy-data')
        mined_data = blockchain.chain[-1]
        pubsub.broadcast_block(mined_data)
        return jsonify(mined_data.to_json())

ROOT_PORT = 5000
PORT = ROOT_PORT

if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 6000)
    result = requests.get(f'http://localhost:{ROOT_PORT}/blockchain')
    result_blockchain = Blockchain.from_json(result.json())
    try:
        blockchain.replace_chain(result_blockchain.chain)
        print('\n -- successfully synchronized the local chain')
    except Exception as e:
        print(f'\n -- error synchronizing: {e}')

app.run(port=PORT)
