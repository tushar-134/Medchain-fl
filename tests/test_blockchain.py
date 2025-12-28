"""Unit tests for blockchain."""

import pytest
from blockchain.ledger import BlockchainLedger, Block
from blockchain.smart_contract import SmartContract


def test_blockchain_creation():
    """Test blockchain initialization."""
    blockchain = BlockchainLedger()
    
    assert len(blockchain.chain) == 1  # Genesis block
    assert blockchain.is_valid()


def test_add_block():
    """Test adding blocks."""
    blockchain = BlockchainLedger()
    
    data = {"test": "data"}
    block = blockchain.add_block(data)
    
    assert len(blockchain.chain) == 2
    assert block.data == data
    assert blockchain.is_valid()


def test_fl_round_recording():
    """Test recording FL round."""
    blockchain = BlockchainLedger()
    
    metrics = {"accuracy": 0.85, "loss": 0.3}
    block = blockchain.record_fl_round(1, 3, metrics)
    
    assert block.data["type"] == "fl_round"
    assert block.data["round"] == 1
    assert blockchain.is_valid()


def test_smart_contract():
    """Test smart contract."""
    contract = SmartContract(min_clients=2)
    
    # Register clients
    assert contract.register_client("client1", "Hospital A", 100)
    assert contract.register_client("client2", "Hospital B", 150)
    
    # Test aggregation permission
    assert contract.can_aggregate(["client1", "client2"])
    assert not contract.can_aggregate(["client1"])  # Not enough clients
