"""Smart contract for federated learning governance."""

from typing import Dict, List, Optional
from datetime import datetime
from config.logging_config import get_logger

logger = get_logger(__name__)


class SmartContract:
    """Smart contract for FL governance and access control."""
    
    def __init__(self, min_clients: int = 2, min_data_quality: float = 0.6):
        """
        Initialize smart contract.
        
        Args:
            min_clients: Minimum clients to aggregate
            min_data_quality: Minimum data quality score
        """
        self.min_clients = min_clients
        self.min_data_quality = min_data_quality
        
        # Registered clients
        self.clients: Dict[str, Dict] = {}
        
        # Access logs
        self.access_log: List[Dict] = []
        
        logger.info(f"Initialized smart contract (min_clients={min_clients})")
    
    def register_client(
        self,
        client_id: str,
        organization: str,
        data_size: int,
        data_quality: float = 1.0
    ) -> bool:
        """
        Register a new client.
        
        Args:
            client_id: Unique client identifier
            organization: Organization name
            data_size: Dataset size
            data_quality: Data quality score (0-1)
            
        Returns:
            True if registration successful
        """
        if client_id in self.clients:
            logger.warning(f"Client {client_id} already registered")
            return False
        
        if data_quality < self.min_data_quality:
            logger.warning(f"Client {client_id} data quality too low: {data_quality}")
            return False
        
        self.clients[client_id] = {
            "organization": organization,
            "data_size": data_size,
            "data_quality": data_quality,
            "registered_at": datetime.now().isoformat(),
            "active": True
        }
        
        logger.info(f"Registered client {client_id} ({organization})")
        return True
    
    def deactivate_client(self, client_id: str) -> bool:
        """Deactivate a client."""
        if client_id not in self.clients:
            return False
        
        self.clients[client_id]["active"] = False
        logger.info(f"Deactivated client {client_id}")
        return True
    
    def can_aggregate(self, participating_clients: List[str]) -> bool:
        """
        Check if aggregation can proceed.
        
        Args:
            participating_clients: List of client IDs
            
        Returns:
            True if aggregation allowed
        """
        # Check minimum clients
        if len(participating_clients) < self.min_clients:
            logger.warning(f"Not enough clients: {len(participating_clients)} < {self.min_clients}")
            return False
        
        # Check all clients are registered and active
        for client_id in participating_clients:
            if client_id not in self.clients:
                logger.warning(f"Unregistered client: {client_id}")
                return False
            
            if not self.clients[client_id]["active"]:
                logger.warning(f"Inactive client: {client_id}")
                return False
        
        return True
    
    def log_access(self, client_id: str, action: str, success: bool):
        """Log client access."""
        self.access_log.append({
            "timestamp": datetime.now().isoformat(),
            "client_id": client_id,
            "action": action,
            "success": success
        })
    
    def get_client_info(self, client_id: str) -> Optional[Dict]:
        """Get client information."""
        return self.clients.get(client_id)
    
    def get_active_clients(self) -> List[str]:
        """Get list of active clients."""
        return [
            client_id
            for client_id, info in self.clients.items()
            if info["active"]
        ]
