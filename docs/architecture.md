# MedChain-FL Architecture

## System Overview

MedChain-FL is a privacy-preserving federated learning system for thalassemia detection that combines:
- **Federated Learning**: Distributed training across hospitals
- **Blockchain**: Transparent and secure model aggregation tracking
- **Azure ML**: Scalable cloud deployment
- **Multi-modal Models**: CBC data + blood smear images

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      MedChain-FL System                     │
└─────────────────────────────────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
   ┌────▼────┐          ┌─────▼─────┐         ┌─────▼─────┐
   │Hospital │          │ Hospital  │         │ Hospital  │
   │  Italy  │          │ Pakistan  │         │    USA    │
   └────┬────┘          └─────┬─────┘         └─────┬─────┘
        │                     │                      │
        │    Local Training   │                      │
        │    (Private Data)   │                      │
        └──────────┬──────────┴──────────────────────┘
                   │
                   │ Model Updates
                   ▼
        ┌──────────────────────┐
        │  FL Orchestrator     │
        │  - FedAvg            │
        │  - Aggregation       │
        └──────────┬───────────┘
                   │
         ┌─────────┴──────────┐
         │                    │
    ┌────▼────┐        ┌─────▼──────┐
    │Blockchain│       │   Global   │
    │ Ledger   │       │   Model    │
    └──────────┘       └────────────┘
```

## Components

### 1. Data Layer
- **Hospital Data**: Decentralized storage at each hospital
- **CBC Features**: 8 blood count parameters
- **Blood Smears**: Microscopy images
- **Data Loaders**: PyTorch datasets for each modality

### 2. Model Layer
- **CBC Model**: MLP for tabular data
- **Image Model**: ResNet-18 for images
- **Hybrid Model**: Fusion of both modalities

### 3. Federated Learning Layer
- **Local Trainers**: Train on hospital data
- **Orchestrator**: Coordinates FL rounds
- **Aggregator**: FedAvg/weighted aggregation

### 4. Blockchain Layer
- **Ledger**: Immutable record of training rounds
- **Smart Contract**: Access control and governance
- **Block Structure**: Round metadata, metrics, model hashes

### 5. Cloud Layer (Azure ML)
- **Compute**: GPU clusters for training
- **Datastores**: Centralized data storage
- **Pipelines**: Automated FL workflows

### 6. API Layer
- **REST API**: Flask-based endpoints
- **Model Serving**: Inference endpoints
- **Monitoring**: Training status

### 7. Dashboard
- **React Frontend**: Web-based monitoring
- **Visualization**: Training metrics, blockchain
- **Management**: Client registration

## Data Flow

1. **Initialization**: Global model initialized
2. **Distribution**: Model sent to hospitals
3. **Local Training**: Each hospital trains on private data
4. **Update Collection**: Send model updates (not data)
5. **Aggregation**: Combine updates using FedAvg
6. **Blockchain Recording**: Log round on blockchain
7. **Iteration**: Repeat for multiple rounds

## Security & Privacy

- **Data Privacy**: Raw data never leaves hospitals
- **Secure Aggregation**: Only model updates shared
- **Blockchain Audit**: Transparent training history
- **Access Control**: Smart contract governance

## Scalability

- **Horizontal**: Add more hospital clients
- **Vertical**: Azure ML for compute scaling
- **Asynchronous**: Non-blocking aggregation
