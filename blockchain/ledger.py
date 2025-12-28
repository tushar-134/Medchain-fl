"""Blockchain ledger for model update tracking."""

import hashlib
import json
from datetime import datetime
from typing import List, Dict, Optional
from config.logging_config import get_logger

logger = get_logger(__name__)


class Block:
    """A single block in the blockchain."""
    
    def __init__(
        self,
        index: int,
        timestamp: str,
        data: Dict,
        previous_hash: str
    ):
        """
        Initialize a block.
        
        Args:
            index: Block index
            timestamp: Block timestamp
            data: Block data (model updates, metrics, etc.)
            previous_hash: Hash of previous block
        """
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate block hash."""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self) -> Dict:
        """Convert block to dictionary."""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }


class BlockchainLedger:
    """Blockchain ledger for federated learning."""
    
    def __init__(self):
        """Initialize blockchain with genesis block."""
        self.chain: List[Block] = []
        self.create_genesis_block()
        logger.info("Initialized blockchain ledger")
    
    def create_genesis_block(self):
        """Create the first block in the chain."""
        genesis_block = Block(
            index=0,
            timestamp=datetime.now().isoformat(),
            data={"message": "Genesis Block - MedChain-FL"},
            previous_hash="0"
        )
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """Get the latest block."""
        return self.chain[-1]
    
    def add_block(self, data: Dict) -> Block:
        """
        Add a new block to the chain.
        
        Args:
            data: Block data
            
        Returns:
            New block
        """
        latest_block = self.get_latest_block()
        
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.now().isoformat(),
            data=data,
            previous_hash=latest_block.hash
        )
        
        self.chain.append(new_block)
        logger.info(f"Added block #{new_block.index} to blockchain")
        
        return new_block
    
    def record_fl_round(
        self,
        round_number: int,
        num_clients: int,
        global_metrics: Dict,
        model_hash: Optional[str] = None
    ) -> Block:
        """
        Record a federated learning round.
        
        Args:
            round_number: FL round number
            num_clients: Number of participating clients
            global_metrics: Aggregated metrics
            model_hash: Hash of global model weights
            
        Returns:
            New block
        """
        data = {
            "type": "fl_round",
            "round": round_number,
            "num_clients": num_clients,
            "metrics": global_metrics,
            "model_hash": model_hash
        }
        
        return self.add_block(data)
    
    def record_client_update(
        self,
        round_number: int,
        client_id: str,
        data_size: int,
        metrics: Dict
    ) -> Block:
        """
        Record a client update.
        
        Args:
            round_number: FL round number
            client_id: Client identifier
            data_size: Client dataset size
            metrics: Client metrics
            
        Returns:
            New block
        """
        data = {
            "type": "client_update",
            "round": round_number,
            "client_id": client_id,
            "data_size": data_size,
            "metrics": metrics
        }
        
        return self.add_block(data)
    
    def is_valid(self) -> bool:
        """
        Validate the blockchain.
        
        Returns:
            True if blockchain is valid
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check hash
            if current_block.hash != current_block.calculate_hash():
                logger.error(f"Invalid hash at block {i}")
                return False
            
            # Check previous hash
            if current_block.previous_hash != previous_block.hash:
                logger.error(f"Invalid previous hash at block {i}")
                return False
        
        return True
    
    def get_chain(self) -> List[Dict]:
        """Get the entire chain as list of dicts."""
        return [block.to_dict() for block in self.chain]
    
    def get_fl_rounds(self) -> List[Dict]:
        """Get all FL round records."""
        return [
            block.to_dict()
            for block in self.chain
            if block.data.get("type") == "fl_round"
        ]
    
    def save_to_file(self, filepath: str):
        """Save blockchain to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.get_chain(), f, indent=2)
        logger.info(f"Saved blockchain to {filepath}")
    
    def load_from_file(self, filepath: str):
        """Load blockchain from JSON file."""
        with open(filepath, 'r') as f:
            chain_data = json.load(f)
        
        self.chain = []
        for block_data in chain_data:
            block = Block(
                index=block_data["index"],
                timestamp=block_data["timestamp"],
                data=block_data["data"],
                previous_hash=block_data["previous_hash"]
            )
            self.chain.append(block)
        
        logger.info(f"Loaded blockchain from {filepath} ({len(self.chain)} blocks)")
