import pytest

from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA

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