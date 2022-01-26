from Blockchain import Blockchain
from Block import Block
from User import User
import json
import binascii
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from queue import Queue
from threading import Thread, Event

blockchain = Blockchain()

#Users generation

users =[]
users.append(User('Sari'))
users.append(User('Hubert'))
users.append(User('Adam'))
users.append(User('Filip'))

proposed_block = None
transaction_list = []

def display_blockchain():
    return json.dumps(blockchain.chain, default=Block.to_dict)


def create_block(data="", nonce=0):
    previous_block = blockchain.show_last_block()
    prev_hash = previous_block.hash_block()
    block = blockchain.create_block(prev_hash, data, nonce)
    hashed_block = block.hash_block()
    date = json.dumps(block.timestamp, default=str)
    response = {'message': 'Created block',
                'previous_hash': block.prev_hash,
                'nonce': block.nonce,
                'data': block.block_data,
                'timestamp': date,
                'hashblock': hashed_block,}

    return json.dumps(response)


def userThread(u :User, b):
    u.updateTransactions(transaction_list)
    global flag
    global proposed_block
    global proof
    while flag:
        b = u.proofofwork()
        if b != -1:
            proof = b
            flag = False
    if b == -1:
        if u.validateBlock(proposed_block) and u.valid_proof(transaction_list, u.bcm.sumHash, proof):
            u.addBlock(proposed_block)
            return print("user " + u.name +  " potwierdza")
        else:
            return print("bład user "  + u.name)
    proposed_block = u.proposeBlock(b)

if __name__ == '__main__':
    blockchain.addUsers(users)
    blockchain.checkWallet(users[0].identity)
    blockchain.checkWallet(users[1].identity)
    blockchain.checkWallet(users[2].identity)
    blockchain.checkWallet(users[3].identity)

    blockchain.generateCoins()


    blockchain.checkWallet(blockchain.users[0].identity)
    blockchain.checkWallet(blockchain.users[1].identity)
    blockchain.checkWallet(blockchain.users[2].identity)
    blockchain.checkWallet(blockchain.users[3].identity)

    
    blockchain.new_transaction(blockchain.users[0], blockchain.users[1], 1)


    blockchain.checkWallet(blockchain.users[0].identity)
    blockchain.checkWallet(blockchain.users[1].identity)
    blockchain.checkWallet(blockchain.users[2].identity)
    blockchain.checkWallet(blockchain.users[3].identity)

    thread1 = Thread(target=userThread(), args=(users[0],-1))
    thread2 = Thread(target=userThread(), args=(users[1],-1))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    random = Crypto.Random.new().read
    rsa = RSA.generate(1024, random)
    pub = binascii.hexlify(rsa.publickey().exportKey(format='DER')).decode('ascii')

    print(blockchain.validateSignature(blockchain.users[0].identity, blockchain.pending_transactions[0]))
    
    blockchain.create_block(blockchain.proof_of_work())
    print(blockchain.checkBlock(blockchain.chain[0]))

