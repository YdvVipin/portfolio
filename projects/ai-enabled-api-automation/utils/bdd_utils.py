import json
import jsonschema
import logging
from typing import Dict, Any, List, Optional
from requests import Response

class BDDUtils:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def validate_status_code(self, response: Response, expected_code: int) -> bool:
        """Validate HTTP status code"""
        actual_code = response.status_code
        if actual_code != expected_code:
            self.logger.error(f"Status code mismatch: expected {expected_code}, got {actual_code}")
            return False
        return True
    
    def validate_response_time(self, response: Response, max_time: float) -> bool:
        """Validate response time"""
        response_time = response.elapsed.total_seconds()
        if response_time > max_time:
            self.logger.error(f"Response time {response_time}s exceeds limit {max_time}s")
            return False
        return True
    
    def validate_json_structure(self, response: Response) -> Optional[Dict[str, Any]]:
        """Validate and parse JSON response"""
        try:
            return response.json()
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON response: {e}")
            return None
    
    def validate_schema(self, data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
        """Validate data against JSON schema"""
        try:
            jsonschema.validate(data, schema)
            return True
        except jsonschema.ValidationError as e:
            self.logger.error(f"Schema validation failed: {e.message}")
            return False
    
    def validate_field_presence(self, data: Dict[str, Any], fields: List[str]) -> List[str]:
        """Return list of missing required fields"""
        return [field for field in fields if field not in data]
    
    def validate_field_type(self, data: Dict[str, Any], field: str, expected_type: type) -> bool:
        """Validate field data type"""
        if field not in data:
            return False
        return isinstance(data[field], expected_type)
    
    def validate_array_not_empty(self, data: Dict[str, Any], field: str) -> bool:
        """Validate that array field is not empty"""
        if field not in data or not isinstance(data[field], list):
            return False
        return len(data[field]) > 0
    
    def log_response_details(self, response: Response, endpoint: str):
        """Log response details for debugging"""
        self.logger.info(f"Endpoint: {endpoint}")
        self.logger.info(f"Status Code: {response.status_code}")
        self.logger.info(f"Response Time: {response.elapsed.total_seconds():.2f}s")
        self.logger.info(f"Response Size: {len(response.content)} bytes")