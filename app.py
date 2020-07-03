from backend.blockchain.blockchain import Blockchain

def main():
    blockchain = Blockchain()
    blockchain.add_block('One')
    blockchain.add_block('Two')
    blockchain.add_block('Three')
    print(blockchain)

if __name__ == '__main__':
    main()
