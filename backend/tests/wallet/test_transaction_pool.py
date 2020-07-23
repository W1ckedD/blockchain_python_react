from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.blockchain.blockchain import Blockchain

def test_set_transacton():
    transaction_pool = TransactionPool()
    transaction = Transaction(Wallet(), 'foo', 1)
    transaction_pool.set_transaction(transaction)

    assert transaction_pool.transaction_map[transaction.id] == transaction

def test_clear_blockchain_transactions():
    transaction_pool = TransactionPool()
    
    transaction1 = Transaction(Wallet(), 'foo', 1)
    transaction2 = Transaction(Wallet(), 'foo', 2)
    transaction3 = Transaction(Wallet(), 'foo', 3)
    
    transaction_pool.set_transaction(transaction1)
    transaction_pool.set_transaction(transaction2)
    transaction_pool.set_transaction(transaction3)

    blockchain = Blockchain()
    blockchain.add_block([transaction1.to_json(), transaction2.to_json(), transaction3.to_json()])

    assert transaction1.id in transaction_pool.transaction_map
    assert transaction2.id in transaction_pool.transaction_map
    assert transaction3.id in transaction_pool.transaction_map

    transaction_pool.clear_blockchain_transactions(blockchain)

    assert not transaction1.id in transaction_pool.transaction_map
    assert not transaction2.id in transaction_pool.transaction_map
    assert not transaction3.id in transaction_pool.transaction_map

