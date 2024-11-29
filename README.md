# Ecologic-credit-system
This is a project aiming at constructing a ecologic credit application using the blockchain. 

A decentralized platform is built to help companies (with associated administrations) to calculate and trade ecologic credits witch can be considered as the impact of a company's activities on the ecosystem, and the algorithm for calculating them can be determined by the platform builder.

More details including the code are discussed below

## Eco-credit

The eco-credit owned can be considered as the environmental impact owned by the company, and its reduction can therefore be considered as the environmental impact of the company.

We want to create a decentralized platform on which eco-credits can be traded: each company can buy eco-credits from the government and other companies, and deduct its own eco-credits based on published data and publicly available algorithms that calculate its environmental impact.

According to our aims, we should clarify the basic rules of the eco-credits:

1. The company reduces its own  eco-credits after a period of time, according to its impact on the environment.
2. Companies can buy eco-credits from the government or companies with eco-credits balances.
3. The government grants each company a certain number of eco-credits per period and allows it to buy additional shares, with the right to penalize eco-credits.

In our case, we propose a more detailed rules as follow pictures (with the calculating algorithm public to be decided )

Eco-credits can be used as a complementary instrument to environment tax, with more flexibility and transparency.

## Tutorial



### Detailed implementation

-----

#### Transaction Module

The `Transaction` module defines the structure and functionality of a transaction. Each transaction represents a message signed with a private key, and the signature can be verified using the corresponding public key. This module allows you to create, sign, verify transactions, and provides utilities for handling transaction data.

- **Transaction Structure**:
  - Each transaction includes the following fields:
    - `message`: The content of the message to be signed.
    - `value`: The transaction value (supports positive or negative values with `±` prefix).
    - `dest`: The destination address (optional, defaults to the author’s address).
    - `date`: The transaction timestamp (uses the current time if not provided).
    - `author`: The hash of the public key, used to identify the transaction’s author.
    - `vk`: The public key (encoded in hexadecimal).
    - `signature`: The signature of the transaction (encoded in hexadecimal).
  - Transactions are JSON-serializable dictionary objects.
- **Core Methods**:
  1. `sign(sk)`: Signs the transaction using a private key.
  2. `verify()`: Verifies the transaction’s signature and author information.
  3. `hash()`: Computes a unique hash for the transaction.
  4. `json_dumps()`: Exports the transaction data in JSON format.
  5. `log(transactions)`: Outputs a formatted log of multiple transactions.
- **Exception Handling**:
  - Custom exception classes `IncompleteTransaction`, `InvalidValue`, and `InvalidDestination` handle errors during transaction creation or validation.

---

#### Block Module

The `Block` module defines the structure and functionality of a blockchain block. A block is a container for transactions and serves as a fundamental unit of the blockchain. The first block in the chain is called the **genesis block**. This module provides mechanisms for creating, linking, validating, and mining blocks in the blockchain.

- **Block Structure**:
  - Each block consists of the following attributes:
    - `index`: The position of the block in the blockchain.
    - `timestamp`: The time the block was created.
    - `transactions`: A list of transaction objects included in the block.
    - `previous_hash`: The hash of the preceding block in the chain.
- **Core Methods**:
  1. `next(transactions)`:Creates a new block linked to the current block, containing the provided transactions.
  2. `hash()`: Computes the SHA256 hash of the block, ensuring consistency by sorting the block’s dictionary representation.
  3. `validity()`: Validates the block by checking transactions, and block constraints.
- **Genesis Block**:
  - If no data is provided, a genesis block is created with:
    - `index = 0`
    - `timestamp = "2023-11-24 00:00:00.000000"`
    - `transactions = []`
    - `previous_hash = "0" * 64`
- **Logging and Debugging**:
  - The `log()` method provides a formatted view of block details, including transactions and links to previous blocks.

---

#### Blockchain Module

The `Blockchain` module implements a blockchain data structure consisting of a sequence of blocks and a **mempool** (a temporary storage area for unconfirmed transactions). It provides methods to manage transactions, create new blocks, validate the blockchain, and merge with other blockchains.

- **Block Structure**:
  - `chain`: A list containing the blocks of the blockchain. The first block is the **genesis block**.
  - `mempool`: A list of unconfirmed transactions awaiting inclusion in a block.
- **Core Methods**:
  1. Transaction Management
     - `add_transaction(transaction)`: Adds a valid transaction to the mempool.
     - `get_transaction_history(vk_hash)`: Retrieves the transaction history for a specific user, identified by their verification key hash.
     - `get_balance(vk_hash)`: Computes the balance of a user based on blockchain transactions.
  2. Block Management
     - `new_block(block=None)`: Creates a new block by selecting transactions from the mempool.
     - `extend_chain(block)`: Adds a block to the blockchain if it is valid.
  3. Validation
     - `validity()` ensures the blockchain is valid by verifying:
       - Blocks are sequential and correctly linked.
       - Transactions in each block are valid and not duplicated.
       - The genesis block is correct.
  4. Merging
     - `merge(other)`: Replaces the blockchain with a longer, valid chain from another blockchain instance.
  5. `validity()`: Validates the block by checking transactions, and block constraints.
- **Logging**:
  - `chain`:The `log()` method prints a detailed view of the blockchain and the mempool.

---

#### Other modules 

- **`config.py`** contains configuration settings and constants for the blockchain system. One can change the basic parameters in this file.
- **`encrypt_data.py`** manages encryption and decryption processes for securing data.
- **`host_node.py`** serves as a script or module for managing the node that interacts with the blockchain network.
- **`interface.py`** defines the user interface or API for interacting with the blockchain system.
- **`utils.py`** provides utility functions used across the other modules.



