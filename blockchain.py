# blockchain.py
# Author: Jerrad Flores

# This is a Python interpretation of a cryptocurrency Blockchain
# For all of our cryptocurrencies, we are going to assume a continuously producing supply of coin (no limit)
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
        self.last_block = self.chain[-1]
        # NEW PROPERTIES (9/7): These will allow the blockchain to simply maintain the value (formula shown in new method below)
        self.bought = {}
        self.sold = {}

    
    # NEW METHOD (9/7)
    # This will allow the user to BUY coins for another coin.
    # It is not the job of the blockchain to maintain the user's balances (decentralized); it is only the job of the blockchain to perform the action and keep a record of the transaction.
    def buy(self, sender, receiver, quantity, traded_coin_quantity, coin_name):
      # received coin is going to be the added transaction in this case (becasue this is going to gain the crypto rather than gaining a crypto (they are "losing" a dollar), so we want to keep track of the crypto)
      self.add_transaction(coin_name, sender, receiver, quantity)
      self.bought[coin_name] += quantity
      time.sleep(2)

    
    # NEW METHOD (9/7)
    # This will allow the user to SELL coins for another coin.
    # It is not the job of the blockchain to maintain the user's balances (decentralized); it is only the job of the blockchain to perform the action and keep a record of the transaction.
    def sell(self, sender, receiver, quantity, traded_coin_quantity, coin_name):
      # Traded coin is going to be the added transaction in this case (becasue this is going to take away the crypto rather than gaining a crypto (they are "gaining" a dollar), so we want to keep track of the crypto)
      self.add_transaction((-1*coin_name), sender, receiver, quantity)
      self.sold[coin_name] += quantity
      time.sleep(2)


    def construct_genesis_block(self):
        self.construct_block("Genesis Coin", nonce = 0, prev_hash = 0)


    def construct_block(self, name, nonce=0, prev_hash=0):
        new_block = block.Block(name,
                                len(self.chain),
                                nonce,
                                prev_hash,
                                self.transactions)
        self.chain.append(new_block)
        
        return new_block

    

    def check_validity(curr_block: block.Block, prev_block: block.Block):
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
        self.transactions.append({
                                    'name': name,
                                    'sender': sender,
                                    'recipient': recipient,
                                    'quantity': quantity,
                                })
    

    def proof_of_work(last_proof):
        nonce = 0
        while Blockchain.verifying_proof(nonce, last_proof) == False:
            nonce += 1
        
        return nonce

    
    def verifying_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


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
        return block


    # NEW METHOD (9/7)
    # The actual method for determining the value of a crypto is based on the overall demand for the market and the overall supply of the crypto. In a situation with crypto, the basic relationship is: value increases as more is bought, and value decreases as more is sold.
    # We want to form a linear relationship with a very steep slope to simulate this smaller value slowly increasing as the amout of coin bought has increased.
    # The slop is going to be the (crypto bought / crypto sold).
    # The formula that will demonstrate this perfectly is:
    # ((1 / 50000000) * (crypto bought / crypto sold)) + .00000000005(crypto bought / crypto sold)
    def value(self, name):
      relation = self.bought[name]/self.sold[name]
      return ((1/50000000)*relation) + (.00000000005*relation)


    def create_node(self, address):
      self.nodes.add(address)