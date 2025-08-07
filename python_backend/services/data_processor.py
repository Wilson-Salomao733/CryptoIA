import pandas as pd
import numpy as np
from typing import Dict, List, Any

class DataProcessor:
    """Service for processing and analyzing data."""
    
    def __init__(self):
        self.processed_count = 0
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming data and return analyzed results.
        
        Args:
            data: Dictionary containing data to process
            
        Returns:
            Dictionary with processed results
        """
        try:
            if 'numbers' in data:
                return self._process_numbers(data['numbers'])
            elif 'text' in data:
                return self._process_text(data['text'])
            elif 'dataset' in data:
                return self._process_dataset(data['dataset'])
            else:
                return self._basic_process(data)
                
        except Exception as e:
            raise Exception(f"Data processing failed: {str(e)}")
    
    def _process_numbers(self, numbers: List[float]) -> Dict[str, Any]:
        """Process numerical data."""
        if not numbers:
            return {"error": "No numbers provided"}
        
        arr = np.array(numbers)
        
        result = {
            "original_data": numbers,
            "count": len(numbers),
            "sum": float(np.sum(arr)),
            "mean": float(np.mean(arr)),
            "median": float(np.median(arr)),
            "std": float(np.std(arr)),
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
            "processed_at": pd.Timestamp.now().isoformat()
        }
        
        self.processed_count += 1
        return result
    
    def _process_text(self, text: str) -> Dict[str, Any]:
        """Process text data."""
        if not text:
            return {"error": "No text provided"}
        
        words = text.split()
        
        result = {
            "original_text": text,
            "word_count": len(words),
            "character_count": len(text),
            "character_count_no_spaces": len(text.replace(" ", "")),
            "sentence_count": len([s for s in text.split('.') if s.strip()]),
            "average_word_length": sum(len(word) for word in words) / len(words) if words else 0,
            "processed_at": pd.Timestamp.now().isoformat()
        }
        
        self.processed_count += 1
        return result
    
    def _process_dataset(self, dataset: List[Dict]) -> Dict[str, Any]:
        """Process dataset (list of dictionaries)."""
        if not dataset:
            return {"error": "Empty dataset"}
        
        df = pd.DataFrame(dataset)
        
        result = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "data_types": df.dtypes.to_dict(),
            "sample_data": df.head().to_dict('records'),
            "processed_at": pd.Timestamp.now().isoformat()
        }
        
        # Add numerical statistics if there are numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            result["numerical_summary"] = df[numeric_cols].describe().to_dict()
        
        self.processed_count += 1
        return result
    
    def _basic_process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Basic processing for any data."""
        result = {
            "data_keys": list(data.keys()),
            "data_size": len(str(data)),
            "data_type": type(data).__name__,
            "processed_at": pd.Timestamp.now().isoformat(),
            "total_processed": self.processed_count + 1
        }
        
        self.processed_count += 1
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return {
            "total_processed": self.processed_count,
            "service_status": "active"
        }
