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
    
    def get_balance(self, vk_hash):
        """
        Returns the balance associated to the verifying key hash in parameters.
        A self transaction is considered to be a creation of value
        :param vk_hash:
        :return: Int
        """
        balance = 0
        memo = []
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.hash() not in memo:
                    memo.append(transaction.hash())
                    if transaction.author == vk_hash:
                        # Transaction sent by vk_hash
                        if transaction.dest == vk_hash:
                            # Transaction with itself (creation of funds)
                            balance += int(transaction.value)  # Add the transaction value to the balance
                        else:
                            # Transaction to another user
                            balance -= int(transaction.value)  # Subtract the transaction value from the balance
                    elif transaction.dest == vk_hash:
                        # Transaction received by vk_hash
                        balance += int(transaction.value)  # Add the transaction value to the balance
        return balance

    def add_transaction(self, transaction):
        """
        Add a new transaction to the mempool. Return True if the transaction is valid and not already in the mempool.
        *We also assert that the message in the transaction is valid. and that the transaction is possible according to the suer's balance
        :param transaction:
        :return: True or False
        """
        #* a list of hash depicting the admin users
        admin_list = config.admin_list

        if transaction in self.mempool:
            return False
        
        if transaction.message==None or transaction.date==None or transaction.author==None or transaction.vk==None or transaction.signature==None or transaction.dest==None or transaction.value==None:
            return False
        
        if not transaction.verify():
            return False
        
        if utils.str_to_time(transaction.date) > utils.str_to_time(utils.get_time()):
            return False
        
        #* assert that the value and destination are valid
        val_pattern = r"^[-+][0-9]+$"
        if not re.match(val_pattern, transaction.value):
            return False
            
        dest_pattern = r"^[0-9a-fA-F]{64}$"
        if not re.match(dest_pattern, transaction.dest):
            return False
        
        #* 
        if not transaction.author in admin_list:
            sender_balance = self.get_balance(transaction.author)
            #* check that the author has enough credit to give some to another user
            if sender_balance <= abs(int(transaction.value)):
                return False
            #* prevent the author from giving himself credit
            if transaction.author == transaction.dest and transaction.value[0]=="+":
                return False
            #* prevent teh author from stealing money to another user
            if transaction.author != transaction.dest and transaction.value[0]=="-":
                return False

        
        self.mempool.append(transaction)
        return True
    
    def get_transaction_history(self, vk_hash):
        """
        Returns the transaction history for a verification key hash
        :param vk_hash:
        :return: list of transactions
        """
        transactions = []
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.author == vk_hash:
                    # Transaction sent by vk_hash
                    if transaction.dest == vk_hash:
                        # Transaction with theyselves (creation or suppression of credits)
                        transactions.append([
                            transaction.data,
                            transaction.message,
                            transaction.author[:6] + '...',
                            transaction.dest[:6] + '...',
                            transaction.value,
                            transaction.value
                        ])
                    else:
                        # Transaction to another user
                        transactions.append([
                            transaction.data,
                            transaction.message,
                            transaction.author[:6] + '...',
                            transaction.dest[:6] + '...',
                            transaction.value,
                            utils.inv_sign(transaction.value)
                        ])
                elif transaction.dest == vk_hash:
                    # Transaction received by vk_hash
                    transactions.append([
                        transaction.data,
                        transaction.message,
                        transaction.author[:6] + '...',
                        transaction.dest[:6] + '...',
                        transaction.value,
                        transaction.value
                    ])

        transactions.sort(key=lambda x: x[0])

        return transactions

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

        for transaction in transactions:
            self.mempool.remove(transaction)

        return new_block

    def extend_chain(self, block):
        """
        Add a new block to the chain if it is valid (index, previous_hash, proof).
        :param block: A block
        :raise InvalidBlock if the block is invalid
        """
        if (block.index == self.last_block.index + 1 
            and block.previous_hash == self.last_block.hash()):

            self.chain.append(block)

        else:
            print(block.index > self.last_block.index)
            print(block.previous_hash == self.last_block.hash())
            # print(block.proof)
            raise InvalidBlock

    def __str__(self):
        """
        String representation of the blockchain
        :return: str
        """
        string = '-----------Blockchain-----------'
        for block in self.chain:
            string+= '\n' + str(block)
        if config.show_mempool:
            string+= '\n-----------Mempool-----------'
            for trans in self.mempool:
                string+= '\n' + str(trans)
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


def merge_test():
    print('-----------merge_test-----------')
    from ecdsa import SigningKey
    blockchain = Blockchain()
    sk = SigningKey.generate()
    for i in range(100):
        t = Transaction(f"Message {i}")
        t.sign(sk)
        blockchain.add_transaction(t)

    blockchain2 = Blockchain()
    sk2 = SigningKey.generate()
    for i in range(100):
        t = Transaction(f"Message {i}")
        t.sign(sk2)
        blockchain2.add_transaction(t)

    for i in range(3):
        b = blockchain.new_block()
        b.mine()
        blockchain.extend_chain(b)

    for i in range(2):
        b = blockchain2.new_block()
        b.mine()
        blockchain2.extend_chain(b)

    blockchain.merge(blockchain2)
    blockchain2.merge(blockchain)

    for i in range(2):
        b = blockchain.new_block()
        b.mine()
        blockchain.extend_chain(b)

    for i in range(4):
        b = blockchain2.new_block()
        b.mine()
        blockchain2.extend_chain(b)

    blockchain.merge(blockchain2)
    blockchain2.merge(blockchain)

    blockchain.log()


def simple_test():
    print('-----------simple_test-----------')
    from ecdsa import SigningKey
    blockchain = Blockchain()
    sk = SigningKey.generate()
    for i in range(100):
        t = Transaction(f"Message {i}")
        t.sign(sk)
        blockchain.add_transaction(t)

    print(blockchain)
    for i in range(3):
        b = blockchain.new_block()
        b.mine()
        blockchain.extend_chain(b)

    print(blockchain)
    print(b.validity())
    print(len(blockchain))

def mon_test():
    print('-----------mon_test-----------')
    from ecdsa import SigningKey
    blockchain = Blockchain()
    sk = SigningKey.generate()

def admin_test():
    print('-----------admin_test-----------')
    from ecdsa import SigningKey
    from utils import hash_str

    blockchain = Blockchain()
    sk_a = SigningKey.generate()
    hash_a = hash_str(sk_a)
    sk_b = SigningKey.generate()
    hash_b = hash_str(sk_b)
    sk_admin = config.sk_admin
    hash_admin = config.admin_list[0]

    for i in range(5):
        t = Transaction(f'Admin - Loose money {i}', '-10')
        t.sign(sk_admin)
        blockchain.add_transaction(t)

    for i in range(5):
        t = Transaction(f'Admin - Gain money {i}', '+3')
        t.sign(sk_admin)
        blockchain.add_transaction(t)

    for i in range(5):
        t = Transaction(f'UserA - Loose Money {i}', '-4')
        t.sign(sk_a)
        blockchain.add_transaction(t)
    
    for i in range(5):
        b = blockchain.new_block()
        b.mine()
        blockchain.extend_chain(b)
        
    print("Expect: -20 0 -35")
    print("a :", blockchain.get_balance(hash_a))
    print("b :", blockchain.get_balance(hash_b))
    print("admin :", blockchain.get_balance(hash_admin))

    for i in range(5):
        t = Transaction(f'Admin gives to A {i}', '+8', hash_a)
        t.sign(sk_admin)
        blockchain.add_transaction(t)
    
    for i in range(2):
        b = blockchain.new_block()
        b.mine()
        blockchain.extend_chain(b)

    t = Transaction("A gives to B", '+7', hash_b)
    t.sign(sk_a)
    print(blockchain.add_transaction(t))

    b = blockchain.new_block()
    b.mine()
    blockchain.extend_chain(b)

    print("Expect: +13 +7 -75")
    print("a :", blockchain.get_balance(hash_a))
    print("b :", blockchain.get_balance(hash_b))
    print("admin :", blockchain.get_balance(hash_admin))

    print(blockchain.get_transaction_history(hash_a))
    print(blockchain.get_transaction_history(hash_b))
    print(blockchain.get_transaction_history(hash_admin))

    print(blockchain)





def fail_test():
    print('-----------fail_test-----------')
    from ecdsa import SigningKey
    from utils import hash_str

    blockchain = Blockchain()
    sk_a = SigningKey.generate()
    hash_a = hash_str(sk_a)
    sk_b = SigningKey.generate()
    hash_b = hash_str(sk_b)
    sk_admin = config.sk_admin
    hash_admin = config.admin_list[0]

    is_fail = False

    # TEST: For empty balances we check transactions
    les_t = []

    t = Transaction('A to admin +', '+15', hash_admin)
    t.sign(sk_a)
    les_t.append(t)

    t = Transaction('B to A +', '+10', hash_b)
    t.sign(sk_a)
    les_t.append(t)

    t = Transaction('A to admin +', '-15', hash_admin)
    t.sign(sk_a)
    les_t.append(t)

    t = Transaction('B to A +', '-10', hash_b)
    t.sign(sk_a)
    les_t.append(t)

    for t in les_t:
        if blockchain.add_transaction(t):
            is_fail = True
            print(t.message)

    # ACTION: Add credit to A and B 
    t = Transaction("admin to A", '+1000', hash_a)
    t.sign(sk_admin)
    blockchain.add_transaction(t)

    t = Transaction("admin to B", '+1000', hash_b)
    t.sign(sk_admin)
    blockchain.add_transaction(t)

    b = blockchain.new_block()
    b.mine()
    blockchain.extend_chain(b)

    print("Expect both 1000")
    print(blockchain.get_balance(hash_a), blockchain.get_balance(hash_b))

    # TEST: For positive balances transfer too big or negative values
    les_t = []

    t = Transaction('A to admin ++', '+1500', hash_admin)
    t.sign(sk_a)
    les_t.append(t)

    t = Transaction('B to A ++', '+1500', hash_a)
    t.sign(sk_b)
    les_t.append(t)

    t = Transaction('A to admin +-', '-15', hash_admin)
    t.sign(sk_a)
    les_t.append(t)

    t = Transaction('B to A +-', '-15', hash_a)
    t.sign(sk_b)
    les_t.append(t)

    for t in les_t:
        if blockchain.add_transaction(t):
            is_fail = True
            print(t.message)
    
    # ACTION: Remove credit to A and B (make it negative) 
    t = Transaction("admin to A", '-2000', hash_a)
    t.sign(sk_admin)
    blockchain.add_transaction(t)

    t = Transaction("admin to B", '-2000', hash_b)
    t.sign(sk_admin)
    blockchain.add_transaction(t)

    b = blockchain.new_block()
    b.mine()
    blockchain.extend_chain(b)

    print("Expect both -1000")
    print(blockchain.get_balance(hash_a), blockchain.get_balance(hash_b))

    # TEST: For negative balances we check transactions
    les_t = []

    t = Transaction('A to admin +', '+15', hash_admin)
    t.sign(sk_a)
    les_t.append(t)

    t = Transaction('B to A +', '+10', hash_a)
    t.sign(sk_b)
    les_t.append(t)

    t = Transaction('A to admin +', '-15', hash_admin)
    t.sign(sk_a)
    les_t.append(t)

    t = Transaction('B to A +', '-10', hash_a)
    t.sign(sk_b)
    les_t.append(t)

    for t in les_t:
        if blockchain.add_transaction(t):
            is_fail = True
            print(t.message)

    # TEST: Give himself credit
    les_t = []

    t = Transaction('A self +', '+150')
    t.sign(sk_a)
    les_t.append(t)

    t = Transaction('B self +', '+150')
    t.sign(sk_b)
    les_t.append(t)

    for t in les_t:
        if blockchain.add_transaction(t):
            is_fail = True
            print(t.message)
    
    # TEST: Identity theft is not a joke Jim!
    les_t = []

    t = Transaction('admin self -', '-150')
    t.sign(sk_a)
    les_t.append(t)

    t = Transaction('B self -', '-150')
    t.sign(sk_a)
    les_t.append(t)


    if is_fail:
        print("========> WARMING: A FAIL OCCURED <========")


if __name__ == '__main__':
    print("Blockchain test")
    # simple_test()
    # merge_test()
    # admin_test()
    # fail_test()
