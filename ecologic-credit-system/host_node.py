from blockchain import *
from flask import Flask, jsonify, request
import socket
from transaction import Transaction
import utils

# Instantiate our Node
app = Flask(__name__)

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
    required = ['message', 'value', 'dest']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    transaction = Transaction(
        message=values['message'],
        value=values['value'],
        dest=values['dest'],
    )

    # Add transaction to the mempool
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

@app.route('/chain/validate', methods=['GET'])
def validate_chain():
    """
    Validate the entire blockchain
    """
    is_valid = blockchain.validity()
    response = {
        'valid': is_valid,
        'message': 'The blockchain is valid' if is_valid else 'The blockchain is not valid'
    }
    return jsonify(response), 200

@app.route('/chain/merge', methods=['POST'])
def merge_chain():
    """
    Merge with another blockchain if it is longer and valid
    """
    values = request.get_json()

    # Check if the required field 'chain' is present
    if 'chain' not in values:
        return 'Missing chain data', 400

    # Create a temporary blockchain from the received data
    other_chain = Blockchain()
    other_chain.chain = [Block(**block_data) for block_data in values['chain']]

    # Attempt to merge the blockchains
    if blockchain.merge(other_chain):
        response = {'message': 'Blockchain merged successfully'}
    else:
        response = {'message': 'Merge unsuccessful. The provided chain is not longer or not valid.'}
    
    return jsonify(response), 200

if __name__ == '__main__':
    # Get the local IP address to bind the Flask server
    host_ip = socket.gethostbyname(socket.gethostname())
    app.run(host=host_ip, port=5000)
