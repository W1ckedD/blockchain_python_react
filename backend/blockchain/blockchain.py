from backend.blockchain.block import Block


class Blockchain(object):
    '''
    Blockchain: a public ledger of transactions.
    Implemented as a list of blocks - data sets of transactions
    '''

    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        last_block = self.chain[-1]
        block = Block.mine_block(last_block, data)
        self.chain.append(block)

    def replace_chain(self, chain):
        '''
        Replace the local change with the incomming one if the following rules apply:
            - The incomming chain must be longer than the local one
            - The incomming chain must be formatted propperly 
        '''

        if len(chain) <= len(self.chain):
            raise Exception(
                'Cannot replace. The incomming chain must be longer')
        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(
                f'Cannot replace. The incomming chain is invalid: {e}')

        self.chain = chain

    def __repr__(self):
        return f'Blockchain: {self.chain}'

    def to_json(self):
        '''
        Serialize the blockchain to a list of blocks
        '''
        return [block.to_json() for block in self.chain]

    @staticmethod
    def from_json(chain_json):
        '''
        Deserialize a list of serialized blocks into a blockchain instance
        The result will contain a chain list of block instances
        '''
        blockchain = Blockchain()
        blockchain.chain = list(
            map(lambda block_json: Block.from_json(block_json), chain_json))
        return blockchain

    @staticmethod
    def is_valid_chain(chain):
        '''
        Validate the incoming chain
        Enforce the following rules of the blockchain
            - Chain must start with genesis block
            - Blocks must be formatted correctly
        '''
        if chain[0].__dict__ != Block.genesis().__dict__:
            raise Exception('The genesis block must be valid')
        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, block)