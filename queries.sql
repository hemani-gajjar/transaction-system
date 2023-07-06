-- Create the Database to store transactions
CREATE DATABASE IF NOT EXISTS blockchainDB;

-- Use the database
USE blockchainDB;

-- Show the tables in the database
SHOW TABLES;

-- Create the table to store Blocks and Transactions 
-- Assumption: Each block has a one transaction 
-- The table is named as BLock

CREATE TABLE block (index_id int, hash varchar(255), timestamp varchar(255), transactions varchar(255), proof varchar(255), previous_hash varchar(255), merkle_root varchar(255));

-- Display the cloumns of the created table
SHOW COlUMNS FROM block;

-- -- +----------------+--------------+------+-----+---------+-------+
-- | Field          | Type         | Null | Key | Default | Extra |
-- +----------------+--------------+------+-----+---------+-------+
-- | index_id       | int          | YES  |     | NULL    |       |
-- | hash           | varchar(255) | YES  |     | NULL    |       |
-- | timestamp      | varchar(255) | YES  |     | NULL    |       |
-- | transaction_id | varchar(255) | YES  |     | NULL    |       |
-- | proof          | varchar(255) | YES  |     | NULL    |       |
-- | previous_hash  | varchar(255) | YES  |     | NULL    |       |
-- | merkle_root    | varchar(255) | YES  |     | NULL    |       |
-- +----------------+--------------+------+-----+---------+-------+

-- Storing a transaction record in the table
insert into block values(10, 'a73272175a4c33f4ccc4bd6d565d565a824b90e576e8dbebc2634addf8976501', '11:58:50', 'b73272175a4c33f4ccc4bd6d565d565a824b90e576e8dbebc2634addf8976501', 'c73272175a4c33f4ccc4bd6d565d565a824b90e576e8dbebc2634addf8976501', 'd73272175a4c33f4ccc4bd6d565d565a824b90e576e8dbebc2634addf8976501', 'e73272175a4c33f4ccc4bd6d565d565a824b90e576e8dbebc2634addf8976501');

-- Other transactions can be added to the table similarly

-- Display the records in the table 
SELECT * FROM block;

-- 1) Find the (Genesis) block hash from the transaction hash
-- Transaction Hash is named as transaction_id
SELECT hash FROM block WHERE transaction_id = 'b73272175a4c33f4ccc4bd6d565d565a824b90e576e8dbebc2634addf8976d72';

--  +------------------------------------------------------------------+
-- | hash                                                             |
-- +------------------------------------------------------------------+
-- | a73272175a4c33f4ccc4bd6d565d565a824b90e576e8dbebc2634addf8976d72 |
-- +------------------------------------------------------------------+

-- 2) Find the addresses and amounts of the transactions
-- Assumption: One block contains only one transaction

-- Display Address
SELECT hash FROM block;

-- Display Amount of transactions
SELECT COUNT(*) FROM block;

-- +----------+
-- | COUNT(*) |
-- +----------+
-- |       12 |
-- +----------+

-- 3) Show the block information of the block with the hash address of
SELECT * FROM block WHERE hash = 'a73272175a4c33f4ccc4bd6d565d565a824b90e576e8dbebc2634addf8976d73';

-- 4) Show the height of the most recent block stored
SELECT index_id FROM block ORDER BY index_id DESC LIMIT 1;
-- Height of the block = index_id + 1

-- +----------+
-- | index_id |
-- +----------+
-- |       10 |
-- +----------+

-- 5) Show the most recent block stored
SELECT * from block ORDER BY index_id DESC LIMIT 1;

-- 6) The average number of transactions per block in the entire Bitcoin blockchain (in your database)
SELECT AVG(no_of_transactions) FROM block;

-- 7) Show a summary report of the transactions in the block with height 6 with two columns:

-- A. “Number of transactions”: numbers of transactions with inputs.
-- B. “Total input Bitcoins”: total inputs’ BTC of transactions with this number of inputs.

-- Height = 6, index_id = 6

SELECT no_of_transactions, coins FROM block WHERE index_id=6;


