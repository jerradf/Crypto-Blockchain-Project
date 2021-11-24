# blockchain.py
# Author: Jerrad Flores

# This is a Python interpretation of a cryptocurrency Blockchain
# For all of our cryptocurrencies, we are going to assume a continuously producing amount of coin (no limit)

import block
import hashlib
import time


class Blockchain:
    
    def __init__(self, name):
        self.name = name
        self.chain = []
        self.transactions = []
        self.nodes = set()
        self.construct_genesis_block()
        self.bought = {}
        self.sold = {}
        self.in_circulation = {}
        self.last_block = self.chain[-1]


    def construct_genesis_block(self):
        self.construct_block("Genesis Coin", nonce = 0, prev_hash = 0)


    def construct_block(self, name, nonce, prev_hash):
        new_block = block.Block(name,
                                len(self.chain),
                                nonce,
                                prev_hash,
                                self.transactions)
        self.chain.append(new_block)
        
        return new_block


    def add_transaction(self, name, sender, recipient, quantity):
        self.transactions.append({
                                    'name': name,
                                    'sender': sender,
                                    'recipient': recipient,
                                    'quantity': quantity,
                                })

    
    def buy(self, sender, receiver, quantity, traded_coin_quantity, coin_name):
      self.add_transaction(coin_name, sender, receiver, quantity)
      self.bought[coin_name] += (quantity/100)
      time.sleep(2)

    
    def sell(self, sender, receiver, quantity, traded_coin_quantity, coin_name):
      self.add_transaction((-1*coin_name), sender, receiver, quantity)
      self.sold[coin_name] += (quantity/100)
      time.sleep(2)


    def value(self, name):
      relation = self.bought[name]/self.sold[name]
      val = (pow(1.01, relation)) - 1
      return val
      

    def check_validity(self, curr_block: block.Block, prev_block: block.Block):
        if curr_block.timestamp <= prev_block.timestamp:
            return False
        return True


    def verifying_proof(proof, last_proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


    def proof_of_work(last_proof):
        nonce = 0
        while Blockchain.verifying_proof(nonce, last_proof) == False:
            nonce += 1
        return nonce


    def mine(self, quantity, name, miner_receiver):
            self.add_transaction(   name,
                                    "0",
                                    miner_receiver,
                                    quantity, 
                                )
            last_block = self.last_block
            last_nonce = last_block.nonce
            nonce = Blockchain.proof_of_work(last_nonce)
            block = None
            time.sleep(quantity)
            if nonce != 0:
                last_hash = last_block.calculate_hash
                block = self.construct_block(self.name, nonce, last_hash)
                if (self.check_validity(block, last_block) == False):
                  block = None
                  self.chain.pop()
                else:
                  self.in_circulation[name] += quantity
            return block


    def create_node(self, address):
        self.nodes.add(address)