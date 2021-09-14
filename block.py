# block.py
# Author: Jerrad Flores

# This is a Python interpretation of a cryptocurrency Block

import hashlib
import time
import datetime

class Block:

    def __init__(self, name, index, nonce, prev_hash, transaction):
        self.name = name
        self.index = index
        self.nonce = 0
        self.prev_hash = prev_hash
        self.transaction = transaction
        self.name = name
        self.timestamp = (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

    
    def calculate_hash(self):
        block_string = "{}{}{}{}{}{}".format(
                                              self.name, self.index, self.nonce,
                                              self.prev_hash, self.transaction,
                                              self.timestamp)

        return hashlib.sha256(block_string.encode()).hexdigest()


    def __repr__(self):
        return "{} - {} - {} - {} - {} - {}".format(self.name, self.index, self.nonce,
                                               self.prev_hash, self.transaction,
                                               self.timestamp)