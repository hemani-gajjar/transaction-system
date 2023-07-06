import datetime
import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4
from urllib.parse import urlparse
import requests
from flask import Flask, jsonify, request
import binascii
from typing import List
import typing
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import base64

# following imports are required by PKI
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

class Blockchain(object):

    def __init__(self, miner):
        self.current_transactions = []
        self.chain = []
        self.miner = miner
        self.wallet = []

        #create the genesis block
        self.new_block(previous_hash = 1, proof = 100) 
        
        # Generate a Private Key
        random = Crypto.Random.new().read
        self.private_key = RSA.generate(1024, random)
        
        # Generate Public Key
        self.public_key = self.private_key.publickey()

        # Use hash of Public Key as address of the wallet
        wallet_address = hashlib.sha256(binascii.hexlify(self.public_key.exportKey(format='DER')).decode('ascii').encode()).hexdigest()
        #a73272175a4c33f4ccc4bd6d565d565a824b90e576e8dbebc2634addf8976d72

    def new_block(self, proof, previous_hash=None):
        #creates a new block and adds it into the chain
        """
        Create a new Block in the Blockchain
        :param proof: <int> The proof given by the proof of work algorithm
        :param previous_hash: (Optional) <str> Hash of previous block
        :param merkle_root: <str> Hash of Root of Merkle Root Tree 
        :return <dict> New Block
        """

        tmp = ["0"]
        mtree = MerkleTree(tmp)

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            'merkle_root': MerkleTree(tmp).getRootHash()
        }

        #Reset the current list of transactions
        self.current_transactions = []

        #append the newly created block to the chain
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        #adds a new transaction to the list of transactions
        """
        Creates a new transaction to go into the next mined block
        :param sender: <str> Address of the sender
        :param recipient: <str> Address of the recipient
        :param amount: <int> Amount
        :return <int> The index of the block that will hold this transaction
        """
        
        self.current_transactions.append({
            'sender' : sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.last_block['index'] + 1

    def encrypt(rsa_publickey,plain_text):
        cipher_text=rsa_publickey.encrypt(plain_text,32)[0]
        b64cipher=base64.b64encode(cipher_text)
        return b64cipher

    def decrypt(rsa_privatekey,b64cipher):
        decoded_ciphertext = base64.b64decode(b64cipher)
        plaintext = rsa_privatekey.decrypt(decoded_ciphertext)
        return plaintext

    def sign(privatekey,data):
        return base64.b64encode(str((privatekey.sign(data,''))[0]).encode())

    def verify(publickey,data,sign):
        return publickey.verify(data,(int(base64.b64decode(sign)),))

    def send_transaction_to_miner(self, sender_public_key):
        miner = self.miner
        signature = sign(self.private_key)
        print("@", signature)
        json_obj = {"signature": signature,"transaction": self.current_transactions, "sender": sender_public_key}
        response = requests.post(f'http://{miner}/handle_transaction', json = json_obj)
        if response.status_code == 200:
            return True
        return False

    @staticmethod
    def hash(block):
        #Hashes a block
        """
        Creates a SHA-256 of a Block
        :param block: <dict> Block
        :return: <str>
        """
        
        # We must make sure that the dictionary is ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True


# Implementing the Merkle Root Tree
class Node:
    def __init__(self, left, right, value: str)-> None:
        self.left: Node = left
        self.right: Node = right
        self.value = value

    @staticmethod
    def hash(val: str)-> str:
        return hashlib.sha256(val.encode('utf-8')).hexdigest()

    @staticmethod
    def doubleHash(val: str)-> str:
        return Node.hash(Node.hash(val))

class MerkleTree:
    def __init__(self, values: List[str])-> None:
        self.__buildTree(values)

    def __buildTree(self, values: List[str])-> None:
        leaves: List[Node] = [Node(None, None, Node.doubleHash(e)) for e in values]
        if len(leaves) % 2 == 1:
            leaves.append(leaves[-1:][0]) # duplicate last elem if odd number of elements
        self.root: Node = self.__buildTreeRec(leaves)

    def __buildTreeRec(self, nodes: List[Node])-> Node:
        half: int = len(nodes) // 2

        if len(nodes) == 2:
            return Node(nodes[0], nodes[1], Node.doubleHash(nodes[0].value + nodes[1].value))

        left: Node = self.__buildTreeRec(nodes[:half])
        right: Node = self.__buildTreeRec(nodes[half:])
        value: str = Node.doubleHash(left.value + right.value)
        return Node(left, right, value)

    def printTree(self)-> None:
        self.__printTreeRec(self.root)

    def __printTreeRec(self, node)-> None:
        if node != None:
            print(node.value)
            self.__printTreeRec(node.left)
            self.__printTreeRec(node.right)

    def getRootHash(self)-> str:
        return self.root.value
    
# instantiate our node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# instantiate the blockchain
blockchain = Blockchain("127.0.0.1:5001")

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)


class Block:

    # Header
    blockNo = 0
    next = None
    hash = None
    nonce = 0
    previous_hash = 0x0
    timestamp = datetime.datetime.now()

    # Body
    data = None

    def __init__(self, data):
        self.data = data

    def hash(self):
        h = hashlib.sha256()
        h.update(
            str(self.nonce).encode('utf-8') + 
            str(self.data).encode('utf-8') + 
            str(self.previous_hash).encode('utf-8') + 
            str(self.timestamp).encode('utf-8') +
            str(self.blockNo).encode('utf-8')
        )

        return h.hexdigest()

    def __str__(self):
        return "Block Hash: " + str(self.hash()) + "\nBlockNo: " + str(self.blockNo) +  "\nBlock Data: " + str(self.data) + "\nHashes: " + str(self.nonce) + "\n------------------"




    
