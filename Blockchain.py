import json
import datetime
import hashlib
import binascii
from typing import List, Dict, Any
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from Block import Block
from User import User


class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.pending_transactions = []
        self.users: List[User] = []
        self.sumHash = 0
        self.create_block("begin")

        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        self.signer = PKCS1_v1_5.new(private_key)
        self.identity = binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')

    def create_block(self, data, nonce: int = 0, timestamp: datetime = datetime.datetime.now(), transactions: list = []):
        block = Block(self.sumHash, data,len(self.chain)+1, nonce, timestamp,transactions)
        self.pending_transactions = []
        self.chain.append(block)
        toCode = json.dumps(block.to_dict(), sort_keys=1).encode()
        self.sumHash = hashlib.sha3_512(toCode).hexdigest()
        return block

    @property
    def show_last_block(self):
        return self.chain[-1]

    def validation(self):
        block_index = len(self.chain) - 1
        while block_index > 0:
            if self.chain[block_index].prev_hash != self.chain[block_index - 1].hash_block():
                return False
            block_index -= 1
        return True

    def addUser(self, user):
        self.users.append(user)

    def addUsers(self, users):
        self.users.extend(users)

    def sign(self, message):
        h = SHA.new(message.encode('utf8'))
        return binascii.hexlify(self.signer.sign(h)).decode('ascii')

#Transactions

    def new_transaction(self, sender, recipient, coinID):
        transaction = {
            'sender': sender.identity,
            'recipient': recipient.identity,
            'coinID': coinID,
            'signature': sender.sign(str(sender.identity) + str(recipient.identity) + str(coinID))
        }

        if self.checkTransaction(transaction):
            self.pending_transactions.append(transaction)
        return self.show_last_block.id + 1

    def updateTransactions(self, transactions):
        for tr in transactions:
            if self.checkTransaction(tr):
                self.pending_transactions.append(tr)
                
    def checkWallet(self, userID):
        owned = []
        for block in self.chain:
            for transaction in block.transactions:
                if transaction['recipient'] == userID:
                    coinID = int(transaction['coinID'])
                    if coinID not in owned:
                        owned.append(coinID)
                if transaction['sender'] == userID:
                    coinID = int(transaction['coinID'])
                    if coinID in owned:
                        owned.remove(coinID)
        print('Owned coins' + str(owned)+ '\n')
        return owned

    def checkTransaction(self, transaction):
        coinID = int(transaction['coinID'])
        owned = self.checkWallet(transaction['sender'])
        if coinID in owned:
            for ordered in self.pending_transactions:
                if ordered["coinID"] == coinID:
                    return False
            return True
        else:
            return False

    def generateCoins(self):
        i=0
        for user in self.users:
            i = i+1
            coin = {
            'sender': self.identity,
            'recipient': user.identity,
            'coinID': i,
            'signature': self.sign(str(self.identity) + str(user.identity) + str(i))
            }
            self.pending_transactions.append(coin)
      
        self.create_block("begin",transactions= self.pending_transactions)
        self.coinCounter = 4 

    def validateSignature(self, identity, transaction):
        pubkey = RSA.importKey(binascii.unhexlify(identity))
        verifier = PKCS1_v1_5.new(pubkey)
        message = str(transaction['sender']) + str(transaction['recipient']) + str(transaction['coinID'])
        h = SHA.new(message.encode('utf8'))
        return verifier.verify(h, binascii.unhexlify(transaction['signature']))

    def checkCurrentBlock(self):
        for tr in self.pending_transactions:
            if not self.validateSignature(tr['sender'], tr):
                return False
        return True


    def checkBlock(self, block: Block):
        for tr in block.transactions:
            if not self.validateSignature(tr['sender'], tr):
                return False
        return True

    def proof_of_work(self):
        proof = 0
        while self.valid_proof(self.sumHash, proof) is False:
            proof += 1
            return -1

        return proof
        
    def valid_proof(self, last_hash, proof, difficulty=5):
        guess = (str(last_hash) + str(proof)).encode()
        guess_hash = hashlib.sha3_512(guess).hexdigest()
        if guess_hash[:difficulty] == '0' * difficulty:
            self.guess_hash = guess_hash
            print(guess_hash)
            return guess_hash
        else:
            return -1