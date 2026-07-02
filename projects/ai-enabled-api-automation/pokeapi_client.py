import json
from api_client import APIClient
from typing import Dict, Any, Optional

class PokeAPIClient(APIClient):
    def __init__(self, config_path: str = "config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        super().__init__(
            base_url=self.config["base_url"],
            timeout=self.config["timeout"],
            retry_count=self.config["retry_count"]
        )
        self.endpoints = self.config["endpoints"]
    
    def get_pokemon(self, identifier: str) -> Dict[str, Any]:
        """Get Pokemon by ID or name"""
        endpoint = f"{self.endpoints['pokemon']}{identifier}"
        response = self.get(endpoint)
        return response
    
    def get_ability(self, identifier: str) -> Dict[str, Any]:
        """Get ability by ID or name"""
        endpoint = f"{self.endpoints['ability']}{identifier}"
        response = self.get(endpoint)
        return response
    
    def get_item(self, identifier: str) -> Dict[str, Any]:
        """Get item by ID or name"""
        endpoint = f"{self.endpoints['item']}{identifier}"
        response = self.get(endpoint)
        return response
    
    def get_move(self, identifier: str) -> Dict[str, Any]:
        """Get move by ID or name"""
        endpoint = f"{self.endpoints['move']}{identifier}"
        response = self.get(endpoint)
        return response
    
    def get_type(self, identifier: str) -> Dict[str, Any]:
        """Get type by ID or name"""
        endpoint = f"{self.endpoints['type']}{identifier}"
        response = self.get(endpoint)
        return response
    
    def get_evolution_chain(self, chain_id: int) -> Dict[str, Any]:
        """Get evolution chain by ID"""
        endpoint = f"{self.endpoints['evolution_chain']}{chain_id}"
        response = self.get(endpoint)
        return response
    
    def get_species(self, identifier: str) -> Dict[str, Any]:
        """Get Pokemon species by ID or name"""
        endpoint = f"{self.endpoints['species']}{identifier}"
        response = self.get(endpoint)
        return response
    
    def get_pokemon_list(self, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """Get list of Pokemon with pagination"""
        endpoint = self.endpoints['pokemon']
        params = {"limit": limit, "offset": offset}
        response = self.get(endpoint, params=params)
        return response