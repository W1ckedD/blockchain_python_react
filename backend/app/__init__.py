import os
import random
import requests

from flask import Flask, jsonify, request
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool

app = Flask(__name__)

blockchain = Blockchain()
wallet = Wallet(blockchain)
transaction_pool = TransactionPool()

pubsub = PubSub(blockchain, transaction_pool)


@app.route('/')
def index():
    return '<h1>Index page</h1>'


@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())


@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = transaction_pool.transaction_data()
    transaction_data.append(Transaction.reward_transaction(wallet).to_json())
    blockchain.add_block(transaction_data)
    mined_data = blockchain.chain[-1]
    pubsub.broadcast_block(mined_data)
    transaction_pool.clear_blockchain_transactions(blockchain)
    

    return jsonify(mined_data.to_json())


@app.route('/wallet/transact', methods=['POST'])
def route_wallet_transact():
    tranasction_data = request.get_json()
    transaction = transaction_pool.existing_transaction(wallet.address)
    if transaction:
        transaction.update(
            wallet,
            tranasction_data['recipient'],
            tranasction_data['amount']
        )
    else:
        transaction = Transaction(
            wallet,
            tranasction_data['recipient'],
            tranasction_data['amount']
        )
    pubsub.brodcast_transaction(transaction)
    return jsonify(transaction.to_json())

@app.route('/wallet/info')
def route_wallet_info():
    return jsonify({ 'address': wallet.address, 'balance': wallet.balance })

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
