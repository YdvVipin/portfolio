import json
import jsonschema
from typing import Dict, Any, List
import logging

class TestUtils:
    @staticmethod
    def validate_response_status(response, expected_status: int = 200):
        """Validate HTTP response status code"""
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
    
    @staticmethod
    def validate_json_response(response) -> Dict[str, Any]:
        """Validate response is valid JSON and return parsed data"""
        try:
            return response.json()
        except json.JSONDecodeError:
            raise AssertionError("Response is not valid JSON")
    
    @staticmethod
    def validate_response_time(response, max_time: float = 5.0):
        """Validate response time is within acceptable limits"""
        response_time = response.elapsed.total_seconds()
        assert response_time <= max_time, f"Response time {response_time}s exceeds limit {max_time}s"
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: List[str]):
        """Validate that required fields are present in response"""
        missing_fields = [field for field in required_fields if field not in data]
        assert not missing_fields, f"Missing required fields: {missing_fields}"
    
    @staticmethod
    def validate_field_types(data: Dict[str, Any], field_types: Dict[str, type]):
        """Validate field data types"""
        for field, expected_type in field_types.items():
            if field in data:
                actual_type = type(data[field])
                assert actual_type == expected_type, f"Field '{field}' expected {expected_type}, got {actual_type}"
    
    @staticmethod
    def validate_json_schema(data: Dict[str, Any], schema: Dict[str, Any]):
        """Validate response against JSON schema"""
        try:
            jsonschema.validate(data, schema)
        except jsonschema.ValidationError as e:
            raise AssertionError(f"JSON schema validation failed: {e.message}")
    
    @staticmethod
    def extract_field_value(data: Dict[str, Any], field_path: str):
        """Extract nested field value using dot notation (e.g., 'sprites.front_default')"""
        keys = field_path.split('.')
        value = data
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        return value