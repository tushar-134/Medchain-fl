"""Standalone Federated Learning Simulation - No complex imports needed!"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import json
from datetime import datetime

print("=" * 80)
print("MedChain-FL: Federated Learning Simulation")
print("=" * 80)

# Simple CBC Model
class CBCModel(nn.Module):
    def __init__(self, input_dim=8, num_classes=3):
        super(CBCModel, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(32, num_classes)
        )
    
    def forward(self, x):
        return self.model(x)

# Simple Dataset
class CBCDataset(Dataset):
    FEATURES = ["hb", "rbc", "mcv", "mch", "mchc", "rdw", "wbc", "platelets"]
    LABEL_MAP = {"normal": 0, "minor": 1, "major": 2}
    
    def __init__(self, csv_path, scaler=None, fit_scaler=True):
        self.data = pd.read_csv(csv_path)
        self.features = self.data[self.FEATURES].values
        self.labels = self.data["condition"].map(self.LABEL_MAP).values
        
        if scaler is None:
            self.scaler = StandardScaler()
        else:
            self.scaler = scaler
        
        if fit_scaler:
            self.features = self.scaler.fit_transform(self.features)
        else:
            self.features = self.scaler.transform(self.features)
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return torch.FloatTensor(self.features[idx]), torch.LongTensor([self.labels[idx]])[0]
    
    def get_scaler(self):
        return self.scaler

# Training function
def train_hospital(hospital_name, global_weights, epochs=2):
    print(f"\n>>> Training {hospital_name.upper()} Hospital...")
    
    data_path = Path(f"data/hospital_{hospital_name}/cbc_data.csv")
    if not data_path.exists():
        print(f"  ⚠ Data not found for {hospital_name}")
        return None, 0, {}
    
    # Load data
    dataset = CBCDataset(data_path)
    loader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    # Create model
    model = CBCModel()
    model.load_state_dict(global_weights)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Train
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        correct = 0
        total = 0
        
        for features, labels in loader:
            optimizer.zero_grad()
            outputs = model(features)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        
        avg_loss = total_loss / len(loader)
        accuracy = 100 * correct / total
        print(f"  Epoch {epoch+1}/{epochs}: Loss={avg_loss:.4f}, Accuracy={accuracy:.2f}%")
    
    # Return trained weights
    metrics = {"loss": avg_loss, "accuracy": accuracy / 100}
    return model.state_dict(), len(dataset), metrics

# Federated aggregation
def fedavg_aggregate(client_weights, client_sizes):
    """FedAvg aggregation."""
    total_size = sum(client_sizes)
    aggregated = {}
    
    for key in client_weights[0].keys():
        aggregated[key] = torch.zeros_like(client_weights[0][key])
    
    for weights, size in zip(client_weights, client_sizes):
        weight = float(size) / float(total_size)
        for key in aggregated.keys():
            aggregated[key] = aggregated[key] + weights[key].float() * weight
    
    # Cast back to original dtype
    for key in aggregated.keys():
        if client_weights[0][key].dtype != torch.float32:
            aggregated[key] = aggregated[key].to(client_weights[0][key].dtype)
    
    return aggregated

# Blockchain Ledger
class SimpleLedger:
    def __init__(self):
        self.chain = []
        self.chain.append({
            "index": 0,
            "timestamp": datetime.now().isoformat(),
            "type": "genesis",
            "data": "MedChain-FL Genesis Block"
        })
    
    def add_block(self, block_type, data):
        block = {
            "index": len(self.chain),
            "timestamp": datetime.now().isoformat(),
            "type": block_type,
            "data": data
        }
        self.chain.append(block)
        return block
    
    def save(self, filepath):
        with open(filepath, 'w') as f:
            json.dump(self.chain, f, indent=2)

# Main FL Simulation
def run_fl_simulation(rounds=3, local_epochs=2):
    print("\n" + "=" * 80)
    print(f"Configuration: {rounds} FL rounds, {local_epochs} local epochs per round")
    print("=" * 80)
    
    # Initialize
    global_model = CBCModel()
    ledger = SimpleLedger()
    hospitals = ["italy", "pakistan", "usa"]
    
    print(f"\nParticipating hospitals: {', '.join([h.upper() for h in hospitals])}")
    
    # FL Rounds
    for round_num in range(rounds):
        print(f"\n{'='*80}")
        print(f"FEDERATED LEARNING ROUND {round_num + 1}/{rounds}")
        print(f"{'='*80}")
        
        global_weights = global_model.state_dict()
        
        # Train each hospital
        client_weights = []
        client_sizes = []
        client_metrics = []
        
        for hospital in hospitals:
            weights, size, metrics = train_hospital(hospital, global_weights, local_epochs)
            
            if weights is not None:
                client_weights.append(weights)
                client_sizes.append(size)
                client_metrics.append(metrics)
                
                # Record on blockchain
                ledger.add_block("client_update", {
                    "round": round_num + 1,
                    "hospital": hospital,
                    "data_size": size,
                    "metrics": metrics
                })
        
        # Aggregate
        if len(client_weights) >= 2:
            print(f"\n>>> Aggregating {len(client_weights)} client models...")
            new_global_weights = fedavg_aggregate(client_weights, client_sizes)
            global_model.load_state_dict(new_global_weights)
            
            # Calculate average metrics
            avg_loss = sum(m["loss"] for m in client_metrics) / len(client_metrics)
            avg_acc = sum(m["accuracy"] for m in client_metrics) / len(client_metrics)
            
            print(f"  Global Model Updated!")
            print(f"  Average Loss: {avg_loss:.4f}")
            print(f"  Average Accuracy: {avg_acc*100:.2f}%")
            
            # Record on blockchain
            ledger.add_block("fl_round", {
                "round": round_num + 1,
                "num_clients": len(client_weights),
                "avg_loss": avg_loss,
                "avg_accuracy": avg_acc
            })
        else:
            print(f"\n  ⚠ Not enough clients (need at least 2)")
    
    # Save results
    print(f"\n{'='*80}")
    print("SAVING RESULTS")
    print(f"{'='*80}")
    
    model_path = "saved_models/final_global_model.pth"
    Path("saved_models").mkdir(exist_ok=True)
    torch.save(global_model.state_dict(), model_path)
    print(f"✓ Saved global model to: {model_path}")
    
    ledger_path = "blockchain_ledger.json"
    ledger.save(ledger_path)
    print(f"✓ Saved blockchain ledger to: {ledger_path}")
    print(f"  Total blocks in chain: {len(ledger.chain)}")
    
    print(f"\n{'='*80}")
    print("FEDERATED LEARNING COMPLETE!")
    print(f"{'='*80}")
    print(f"✓ Trained for {rounds} rounds across {len(hospitals)} hospitals")
    print(f"✓ Final model saved")
    print(f"✓ Blockchain ledger created")
    print("\nYour federated learning system is now ready!")

# Run it!
if __name__ == "__main__":
    run_fl_simulation(rounds=3, local_epochs=2)
