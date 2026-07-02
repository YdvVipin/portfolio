import json
import time
from typing import Dict, Any, List

class ReusableFunctions:
    @staticmethod
    def load_test_data(file_path: str = "data/test_data.json") -> Dict[str, Any]:
        """Load test data from JSON file"""
        with open(file_path, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def extract_id_from_url(url: str) -> str:
        """Extract ID from API URL"""
        return url.rstrip('/').split('/')[-1]
    
    @staticmethod
    def measure_response_time(func, *args, **kwargs) -> tuple:
        """Measure function execution time"""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        return result, end_time - start_time
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> bool:
        """Check if all required fields are present"""
        return all(field in data for field in required_fields)
    
    @staticmethod
    def extract_nested_value(data: Dict[str, Any], path: str, default=None):
        """Extract nested value using dot notation"""
        keys = path.split('.')
        value = data
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    @staticmethod
    def format_pokemon_data(pokemon_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format Pokemon data for display"""
        return {
            "id": pokemon_data.get("id"),
            "name": pokemon_data.get("name", "").title(),
            "height": pokemon_data.get("height"),
            "weight": pokemon_data.get("weight"),
            "types": [t["type"]["name"] for t in pokemon_data.get("types", [])],
            "abilities": [a["ability"]["name"] for a in pokemon_data.get("abilities", [])]
        }
    
    @staticmethod
    def compare_response_data(actual: Dict[str, Any], expected: Dict[str, Any]) -> bool:
        """Compare response data with expected values"""
        for key, expected_value in expected.items():
            if key not in actual or actual[key] != expected_value:
                return False
        return True