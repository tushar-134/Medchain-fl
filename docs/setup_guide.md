# Setup Guide

## Prerequisites

- Python 3.10+
- Node.js 16+ (for dashboard)
- Git
- (Optional) Azure subscription for cloud deployment
- (Optional) CUDA-capable GPU for faster training

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/medchain-fl/medchain-fl.git
cd medchain-fl
```

### 2. Python Environment

**Option A: Conda (Recommended)**
```bash
conda env create -f environment.yml
conda activate medchain-fl
```

**Option B: pip + venv**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Install Package

```bash
pip install -e .
```

### 4. Generate Demo Data

```bash
python scripts/generate_demo_data.py --n-samples 1000
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Model Settings
MODEL_TYPE=hybrid
IMAGE_SIZE=224
NUM_CLASSES=3

# Training
BATCH_SIZE=32
LEARNING_RATE=0.001
EPOCHS=50

# Federated Learning
FL_ROUNDS=10
LOCAL_EPOCHS=5
AGGREGATION_METHOD=fedavg
MIN_CLIENTS=2

# Blockchain
BLOCKCHAIN_ENABLED=true
BLOCKCHAIN_NETWORK=ganache

# API
API_HOST=0.0.0.0
API_PORT=5000
API_DEBUG=true

# Azure ML (if using)
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_RESOURCE_GROUP=medchain-fl-rg
AZURE_WORKSPACE_NAME=medchain-fl-ws
```

## Running the System

### 1. Local Federated Learning

```bash
python scripts/run_local_fl.py --rounds 10 --local-epochs 5
```

### 2. Start API Server

```bash
cd api
python app.py
```

### 3. Start Dashboard

```bash
cd dashboard
npm install
npm run dev
```

Visit `http://localhost:5173` to view the dashboard.

### 4. Run Tests

```bash
pytest tests/ -v
```

## Azure ML Setup (Optional)

### 1. Install Azure CLI

```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
az login
```

### 2. Setup Workspace

```bash
python azure_ml/setup_compute.py
```

### 3. Upload Data

```bash
python azure_ml/upload_data.py
```

### 4. Run Azure FL

```bash
python scripts/run_azure_fl.py
```

## Troubleshooting

### Import Errors
Make sure you installed the package with `pip install -e .`

### CUDA Out of Memory
Reduce `BATCH_SIZE` in your `.env` file

### Data Not Found
Run `python scripts/generate_demo_data.py` first

### API Connection Refused
Make sure the API server is running on the correct port

## Next Steps

- Read the [Architecture](architecture.md) documentation
- Check out the [API Documentation](api_documentation.md)
- Review example notebooks in `notebooks/`
