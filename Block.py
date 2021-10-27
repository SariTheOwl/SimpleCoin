import hashlib
import datetime
import json


class Block:
    def __init__(self,  prev_hash, block_data, nonce: int = 0, timestamp: datetime = datetime.datetime.now()):
        self.nonce = nonce
        self.block_data = block_data
        self.prev_hash = prev_hash
        self.timestamp = timestamp

    def hash_block(self):
        hashed_block = f"prev_hash={self.prev_hash},nonce={self.nonce},data={self.block_data},timestamp={self.timestamp}"

        return hashlib.sha256(hashed_block.encode()).hexdigest()

    def to_dict(u):
        if isinstance(u, Block):
            dict = {
                "nonce": u.nonce,
                "data": u.block_data,
                "previous hash": u.prev_hash,
                "timestamp": u.timestamp.strftime("%d %b %y")
            }
            return dict
        else:
            type_name = u.__class__.__name__
            raise TypeError("Unexpected type {0}".format(type_name))

