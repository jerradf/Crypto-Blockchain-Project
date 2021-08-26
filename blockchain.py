# blockchain.py
# Author: Jerrad Flores

# This is a Python interpretation of a cryptocurrency Blockchain

import block
import hashlib


class Blockchain:
    
    def __init__(self, name):
        # self.chain is where we will store all of the cryptocurrency coin blocks
        self.chain = []

        # self.completed_transactions is where we will store all of the completed transations
        # This will be reinitialized as empty after every time we create a new block
        # (this is because we want to ensure that future transactions are accurately added into the list
        # for this specific block ONLY.)
        # A list of dictionaries. Each index will be a dictionary.
        #      [{sender, recipient, quantity}, {sender, recipient, quantity}, {sender, recipient, quantity}]
        self.completed_transactions = []

        # self.nodes is the set of computers/servers/locations that connects to the blockchain.
        # This is more practical with larger blockchains (such as IBM Blockchain Platform,
        # which has hundreds of nodes connected to their network)
        # We want to use a set for this because each individual node is unique
        # (the location cannot be duplicated).
        self.nodes = set()
        
        # Call the self.construct_genesis_block() method when we initialize the Blockchain
        # (this is so that we don't have to worry about the user having to deal with this; 
        # it should automatically occur at the start).
        self.construct_genesis_block()

        # self.last_block allows us to get the last block (the one that was most recently added to the Blockchain)
        self.last_block = self.chain[-1]


    def construct_genesis_block(self):
        # The Genesis Block (block 0 in the blockchain)
        # The very first cryptocurrency coin block upon which additional blocks in a blockchain are added. 
        # This is known as the ancestor of every block
        # (It is important that we can reference the block before a given one)
        # It's vital that we call this when the Blockchain object is instantiated
        # (We don't want the user to worry about this genesis block being created)
        self.construct_block("Genesis Coin", nonce = 0, prev_hash = 0)

    def construct_block(self, name, nonce=0, prev_hash=0):
        # We want to initialize a new Block
        # The index that this block is stored at the back of the chain (the last index)
        # prev_hash is passed by the caller method
        # completed_transactions are then 
        new_block = block.Block(name,
                                len(self.chain),
                                nonce,
                                prev_hash,
                                self.completed_transactions)
        
        # Now that the block has been created, we want that to be stored in the chain.
        self.chain.append(new_block)
        
        return new_block

    
    def check_validity(curr_block: block.Block, prev_block: block.Block):
        # In order to maintain the integrity of our blockchain, we need to check that the hash of every block
        # in the Blockchain is correct.
        # Because any changes to the blockchain can guarentee large changes to the hashes in our blocks,
        # this method makes sure that every block is correctly pointing to the previous block 
        # (and that the hashes are correct)
        # Returns True if everything is validated; returns False otherwise
        if prev_block.index + 1 != curr_block.index:
            return False

        elif prev_block.calculate_hash != curr_block.prev_hash:
            return False

        elif not Blockchain.verifying_proof(curr_block.nonce, prev_block.nonce):
            return False

        elif curr_block.timestamp <= prev_block.timestamp:
            return False

        return True

    
    def add_transaction(self, name, sender, recipient, quantity):
        # adds a new transaction to the back of the list of self.completed_transactions
        # {sender, recipient, quantity}
        self.completed_transactions.append({
                                    'name': name,
                                    'sender': sender,
                                    'recipient': recipient,
                                    'quantity': quantity,
                                })
    

    def proof_of_work(last_proof):
        # A Proof of Work prevents abuse in the Blockchain (such as spamming the Blockchain and easily mining Blocks)
        # Returns a number that is solved after verifying the proof (see verifying_proof for more details)
        nonce = 0
        while Blockchain.verifying_proof(nonce, last_proof) == False:
            nonce += 1
        
        return nonce

    
    def verifying_proof(last_proof, proof):
        # An example of this situation for verifying the proof: 
        #    does hash(last_proof, proof) contain 4 leading zeroes?

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


    def mine(self, name, miner_receiver):
        # The mine method does 3 essential things:
        # 1.) Adds the transaction with the information of who the receiver is
        # 2.) Does the proof of work
        # 3.) Creates the Block object

        # Add the transaction first
        self.add_transaction(   name,
                                "0",  #it implies that this node has created a new block
                                miner_receiver,
                                1,  #creating a new block (or identifying the proof number) is awarded with 1
                            )

        # All the security and integrity-maintaining actions are performed after the mining process.
        last_block = self.last_block

        last_nonce = last_block.nonce
        nonce = Blockchain.proof_of_work(last_nonce)
        print(nonce)
        if nonce != 0:
            # Mine the block after successfully verifying the transaction is valid.
            print("{Note from miner}....Success!")
            last_hash = last_block.calculate_hash
            block = self.construct_block(nonce, last_hash)
        else:
            print("{Note from miner}....Failure to mine!")
        return vars(block)


    def create_node(self, address):
        # In the event that we have a new node that wants to connect to our blockchain network,
        # we can add them to our list of nodes here.
        self.nodes.add(address)


    def obtain_block_object(block_data):
        # Returns the block object given the data that we need to retrieve it.

        return block.Block(
            block_data['name'],
            block_data['index'],
            block_data['nonce'],
            block_data['prev_hash'],
            block_data['transactions'])