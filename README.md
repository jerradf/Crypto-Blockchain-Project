# Crypto-Blockchain-Project

The Blockchain stores all the Block inside it's chain.
The Blockchain can remember all the Blocks (the Block can only remember it's specific data only!)
This distinction is important!




The Main Program
When the main program is ran, the only thing that the user has to be concerned with is declaring the blockchain with the name of the blockchain as the parameter. In terms of what is going on here in the background, the Blockchain has to be initialized first. 



What is a Block?
A Block in this program represents a cryptocurrency coin block, with the name of the coin that is represented in this Block, an index to represent where this Block is located within our Blockchain (more on that below), a nonce integer value (the number of zero bits that occur after the block has been hashed. This value will allow for the security of this Block instance (no one can easily modify it; they would have to modify all the other blocks in the blockchain for tampering to properly take effect (more on that below)), a prev_hash value, which represents the calculated_hash of the previous block that was added into the Blockchain (more on how Blocks are added to the Blockchain is detailed below), and a timestamp of when this Block was created (we retrieve the actual time).

The calculate_hash method uses the SHA-256 hashing method (since we are using different data types for our properties of this Block, this is a great hashing method to utilize to prevent any possible errors). This hashing method returns a 256-bit string representing the contents of this Block. We only use this method when we are creating a hash for the Block most recently added to the Blockchain (more on this below).

The __repr__ method returns the original pointer to this Block object into a string format of our desired choice (since the class object, when printed, is simply a pointer to a location in memory).


What is a Blockchain?
During the initialization of the Blockchain, the following are initialized as properties: name of the blockchain, the chain list that keeps track of all the blocks, the list of completed_transactions (there is interesting stuff that goes on with this, more on that later. Just know that the completed_transactions is SEPARATE from the chain, because this is what the user can use to pull up all of the mines that went on with this), along with the set of nodes (we use a set because there must be no duplicates: nodes are the servers/computers/locations that utilize this blockchain. Rather than creating multiple instantiations of this Blockchain, the Blockchain would be instantialized once, with any other servers/computers/locations that want to connect to this blockchain to be added to the set (similar to a bank chain, with various physical bank locations being connected to the chain), construct_genesis() method is called because we want to initialize the first coin (this will always be referred to as the "Genesis Coin" for simplicity), and the last_block, which stores the most recently added block from the chain (this is important when we are verifying our block to be added in the chain during the mining process); when we want to mine the first block, the most recent block would be the Genesis block, and when we mine the second block, the most recent block would be the first block, and so on.

The construct_block method creates a new Block object and adds this block to the chain.

The add_transaction method adds a record of the transaction from the mine that we are executing to our list of transaction dictionaries.

The check_validity method checks to ensure that the most recently added block in the chain is correct (if someone tampered with/ hacked our Blockchain to add one in themselves, this is the way that we check for that.
We check for the previous hash, the index, the timestamp, to see if these all match up correctly (if they are equal to each other). along with the verifying_proof portion of it.

The verifying_proof method encodes our nonce values from the most recently added Block added to the Blockchain, as well as the current nonce value from the Block that wants to be added to the Blockchain. The bits from the previous Block's nonce value is encoded with the current Block's nonce value from an f' string. Hashing is implemented from this encoded value using the hash.hexdigest() method. We use this hexdigest() in encryption-required environments (email applications or server-based environments where security is essential, such as this one). If the hashing of both of these nonce values combined does not contain 4 leading zeroes, this function returns False.

The proof_of_work method runs a continuously running while loop that continuously increases our nonce value. Since the value that results from hashing the previously added Block's nonce value with the current Block's nonce value (calling verifying_proof) is going to result in False a large amount of times, the nonce value will continuously increase by 1 until verifying_proof returns True. The reason why verifying_proof will result in False a large amount of times is because the nonce value in the current Block is vastly different from the nonce value in the previously added Block, so continuously increasing the nonce value by 1 ensures that we are going to have equivalent nonce values throughout our entire Blockchain (we want this to be the case. We could've simply said "self.nonce = last_block.nonce", but this is a great way to practice the use of multi-function hashing techniques that can show how we can have security and integrity in our coin. Not only that, but the user should not worry about any of this information (details regarding the requirements of the main program above). In typical crypto-developer environments, we want this to be a private attribute, but since this cannot be done in Python, the equivalence of nonce values can be easily seen. This is one of the downfalls of developing this portion of the application in Python, and which is why other programming languages such as C++ are utilized for this component).

The mine method does 3 simple actions: 1.) Adds the transaction with the information of who the receiver is by calling add_transaction, 2.) Does the proof_of_work, and 3.) Creates the Block object by calling construct_block. This is where we create the hashing for the previous block (more details on how this is performed above). The order that this occurs is important. We want to add this record transaction to our list of completed_transactions, regardless if this was a failure or success. We then want to verify everything (details above regarding this), and then we want to create that Block object if the nonce value was correctly (if the nonce value is 0, then an internal error has occurred in the verifying_proof step (either the blockchain has been tampered with by the user or an error resulting in a different nonce value somewhere or with the hashing when we created the hash (when we created the previous_block's hash) has occurred). What is returned is the Block object that we created.

The create_node method adds any new Servers/Computers/Locations that want to join our Blockchain network to our set of nodes.