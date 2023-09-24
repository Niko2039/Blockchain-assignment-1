# Imports
import hashlib
import json

# Blockchain class
class Blockchain:

    # Constructor
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        # Create genesis block
        self.new_block(previous_hash=1, proof=100)

    # Create new block
    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': ..., 
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    # New transaction
    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return self.last_block['index'] + 1
    
    # Hash block
    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    # Proof of work
    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    # Validate proof
    def valid_proof(self, last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
    
    # Return last block
    @property
    def last_block(self):
        return self.chain[-1]

    # Consensus algorithm
    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)
        for node in neighbours:
            response = ... # request chain from node
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
        if new_chain:
            self.chain = new_chain
            return True
        return False

    # Validate blockchain
    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            # Check hash linkage
            if block['previous_hash'] != self.hash(last_block):
                return False
            # Check proof of work
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            last_block = block
            current_index += 1
        return True
    
    # Consensus
    def consensus(self):
        ...

# Merkle Tree
class MerkleTree:
    
    def __init__(self):
        self.tx_hashes = []
        self.root_hash = None
    
    def add_tx(self, tx):
        tx_hash = hashlib.sha256(json.dumps(tx).encode()).hexdigest()
        self.tx_hashes.append(tx_hash)
        if len(self.tx_hashes) > 1:
            self.update_root_hash()
    
    def update_root_hash(self):
        tx_hash_list = self.tx_hashes.copy()
        temp_hashes = []
        # Calculation
        while len(tx_hash_list) > 1:
            # Hash pairs
            for i in range(0, len(tx_hash_list)-1, 2):
                tx_1 = tx_hash_list[i]
                if i+1 >= len(tx_hash_list):
                    tx_2 = tx_hash_list[i]
                else:
                    tx_2 = tx_hash_list[i+1]
                temp_hash = hashlib.sha256((tx_1 + tx_2).encode()).hexdigest()
                temp_hashes.append(temp_hash)
            # Update
            if len(tx_hash_list) % 2 == 1: 
                temp_hashes.append(tx_hash_list[-1])
            tx_hash_list = temp_hashes.copy()
            temp_hashes = []
        self.root_hash = tx_hash_list[0]

# Driver code
blockchain = Blockchain()
merkle = MerkleTree()

# Add transactions
tx1 = {'from': 'Alice', 'to': 'Bob', 'amount': 10}
blockchain.new_transaction(tx1['from'], tx1['to'], tx1['amount'])
merkle.add_tx(tx1)

tx2 = {'from': 'Bob', 'to': 'Charlie', 'amount': 5}
blockchain.new_transaction(tx2['from'], tx2['to'], tx2['amount']) 
merkle.add_tx(tx2)

# Mine block
last_block = blockchain.last_block
last_proof = last_block['proof']
proof = blockchain.proof_of_work(last_proof)

# Get Merkle root
merkle_root = merkle.root_hash

# Add block    
block = blockchain.new_block(proof, merkle_root)

print('Block successfully mined!')
print(block)