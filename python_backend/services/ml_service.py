import numpy as np
from typing import List, Dict, Any
import json

class MLService:
    """Simple machine learning service for demonstrations."""
    
    def __init__(self):
        self.model_loaded = True
        self.prediction_count = 0
        
        # Simple mock model weights for demonstration
        self.weights = np.array([0.5, -0.3, 0.8, 0.2])
        self.bias = 0.1
    
    def predict(self, features: List[float]) -> Dict[str, Any]:
        """
        Make predictions using the mock model.
        
        Args:
            features: List of numerical features
            
        Returns:
            Dictionary containing prediction results
        """
        try:
            if not features:
                raise ValueError("No features provided")
            
            # Ensure we have the right number of features
            feature_array = np.array(features)
            
            if len(feature_array) != len(self.weights):
                # Pad or truncate features to match model
                if len(feature_array) < len(self.weights):
                    feature_array = np.pad(feature_array, (0, len(self.weights) - len(feature_array)))
                else:
                    feature_array = feature_array[:len(self.weights)]
            
            # Simple linear prediction
            raw_prediction = np.dot(feature_array, self.weights) + self.bias
            
            # Apply sigmoid for probability
            probability = 1 / (1 + np.exp(-raw_prediction))
            
            # Classify based on threshold
            classification = "positive" if probability > 0.5 else "negative"
            confidence = abs(probability - 0.5) * 2  # Scale confidence to 0-1
            
            result = {
                "raw_prediction": float(raw_prediction),
                "probability": float(probability),
                "classification": classification,
                "confidence": float(confidence),
                "features_used": feature_array.tolist(),
                "model_info": {
                    "type": "linear_classifier",
                    "features_count": len(self.weights),
                    "trained": True
                }
            }
            
            self.prediction_count += 1
            return result
            
        except Exception as e:
            raise Exception(f"Prediction failed: {str(e)}")
    
    def predict_batch(self, batch_features: List[List[float]]) -> List[Dict[str, Any]]:
        """
        Make predictions for multiple feature sets.
        
        Args:
            batch_features: List of feature lists
            
        Returns:
            List of prediction results
        """
        results = []
        for features in batch_features:
            try:
                result = self.predict(features)
                results.append(result)
            except Exception as e:
                results.append({"error": str(e)})
        
        return results
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance scores."""
        importance = np.abs(self.weights) / np.sum(np.abs(self.weights))
        return {
            f"feature_{i}": float(importance[i]) 
            for i in range(len(self.weights))
        }
    
    def train_mock_model(self, training_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Mock training function - in reality, this would train a real model.
        
        Args:
            training_data: Training dataset
            
        Returns:
            Training results
        """
        if not training_data:
            return {"error": "No training data provided"}
        
        # Simulate training by slightly adjusting weights
        noise = np.random.normal(0, 0.1, len(self.weights))
        self.weights = self.weights + noise
        
        return {
            "status": "trained",
            "samples_used": len(training_data),
            "new_weights": self.weights.tolist(),
            "accuracy": np.random.uniform(0.8, 0.95),  # Mock accuracy
            "epochs": 10
        }
    
    def get_model_stats(self) -> Dict[str, Any]:
        """Get model statistics."""
        return {
            "model_loaded": self.model_loaded,
            "predictions_made": self.prediction_count,
            "weights": self.weights.tolist(),
            "bias": float(self.bias),
            "feature_count": len(self.weights)
        }
