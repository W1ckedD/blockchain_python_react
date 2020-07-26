import pytest

from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet

def test_blockchain_instance():
    blockchain = Blockchain()
    assert blockchain.chain[0].hash == GENESIS_DATA['hash']

def test_add_block():
    blockchain = Blockchain()
    data = 'test-data'
    blockchain.add_block(data)

    assert blockchain.chain[-1].data == data

def test_is_valid_chain():
    blockchain = Blockchain()

    for i in range(3):
        blockchain.add_block(i)

    Blockchain.is_valid_chain(blockchain.chain)

def test_is_valid_chain_bad_genesis():
    blockchain = Blockchain()

    for i in range(3):
        blockchain.add_block(i)

    blockchain.chain[0].hash = 'bad-hash'
    
    with pytest.raises(Exception, match='The genesis block must be valid'):
        Blockchain.is_valid_chain(blockchain.chain)

def test_replace_chain():
    blockchain = Blockchain()
    blockchain_three_blocks = Blockchain()
    for i in range(3):
        blockchain_three_blocks.add_block(i)

    blockchain.replace_chain(blockchain_three_blocks.chain)

    assert blockchain_three_blocks.chain == blockchain.chain

def test_replace_chain_not_longer():
    blockchain_three_blocks = Blockchain()
    for i in range(3):
        blockchain_three_blocks.add_block(i)

    blockchain = Blockchain()
    
    with pytest.raises(Exception, match="Cannot replace. The incomming chain must be longer"):
        blockchain_three_blocks.replace_chain(blockchain.chain)

def test_replace_chain_bad_chain():
    blockchain = Blockchain()
    blockchain_three_blocks = Blockchain()
    for i in range(3):
        blockchain_three_blocks.add_block(i)

    blockchain_three_blocks.chain[1].hash = 'bad-hash'
      
    with pytest.raises(Exception, match="Cannot replace. The incomming chain is invalid"):
        blockchain.replace_chain(blockchain_three_blocks.chain)

def test_is_valid_transaction_chain():
    blockchain = Blockchain()
    blockchain_three_blocks = Blockchain()
    for i in range(3):
        blockchain_three_blocks.add_block([Transaction(Wallet(), 'recipient', i).to_json()])

    Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)

def test_is_valid_transaction_chain_duplicate_transactions():
    blockchain_three_blocks = Blockchain()
    for i in range(3):
        blockchain_three_blocks.add_block([Transaction(Wallet(), 'recipient', i).to_json()])

    transaction = Transaction(Wallet(), 'recipient', 10).to_json()
    blockchain_three_blocks.add_block([transaction, transaction, transaction])

    with pytest.raises(Exception, match='is not unique'):
        Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)

def test_is_valid_transaction_chain_multiple_rewards():
    blockchain_three_blocks = Blockchain()
    for i in range(3):
        blockchain_three_blocks.add_block([Transaction(Wallet(), 'recipient', i).to_json()])

    reward1 = Transaction.reward_transaction(Wallet()).to_json()
    reward2 = Transaction.reward_transaction(Wallet()).to_json()
    blockchain_three_blocks.add_block([reward1, reward2])

    with pytest.raises(Exception, match='one minig reward per block'):
        Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)

def test_is_valid_transaction_chain_bad_transaction():
    blockchain_three_blocks = Blockchain()
    for i in range(3):
        blockchain_three_blocks.add_block([Transaction(Wallet(), 'recipient', i).to_json()])

    bad_transaction = Transaction(Wallet(), 'recipient', 1)
    bad_transaction.input['signature'] = Wallet().sign(bad_transaction.output)
    blockchain_three_blocks.add_block([bad_transaction.to_json()])

    with pytest.raises(Exception):
        Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)
