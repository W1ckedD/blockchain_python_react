import pytest

from backend.wallet.wallet import Wallet

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