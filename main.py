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

blockchain = Blockchain()

#Users generation

users =[]
users.append(User('Sari'))
users.append(User('Hubert'))
users.append(User('Adam'))
users.append(User('Filip'))


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

    
    random = Crypto.Random.new().read
    rsa = RSA.generate(1024, random)
    pub = binascii.hexlify(rsa.publickey().exportKey(format='DER')).decode('ascii')

    print(blockchain.validateSignature(blockchain.users[0].identity, blockchain.pending_transactions[0]))
    
    blockchain.create_block('blok2')
    print(blockchain.checkBlock(blockchain.chain[0]))

