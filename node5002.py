# Description
# This is a code for node 5002. This program allows node 5001 to be added to the blockchain network.




import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse



# ///
# build blockchain network
class Blockchain:
    
    # initialize
    def __init__(self): 
        self.chain = []
        self.transactions = []
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes = set()
        
        
        
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        self.transactions = []
        self.chain.append(block)
        
        return block
        
    
    
    
    # get previous block in the chain
    def get_previous_block(self): 
        
        return self.chain[-1]
    
    
    
    # solve mathematical problem to mine a block
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            
            if hash_operation[:4] == '0000': # POW until finding mathematical solution starting with 0000
                                             # In Bitcoin network, the number of zeros change every 2016 blocks aka difficulty adjustment 
                                             # In this program, no difficulty adjustment
                check_proof = True
            else:
                new_proof += 1
            
        return new_proof
    
    
    
    
    # encode block using sha 256 function
    def hash(self, block): 
        encoded_block = json.dumps(block, sort_keys = True).encode()
        
        return hashlib.sha256(encoded_block).hexdigest()
    
    
    
    # check whether chain is valid
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        
        while block_index < len(chain):
            block = chain[block_index]
            
            # check whether previous hash matches with hash of previous block
            if block['previous_hash'] != self.hash(previous_block):
                
                return False
            
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            
            # check whether mathematical solution found is correct
            if hash_operation[:4] != '0000':
                
                return False
            
            previous_block = block
            block_index += 1
            
        return True
            
    
    
    
    
    # append a block with a transaction. In Bitcoin network, a block contains multiple transactions
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
        
        previous_block = self.get_previous_block()
        
        return previous_block['index'] + 1 
    
    
    
    
    # connect network
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        # address = 'http://127.0.0.1:5000/'
        
        
        
        
    # when mining occur at multiple nodes at the same time. Longest chain wins
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                
                if length > max_length and is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        
        if longest_chain:
            self.chain = longest_chain
        
            return True # return will break out nested loops
        
        return False
# ///





    
    
# ///    
# mine blockchain
# create a web app
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False




# create an address for the node on port 5000 meaning node 5000
node_address = str(uuid4()).replace('-', '')



# create a blockchain network
blockchain = Blockchain()




# mine a new block
@app.route("/mine_block", methods=['GET'])

def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender = node_address, receiver = 'Receiver 2', amount = 7)
    block = blockchain.create_block(proof, previous_hash)
    
    
    response = {'message': 'Success on mining a new block',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    
    return jsonify(response), 200





# get the full blockchain
@app.route("/get_chain", methods=['GET']) # GET: nothing needed to get something. POST: create or post something to get something

# download blockchain ledger
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    
    return jsonify(response), 200



# check if the blockchain is valid
@app.route("/is_valid", methods=['GET'])

def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    
    if is_valid:
        response = {'message': 'The blockchain is valid.'}
    
    else:
        response = {'message': 'The blockchain is not valid.'}
        
        return jsonify(response), 200




# add a new transaction to the blockchain
@app.route("/add_transaction", methods=['POST'])

def add_transaction():
    json = request.get_json() # json: dictionary
    transaction_keys = ['sender', 'receiver', 'amount']
    
    if not all (key in json for key in transaction_keys):
        
        return 'Some elements of the transaction are missing.', 400    
    
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = {'message': f'This transaction will be added to Block {index}.'}
    
    return jsonify(response), 201
# ///




# ///
# decentralize the blockchain meaning allowing other nodes to be part of the network
# connect new nodes
@app.route("/connect_node", methods=['POST'])

def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    
    if node is none:
        
        return "No node", 400
    
    for node in nodes:
        blockchain.add_node(node)
        
    response = {'message': 'All the nodes are now connected. The blockchain network now contains the following nodes:',
                'total_nodes': list(blockchain.nodes)}
        
    return jsonify(response), 201




# replace the chain with the longest chain if mining at different nodes occur at the same time
@app.route("/replace_chain", methods=['GET'])

def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    
    if is_chain_replaced:
        response = {'message': 'The nodes had different chains, so the chain was replaced by the longest ones.',
                    'new_chain': blockchain.chain}
    
    else:
        response = {'message': 'All good. The chain is the largest one.',
                    'actual_chain': blockchain.chain}
        
        return jsonify(response), 200



# run the app
app.run(host='0.0.0.0', port = 5002) # port number represents node number, for example, node 5002


# ///