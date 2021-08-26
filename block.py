# block.py
# Author: Jerrad Flores

# This is a Python interpretation of a cryptocurrency block

import hashlib
import time
import datetime

class Block:

    def __init__(self, name, index, nonce, prev_hash, transactions):
        # self.name is the name of the coin for this specific Block
        self.name = name

        # self.index is going to keep track of where this Block instance
        # is located in the Blockchain
        self.index = index
        
        # self.nonce is the number of zero bits that occur after the block has been hashed.
        # This value will allow for the security of this Block instance (no one can easily modify it;
        # they would have to modify all the other blocks in the blockchain for this to take effect)
        # (For more information: take a look at the proof_of_work in blockchain.py in the Blockchain class.)
        self.nonce = 0

        # self.prev_hash is the hash of the previous block in the Blockchain
        # This will allow for the security of this Block instance (no one can easily modify it)
        # For more information: take a look at the proof_of_work in blockchain.py in the Blockchain class.)         
        self.prev_hash = prev_hash

        # self.completed_transactions has all the transactions that have been completed for this given block, 
        # as well as the total quantity of coin mined for this Block instance.
        # (the transactions will start out as empty but will be modified as more transactions are executed with this Block instance)
        self.completed_transactions = transactions
        
        self.name = name

        # self.timestamp is the time that this Block instance was mined.
        self.timestamp = (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

    
    def calculate_hash(self):
        # Generates the hash of the blocks using the components of the Block instnace. 
        # # The SHA-256 is what we will use to properly obtainin the hashes of the blocks
        # (since we are using different data types for our properties of the Block, this is crucial)
        # Returns a 256-bit string representing the contents of the block.

        block_string = "{}{}{}{}{}{}".format(self.name, self.index, self.nonce,
                                              self.prev_hash, self.data,
                                              self.timestamp)

        return hashlib.sha256(block_string.encode()).hexdigest()


    def __repr__(self):
        # This function will allow us to print the Block with this format (rather than a class object)
        return "{} - {} - {} - {} - {} - {}".format(self.name, self.index, self.nonce,
                                               self.prev_hash, self.completed_transactions,
                                               self.timestamp)