import hashlib
import json
import time
import os

BLOCKCHAIN_FILE = "data/blockchain.json"


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }


class Blockchain:
    def __init__(self):
        self.chain = []

        # Load blockchain if file exists
        if os.path.exists(BLOCKCHAIN_FILE):
            self.load_chain()

        # Always ensure genesis block exists
        if len(self.chain) == 0:
            self.create_genesis_block()
            self.save_chain()

    def create_genesis_block(self):
        genesis_block = Block(
            index=0,
            timestamp=time.time(),
            data="Genesis Block",
            previous_hash="0"
        )
        self.chain.append(genesis_block)

    def add_block(self, data):
        last_block = self.chain[-1]

        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=data,
            previous_hash=last_block.hash
        )

        self.chain.append(new_block)
        self.save_chain()

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

        return True

    def save_chain(self):
        os.makedirs("data", exist_ok=True)
        with open(BLOCKCHAIN_FILE, "w") as f:
            json.dump([block.to_dict() for block in self.chain], f, indent=4)

    def load_chain(self):
        with open(BLOCKCHAIN_FILE, "r") as f:
            data = json.load(f)

        self.chain = []

        for block_data in data:
            block = Block(
                index=block_data["index"],
                timestamp=block_data["timestamp"],
                data=block_data["data"],
                previous_hash=block_data["previous_hash"]
            )
            block.hash = block_data["hash"]
            self.chain.append(block)
