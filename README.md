## Project Details

### Title: Secure Transaction System

#### This Project is done as part of the Course - CSL7490: Introduction to Blockchain

## About

A public blockchain structure for secure storage, retrieval, and analysis of transactions, implemented in Python (Flask) and SQL for efficient querying

## Objectives 

- Implement a blockchain with the following functionalities:

1. Create at least 10 nodes as miners who are connected to each other.
2. Each Miner is connected to at least 2 users. 
3. Create a wallet which contains private and public keys.
4. Use the hash of the public key as the address of each user’s wallet. 
5. Using digital signatures verify the sender and receiver. 
6. The header of a block in the blockchain should contain: block index,
7. timestamp, previous block hash, and merkle root. 
8. The body of the block should contain the hash of each transaction. 
9. Store the transactions in UTXO format (w.r.t. Bitcoin wallet). 

- Execute the above-described Blockchain, then store the data (transactions) in the database and ask the following queries:

1. Genesis transaction: find the (Genesis) block hash from the transaction hash. 
2. Find the addresses and amounts of the transactions.
3. Show the block information of the block with the hash address of (input the hash of the block).
4. Show the height of the most recent block stored. 
5. Show the most recent block stored. 
6. The average number of transactions per block in the entire Bitcoin blockchain (in your database). 
7. Show a summary report of the transactions in the block with height 6 with two columns <br/>
&nbsp;&nbsp;&nbsp;&nbsp; A. “Number of transactions”: numbers of transactions with inputs. <br/>
&nbsp;&nbsp;&nbsp;&nbsp; B. “Total input Bitcoins”: total inputs’ BTC of transactions with this number of inputs.


### Relavant Documents 

* [Better Readme](https://docs.google.com/document/d/1YpEpInGWa_vDUxZNX3z81Kc8JNtiLQf5JAOQml1_ifM/edit?usp=sharing)


### Execution Steps
- There are following files: 
1.  ```miner-1.py (port 5001)```, ```miner-2.py (port 5002)```, ```user-1.py (port 5005)```, ```user-2.py (port 5006)```
2. Install the libraries mentioned in the import statements
3. Open the terminal and run the following command to start the server and the miner code runs at the port 5001
	
	``` python miner-1.py ```

5. Run the file named ```miner-2.py``` in a new terminal which has a different port No. 5002
6. Files for all the 10 miners to demonstrate can be generated by copying the ```miner-1.py``` and changing the port number for each of the miners. Thus, ```miner-1.py```, ```miner-2.py```, ```miner-3.py```, ```miner-4.py```, ```miner-5.py```, ```miner-6.py```, ```miner-7.py```, ```miner-8.py```, ```miner-9.py```, ```miner-10.py``` can be generated.
7. Similary 20 files for ```user-1.py``` to ```user-20.py``` can be generated by changing the port number for each file of the user

1. Files named ```miner-1.py``` to ```miner-10.py``` are run on different ports to demonstrate 10 miners
2. Files named ```user-1.py``` to ```user-20.py``` are run on different ports to demonstrate 20 users
3. Each user sends the transactions to the miner defined in their code and the miner then broadcasts the transaction to other connected miners

### Methods supported for miners: 

- Mine new blocks
- Add New Transactions
- Register New Miner Nodes
- Get the current chain
- Resolve the chains by choosing the one with longer length
- Broadcast the transaction received from the user to other miner nodes

### Methods supported for users: 

- Add new transactions (which is sent to the intended miner)
- Get current chain

### Functionalities

- A Private key and Public Key is generated for every user (wallet) and the address of the wallet is generated by the Hash of the Public key
- Digital signature mechanism is implemented in the code
- The MerkleTree Class has been implemented with all the necessary steps and the block has been defined as required
- Current transactions ( in other words MemPool is used to store the transactions that are yet to be added to the block)
- The transactions in UTXO format are stored in the list named wallet for all the user files


### Assumptions

- The blockchain is a simple list (storing all the blocks in our blockchain), there is another list to store the transactions for each of the miners as their own copy)
- The blockchain class is responsible for managing the chain. It will store transactions and have some helper methods for adding new blocks to the chain.
- Each block has an index, a timestamp, a list of transactions (or in simple terms, data), a proof (the nonce value), hash of the root of the merkle tree and the hash of the previous block
- Proof of work has been used to implement the consensus algorithm


### Next Steps:

- After Execution of above steps ( the blockchain) 
- Implement the database
- Store the data (transactions) in the database 
- Run the required queries (Refer [here](https://docs.google.com/document/d/1YpEpInGWa_vDUxZNX3z81Kc8JNtiLQf5JAOQml1_ifM/edit?usp=sharing) for a more detailed version)


### Technologies Used

* [Flask](https://flask.palletsprojects.com/en/2.3.x/)
* [MySQL](https://www.mysql.com/)
