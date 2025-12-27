from api_collections.pokemon_api import PokemonAPICollection
from utils.bdd_utils import BDDUtils
from reusable_functions import ReusableFunctions
from schemas import POKEMON_SCHEMA, ABILITY_SCHEMA, POKEMON_LIST_SCHEMA
from typing import Dict, Any, Optional

class PokemonPage:
    def __init__(self):
        self.api = PokemonAPICollection()
        self.utils = BDDUtils()
        self.functions = ReusableFunctions()
        self.last_response = None
        self.last_response_data = None
        self.response_time = None
    
    def get_pokemon_by_identifier(self, identifier: str):
        """Get Pokemon by ID or name and store response"""
        if identifier.isdigit():
            self.last_response = self.api.get_pokemon_by_id(int(identifier))
        else:
            self.last_response = self.api.get_pokemon_by_name(identifier)
        
        self.utils.log_response_details(self.last_response, f"pokemon/{identifier}")
        return self.last_response
    
    def get_pokemon_list_with_pagination(self, limit: int = 20, offset: int = 0):
        """Get Pokemon list and store response"""
        self.last_response = self.api.get_pokemon_list(limit, offset)
        self.utils.log_response_details(self.last_response, "pokemon list")
        return self.last_response
    
    def get_ability_by_identifier(self, identifier: str):
        """Get ability and store response"""
        self.last_response = self.api.get_ability(identifier)
        self.utils.log_response_details(self.last_response, f"ability/{identifier}")
        return self.last_response
    
    def get_item_by_identifier(self, identifier: str):
        """Get item and store response"""
        self.last_response = self.api.get_item(identifier)
        self.utils.log_response_details(self.last_response, f"item/{identifier}")
        return self.last_response
    
    def validate_response_status(self, expected_status: int) -> bool:
        """Validate last response status code"""
        return self.utils.validate_status_code(self.last_response, expected_status)
    
    def validate_response_time(self, max_time: float) -> bool:
        """Validate last response time"""
        return self.utils.validate_response_time(self.last_response, max_time)
    
    def parse_response_data(self) -> Optional[Dict[str, Any]]:
        """Parse and store last response JSON data"""
        self.last_response_data = self.utils.validate_json_structure(self.last_response)
        return self.last_response_data
    
    def validate_pokemon_schema(self) -> bool:
        """Validate Pokemon response against schema"""
        if not self.last_response_data:
            self.parse_response_data()
        return self.utils.validate_schema(self.last_response_data, POKEMON_SCHEMA)
    
    def validate_ability_schema(self) -> bool:
        """Validate ability response against schema"""
        if not self.last_response_data:
            self.parse_response_data()
        return self.utils.validate_schema(self.last_response_data, ABILITY_SCHEMA)
    
    def validate_pokemon_list_schema(self) -> bool:
        """Validate Pokemon list response against schema"""
        if not self.last_response_data:
            self.parse_response_data()
        return self.utils.validate_schema(self.last_response_data, POKEMON_LIST_SCHEMA)
    
    def validate_required_fields(self, fields: list) -> bool:
        """Validate required fields are present"""
        if not self.last_response_data:
            self.parse_response_data()
        missing_fields = self.utils.validate_field_presence(self.last_response_data, fields)
        return len(missing_fields) == 0
    
    def get_pokemon_name(self) -> str:
        """Get Pokemon name from last response"""
        if not self.last_response_data:
            self.parse_response_data()
        return self.last_response_data.get("name", "")
    
    def get_pokemon_id(self) -> int:
        """Get Pokemon ID from last response"""
        if not self.last_response_data:
            self.parse_response_data()
        return self.last_response_data.get("id", 0)
    
    def get_pokemon_types(self) -> list:
        """Get Pokemon types from last response"""
        if not self.last_response_data:
            self.parse_response_data()
        return [t["type"]["name"] for t in self.last_response_data.get("types", [])]
    
    def validate_pokemon_has_abilities(self) -> bool:
        """Validate Pokemon has at least one ability"""
        if not self.last_response_data:
            self.parse_response_data()
        return self.utils.validate_array_not_empty(self.last_response_data, "abilities")
    
    def validate_pokemon_has_types(self) -> bool:
        """Validate Pokemon has at least one type"""
        if not self.last_response_data:
            self.parse_response_data()
        return self.utils.validate_array_not_empty(self.last_response_data, "types")