import pytest

from backend.wallet.wallet import Wallet

def test_verify_wallet_valid_signiture():
    data = {'test': 'test_data'}
    wallet = Wallet()
    signiture = wallet.sign(data)
    
    assert Wallet.verify(wallet.public_key, data, signiture)

def test_verify_wallet_invalid_signiture():
    data = {'test': 'test_data'}
    wallet = Wallet()
    signiture = wallet.sign(data)
    
    assert not Wallet.verify(wallet.public_key, 'different-data', signiture)