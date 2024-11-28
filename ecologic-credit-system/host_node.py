from blockchain import *
from time import time
import hashlib
import json
import requests
import socket

from uuid import uuid4
from flask import Flask, jsonify, request, send_file

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/chain', methods=['GET'])
def full_chain():
    """
    Retrieve the entire blockchain
    """
    response = {
        'chain': [block.__dict__ for block in blockchain.chain],
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """
    Create a new transaction to add to the mempool
    """
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    transaction = Transaction(
        sender=values['sender'],
        recipient=values['recipient'],
        value=values['amount'],
        date=utils.get_time(),  # Use current time for the transaction
        message="Example transaction",
        signature="FakeSignature",  # In a real blockchain, this would be a cryptographic signature
        vk="FakeVerificationKey"  # In a real blockchain, this would be a public key
    )

    if blockchain.add_transaction(transaction):
        response = {'message': f'Transaction will be added to the mempool'}
        return jsonify(response), 201
    else:
        return 'Invalid transaction', 400

@app.route('/mine', methods=['GET'])
def mine():
    """
    Mine a new block by taking transactions from the mempool
    """
    if len(blockchain.mempool) == 0:
        return 'No transactions to mine', 400

    # Create a new block from transactions in the mempool
    new_block = blockchain.new_block()

    # Add the new block to the chain if it is valid
    try:
        blockchain.extend_chain(new_block)
    except InvalidBlock:
        return 'Invalid block', 400

    response = {
        'message': "New Block Forged",
        'index': new_block.index,
        'transactions': [trans.__dict__ for trans in new_block.transactions],
        'previous_hash': new_block.previous_hash,
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    """
    Register new nodes in the network
    """
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    """
    Consensus algorithm to resolve conflicts
    """
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': [block.__dict__ for block in blockchain.chain]
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': [block.__dict__ for block in blockchain.chain]
        }

    return jsonify(response), 200

# @app.route('/postman-collection', methods=['GET'])
# def get_postman_collection():
#     """
#     Provide a Postman collection JSON file for easy API testing
#     """
#     collection = {
#         "info": {
#             "name": "Blockchain API",
#             "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
#         },
#         "item": [
#             {
#                 "name": "Mine a New Block",
#                 "request": {
#                     "method": "GET",
#                     "header": [],
#                     "url": {
#                         "raw": "{{base_url}}/mine",
#                         "host": ["{{base_url}}"],
#                         "path": ["mine"]
#                     }
#                 }
#             },
#             {
#                 "name": "Create a New Transaction",
#                 "request": {
#                     "method": "POST",
#                     "header": [
#                         {
#                             "key": "Content-Type",
#                             "value": "application/json"
#                         }
#                     ],
#                     "body": {
#                         "mode": "raw",
#                         "raw": "{\n  \"sender\": \"address1\",\n  \"recipient\": \"address2\",\n  \"amount\": 10\n}"
#                     },
#                     "url": {
#                         "raw": "{{base_url}}/transactions/new",
#                         "host": ["{{base_url}}"],
#                         "path": ["transactions", "new"]
#                     }
#                 }
#             },
#             {
#                 "name": "View Full Blockchain",
#                 "request": {
#                     "method": "GET",
#                     "header": [],
#                     "url": {
#                         "raw": "{{base_url}}/chain",
#                         "host": ["{{base_url}}"],
#                         "path": ["chain"]
#                     }
#                 }
#             }
#         ]
#     }
#     # Convert the collection to JSON and return as a file
#     with open('blockchain_postman_collection.json', 'w') as f:
#         json.dump(collection, f, indent=4)
#     return send_file('blockchain_postman_collection.json', as_attachment=True)

if __name__ == '__main__':
    # Get the local IP address to bind the Flask server
    recipient = socket.gethostbyname(socket.gethostname())
    app.run(host=recipient, port=5000)

    
