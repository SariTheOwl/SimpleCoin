import datetime
import hashlib
from typing import List, Dict, Any

from Block import Block


class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.create_block(hashlib.sha256("0".encode()).hexdigest(), "begin")

    def create_block(self, prev_hash, data, nonce: int = 0, timestamp: datetime = datetime.datetime.now()):
        block = Block(prev_hash, data, nonce, timestamp)
        self.chain.append(block)
        return block

    def show_last_block(self):
        return self.chain[-1]

    def validation(self):
        block_index = len(self.chain) - 1
        while block_index > 0:
            if self.chain[block_index].prev_hash != self.chain[block_index - 1].hash_block():
                return False
            block_index -= 1
        return True
