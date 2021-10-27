from Blockchain import Blockchain
from Block import Block
import json

blockchain = Blockchain()


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
    print(display_blockchain())

    print(create_block())
    print(create_block())
    print(create_block())

    print(display_blockchain())
    print(blockchain.validation())

