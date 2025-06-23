import hashlib
import json
from time import time
import os

class Block:
    def __init__(self, index, timestamp, data, prediction, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prediction = prediction
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "prediction": self.prediction,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()
    
    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "prediction": self.prediction,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

class Blockchain:
    def __init__(self, blockchain_file="blockchain.json"):
        self.chain = []
        self.blockchain_file = blockchain_file
        
        # Load existing blockchain if it exists
        if os.path.exists(self.blockchain_file):
            try:
                with open(self.blockchain_file, 'r') as f:
                    chain_data = json.load(f)
                    for block_data in chain_data:
                        block = Block(
                            block_data["index"],
                            block_data["timestamp"],
                            block_data["data"],
                            block_data["prediction"],
                            block_data["previous_hash"]
                        )
                        block.hash = block_data["hash"]
                        self.chain.append(block)
            except Exception as e:
                print(f"Error loading blockchain: {e}")
                self.create_genesis_block()
        else:
            self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis_block = Block(0, time(), {}, "Genesis Block", "0")
        self.chain.append(genesis_block)
        self.save_blockchain()
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def add_block(self, data, prediction):
        latest_block = self.get_latest_block()
        new_block = Block(
            len(self.chain),
            time(),
            data,
            prediction,
            latest_block.hash
        )
        
        self.chain.append(new_block)
        self.save_blockchain()
        return new_block
    
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check if the current block's hash is correct
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if the previous hash reference is correct
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def save_blockchain(self):
        chain_data = [block.to_dict() for block in self.chain]
        with open(self.blockchain_file, 'w') as f:
            json.dump(chain_data, f, indent=4)
    
    def get_chain(self):
        return [block.to_dict() for block in self.chain]