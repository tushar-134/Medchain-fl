"""API routes and endpoints."""

from flask import Blueprint, request, jsonify
import torch
import numpy as np
from pathlib import Path
from models.thalassemia_models import get_model
from models.model_utils import load_model
from config.settings import settings
from config.logging_config import get_logger

logger = get_logger(__name__)

# Create blueprint
api_bp = Blueprint('api', __name__)

# Global model (loaded on startup)
global_model = None


@api_bp.route('/predict/cbc', methods=['POST'])
def predict_cbc():
    """
    Predict thalassemia from CBC data.
    
    Request body:
    {
        "hb": 12.5,
        "rbc": 5.0,
        "mcv": 75.0,
        "mch": 25.0,
        "mchc": 32.0,
        "rdw": 14.5,
        "wbc": 7.0,
        "platelets": 250.0
    }
    """
    try:
        data = request.get_json()
        
        # Extract features
        features = np.array([[
            data['hb'],
            data['rbc'],
            data['mcv'],
            data['mch'],
            data['mchc'],
            data['rdw'],
            data['wbc'],
            data['platelets']
        ]], dtype=np.float32)
        
        # Normalize (you should use the same scaler from training)
        features_tensor = torch.FloatTensor(features)
        
        # Predict (placeholder - load actual model)
        # prediction = model(features_tensor)
        
        # Mock prediction
        prediction = {
            'condition': 'normal',
            'confidence': 0.85,
            'probabilities': {
                'normal': 0.85,
                'minor': 0.10,
                'major': 0.05
            }
        }
        
        return jsonify(prediction)
    
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 400


@api_bp.route('/model/info', methods=['GET'])
def model_info():
    """Get model information."""
    return jsonify({
        'model_type': settings.model_type,
        'num_classes': settings.num_classes,
        'image_size': settings.image_size,
        'status': 'loaded' if global_model else 'not_loaded'
    })


@api_bp.route('/blockchain/status', methods=['GET'])
def blockchain_status():
    """Get blockchain status."""
    # Placeholder - integrate with actual blockchain
    return jsonify({
        'enabled': settings.blockchain_enabled,
        'network': settings.blockchain_network,
        'blocks': 0
    })


@api_bp.route('/federated/status', methods=['GET'])
def federated_status():
    """Get federated learning status."""
    return jsonify({
        'fl_rounds': settings.fl_rounds,
        'min_clients': settings.min_clients,
        'aggregation_method': settings.aggregation_method,
        'current_round': 0
    })


@api_bp.route('/hospital/register', methods=['POST'])
def register_hospital():
    """
    Register a hospital as FL client.
    
    Request body:
    {
        "hospital_id": "hospital_italy",
        "organization": "Hospital Italy",
        "data_size": 1000
    }
    """
    try:
        data = request.get_json()
        
        # Placeholder - integrate with smart contract
        response = {
            'status': 'registered',
            'hospital_id': data['hospital_id'],
            'message': 'Hospital successfully registered for federated learning'
        }
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({'error': str(e)}), 400
