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
        self.nonce = nonce
        self.prev_hash = prev_hash
        self.transaction = transaction
        self.timestamp = (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

    
    def calculate_hash(self):
        block_string = "{}{}{}{}{}{}".format(
                                              self.name, self.index, self.nonce,
                                              self.prev_hash, self.transaction,
                                              self.timestamp)
        encoded_string = block_string.encode()
        hashed_encoded_string = hashlib.sha256(encoded_string)
        hexadecimal_hash = hashed_encoded_string.hexdigest()
        return hexadecimal_hash


    def __repr__(self):
        return "{} - {} - {} - {} - {} - {}".format(self.name, self.index,                                                                       self.nonce,
                                                    self.prev_hash, self.transaction,
                                                    self.timestamp)