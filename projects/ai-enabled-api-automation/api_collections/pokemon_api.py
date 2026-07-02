from api_client import APIClient
import json
from typing import Dict, Any, Optional

class PokemonAPICollection:
    def __init__(self, config_path: str = "config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.client = APIClient(
            base_url=self.config["base_url"],
            timeout=self.config["timeout"],
            retry_count=self.config["retry_count"]
        )
        self.endpoints = self.config["endpoints"]
    
    def get_pokemon_by_id(self, pokemon_id: int):
        """Get Pokemon by ID"""
        endpoint = f"{self.endpoints['pokemon']}{pokemon_id}"
        return self.client.get(endpoint)
    
    def get_pokemon_by_name(self, pokemon_name: str):
        """Get Pokemon by name"""
        endpoint = f"{self.endpoints['pokemon']}{pokemon_name}"
        return self.client.get(endpoint)
    
    def get_pokemon_list(self, limit: int = 20, offset: int = 0):
        """Get Pokemon list with pagination"""
        endpoint = self.endpoints['pokemon']
        params = {"limit": limit, "offset": offset}
        return self.client.get(endpoint, params=params)
    
    def get_ability(self, identifier: str):
        """Get ability by ID or name"""
        endpoint = f"{self.endpoints['ability']}{identifier}"
        return self.client.get(endpoint)
    
    def get_item(self, identifier: str):
        """Get item by ID or name"""
        endpoint = f"{self.endpoints['item']}{identifier}"
        return self.client.get(endpoint)
    
    def get_move(self, identifier: str):
        """Get move by ID or name"""
        endpoint = f"{self.endpoints['move']}{identifier}"
        return self.client.get(endpoint)
    
    def get_type(self, identifier: str):
        """Get type by ID or name"""
        endpoint = f"{self.endpoints['type']}{identifier}"
        return self.client.get(endpoint)
    
    def get_evolution_chain(self, chain_id: int):
        """Get evolution chain by ID"""
        endpoint = f"{self.endpoints['evolution_chain']}{chain_id}"
        return self.client.get(endpoint)
    
    def get_species(self, identifier: str):
        """Get Pokemon species by ID or name"""
        endpoint = f"{self.endpoints['species']}{identifier}"
        return self.client.get(endpoint)