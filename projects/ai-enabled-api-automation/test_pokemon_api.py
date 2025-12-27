import pytest
import json
from pokeapi_client import PokeAPIClient
from test_utils import TestUtils
from schemas import POKEMON_SCHEMA, ABILITY_SCHEMA, POKEMON_LIST_SCHEMA

class TestPokemonAPI:
    @classmethod
    def setup_class(cls):
        """Setup test class with API client and test data"""
        cls.client = PokeAPIClient()
        cls.utils = TestUtils()
        cls.test_data = cls.client.config["test_data"]
    
    @pytest.mark.parametrize("pokemon_id", [1, 25, 150])
    def test_get_pokemon_by_id_valid(self, pokemon_id):
        """Test getting Pokemon by valid ID"""
        response = self.client.get_pokemon(pokemon_id)
        
        # Validate response
        self.utils.validate_response_status(response, 200)
        self.utils.validate_response_time(response, 5.0)
        
        data = self.utils.validate_json_response(response)
        self.utils.validate_json_schema(data, POKEMON_SCHEMA)
        
        # Validate specific fields
        assert data["id"] == pokemon_id
        assert isinstance(data["name"], str)
        assert len(data["name"]) > 0
    
    @pytest.mark.parametrize("pokemon_name", ["pikachu", "charizard", "mewtwo"])
    def test_get_pokemon_by_name_valid(self, pokemon_name):
        """Test getting Pokemon by valid name"""
        response = self.client.get_pokemon(pokemon_name)
        
        self.utils.validate_response_status(response, 200)
        self.utils.validate_response_time(response, 5.0)
        
        data = self.utils.validate_json_response(response)
        self.utils.validate_json_schema(data, POKEMON_SCHEMA)
        
        assert data["name"] == pokemon_name
        assert data["id"] > 0
    
    @pytest.mark.parametrize("invalid_id", [0, -1, 99999])
    def test_get_pokemon_by_invalid_id(self, invalid_id):
        """Test getting Pokemon by invalid ID returns 404"""
        response = self.client.get_pokemon(invalid_id)
        self.utils.validate_response_status(response, 404)
    
    @pytest.mark.parametrize("invalid_name", ["invalidpokemon", "123abc", ""])
    def test_get_pokemon_by_invalid_name(self, invalid_name):
        """Test getting Pokemon by invalid name returns 404"""
        response = self.client.get_pokemon(invalid_name)
        self.utils.validate_response_status(response, 404)
    
    def test_pokemon_required_fields(self):
        """Test that Pokemon response contains all required fields"""
        response = self.client.get_pokemon("pikachu")
        data = self.utils.validate_json_response(response)
        
        required_fields = ["id", "name", "height", "weight", "abilities", "types", "sprites"]
        self.utils.validate_required_fields(data, required_fields)
    
    def test_pokemon_field_types(self):
        """Test Pokemon response field data types"""
        response = self.client.get_pokemon("pikachu")
        data = self.utils.validate_json_response(response)
        
        field_types = {
            "id": int,
            "name": str,
            "height": int,
            "weight": int,
            "abilities": list,
            "types": list
        }
        self.utils.validate_field_types(data, field_types)
    
    def test_pokemon_abilities_structure(self):
        """Test Pokemon abilities have correct structure"""
        response = self.client.get_pokemon("pikachu")
        data = self.utils.validate_json_response(response)
        
        assert len(data["abilities"]) > 0
        for ability in data["abilities"]:
            assert "ability" in ability
            assert "is_hidden" in ability
            assert "slot" in ability
            assert isinstance(ability["is_hidden"], bool)
    
    def test_pokemon_types_structure(self):
        """Test Pokemon types have correct structure"""
        response = self.client.get_pokemon("pikachu")
        data = self.utils.validate_json_response(response)
        
        assert len(data["types"]) > 0
        for ptype in data["types"]:
            assert "slot" in ptype
            assert "type" in ptype
            assert "name" in ptype["type"]
            assert "url" in ptype["type"]
    
    @pytest.mark.parametrize("limit,offset", [(10, 0), (20, 20), (5, 100)])
    def test_pokemon_list_pagination(self, limit, offset):
        """Test Pokemon list with different pagination parameters"""
        response = self.client.get_pokemon_list(limit=limit, offset=offset)
        
        self.utils.validate_response_status(response, 200)
        data = self.utils.validate_json_response(response)
        self.utils.validate_json_schema(data, POKEMON_LIST_SCHEMA)
        
        assert len(data["results"]) <= limit
        assert data["count"] > 0
    
    def test_pokemon_evolution_chain_integration(self):
        """Test integration between Pokemon and evolution chain endpoints"""
        # Get Pokemon species first
        species_response = self.client.get_species("pikachu")
        self.utils.validate_response_status(species_response, 200)
        species_data = self.utils.validate_json_response(species_response)
        
        # Extract evolution chain URL and get chain ID
        evolution_url = species_data["evolution_chain"]["url"]
        chain_id = evolution_url.split("/")[-2]
        
        # Get evolution chain
        evolution_response = self.client.get_evolution_chain(chain_id)
        self.utils.validate_response_status(evolution_response, 200)
        evolution_data = self.utils.validate_json_response(evolution_response)
        
        assert "chain" in evolution_data
        assert "species" in evolution_data["chain"]