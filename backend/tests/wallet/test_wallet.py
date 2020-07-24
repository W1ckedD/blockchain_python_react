import pytest

from backend.blockchain.blockchain import Blockchain
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.config import STARTING_BALANCE


def test_verify_wallet_valid_signature():
    data = {'test': 'test_data'}
    wallet = Wallet()
    signature = wallet.sign(data)

    assert Wallet.verify(wallet.public_key, data, signature)


def test_verify_wallet_invalid_signature():
    data = {'test': 'test_data'}
    wallet = Wallet()
    signature = wallet.sign(data)

    assert not Wallet.verify(wallet.public_key, 'different-data', signature)


def test_calculate_balance():
    blockchain = Blockchain()
    wallet = Wallet()

    assert Wallet.calculate_balance(
        blockchain, wallet.address) == STARTING_BALANCE

    amount = 20
    transacion = Transaction(wallet, 'recipient', amount)
    blockchain.add_block([transacion.to_json()])
    assert Wallet.calculate_balance(
        blockchain, wallet.address) == STARTING_BALANCE - amount

    recieved_amount1 = 10
    recieved_transaction1 = Transaction(
        Wallet(),
        wallet.address,
        recieved_amount1
    )
    recieved_amount2 = 40
    recieved_transaction2 = Transaction(
        Wallet(),
        wallet.address,
        recieved_amount2
    )
    blockchain.add_block([recieved_transaction1.to_json(),
                          recieved_transaction2.to_json()])
    assert Wallet.calculate_balance(
        blockchain, wallet.address) == STARTING_BALANCE - amount + recieved_amount1 + recieved_amount2
