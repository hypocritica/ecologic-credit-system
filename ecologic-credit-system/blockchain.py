"""
This module contains the class Blockchain. A blockchain is a list of blocks and a mempool.
"""
import json
import random
import config
import utils
from block import Block, InvalidBlock
from transaction import Transaction

import re

class Blockchain(object):
    def __init__(self):
        self.chain = [Block()]
        self.mempool = []

    @property
    def last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        """
        Add a new transaction to the mempool. Return True if the transaction is valid and not already in the mempool.
        *We also assert that the message in the transaction is valid
        :param transaction:
        :return: True or False
        """
        if transaction in self.mempool:
            return False
        
        if transaction.message==None or transaction.date==None or transaction.author==None or transaction.vk==None or transaction.signature==None:
            return False
        
        if not transaction.verify():
            return False
        
        if utils.str_to_time(transaction.date) > utils.str_to_time(utils.get_time()):
            return False
        
        #* assert that the value and destination are valid
        val_pattern = r"^[-+][0-9]+$"
        if not re.match(val_pattern, transaction.value):
            return False
            
        dest_pattern = r"^[0-9a-fA-F]{430}$"
        if not re.match(dest_pattern, transaction.dest):
            return False
            
        
        self.mempool.append(transaction)
        return True
    
    def new_block(self, block=None):
        """
        Create a new block from transactions choosen in the mempool.
        :param block: The previous block. If None, the last block of the chain is used.
        :return: The new block
        """
        if not block:
            block = self.last_block

        transactions = random.sample(self.mempool, min(len(self.mempool), config.blocksize))
        new_block = block.next(transactions)

        return new_block

    def extend_chain(self, block):
        """
        Add a new block to the chain if it is valid (index, previous_hash, proof).
        :param block: A block
        :raise InvalidBlock if the block is invalid
        """
        if (block.index == self.last_block.index + 1 
            and block.previous_hash == self.last_block.hash() 
            and block.valid_proof()):

            self.chain.append(block)

        else:
            print(block.index > self.last_block.index)
            print(block.previous_hash == self.last_block.hash())
            print(block.proof)
            raise InvalidBlock

    def __str__(self):
        """
        String representation of the blockchain
        :return: str
        """
        string = '-----------Blockchain-----------'
        for block in self.chain:
            string+= '\n' + str(block)
        # string+= '\n-----------Mempool-----------'
        # for trans in self.mempool:
        #     string+= '\n' + str(trans)
        return string

    def validity(self):
        """
        Check the validity of the chain.
        - The first block must be the genesis block
        - Each block must be valid
        - Each block must point to the previous one
        - A transaction can only be in one block
        :return: True if the chain is valid, False otherwise
        """
        if self.chain[0].index != 0:
            return False

        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if not current_block.validity():
                return False

            if current_block.previous_hash != previous_block.hash():
                return False

            transactions_hashes = [transaction.hash() for transaction in current_block.transactions]
            for j in range(i - 1, -1, -1):
                previous_block = self.chain[j]
                previous_transactions_hashes = [transaction.hash() for transaction in previous_block.transactions]
                for transaction_hash in transactions_hashes:
                    if transaction_hash in previous_transactions_hashes:
                        return False

        return True

    def __len__(self):
        """
        Return the length of the chain
        :return:
        """
        return len(self.chain)

    def merge(self, other):
        """
        Modify the blockchain if other is longer and valid.
        :param other:
        :return: True if the other chain is longer and valid, False otherwise
        """
        if other.validity() and len(self) < len(other):
            self.chain = other.chain[:]
            
            for block in other.chain:
                for transaction in block.transactions:
                    if transaction not in self.mempool:
                        self.mempool.append(transaction)

            return True

        else:
            return False

    def log(self):
        print(self)
        Transaction.log(self.mempool)

        for b in self.chain:
            b.log()


if __name__ == '__main__':
    print("Blockchain test")
    # simple_test()
    # merge_test()

