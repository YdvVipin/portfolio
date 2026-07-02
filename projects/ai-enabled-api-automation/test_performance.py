import pytest
import time
import concurrent.futures
from pokeapi_client import PokeAPIClient
from test_utils import TestUtils

class TestPerformance:
    @classmethod
    def setup_class(cls):
        cls.client = PokeAPIClient()
        cls.utils = TestUtils()
    
    def test_response_time_single_pokemon(self):
        """Test single Pokemon request response time"""
        start_time = time.time()
        response = self.client.get_pokemon("pikachu")
        end_time = time.time()
        
        self.utils.validate_response_status(response, 200)
        response_time = end_time - start_time
        assert response_time < 2.0, f"Response time {response_time}s exceeds 2s limit"
    
    def test_response_time_multiple_requests(self):
        """Test multiple sequential requests performance"""
        pokemon_list = ["pikachu", "charizard", "blastoise", "venusaur", "mewtwo"]
        total_start = time.time()
        
        for pokemon in pokemon_list:
            start_time = time.time()
            response = self.client.get_pokemon(pokemon)
            end_time = time.time()
            
            self.utils.validate_response_status(response, 200)
            response_time = end_time - start_time
            assert response_time < 3.0, f"Response time {response_time}s for {pokemon} exceeds 3s limit"
        
        total_time = time.time() - total_start
        avg_time = total_time / len(pokemon_list)
        assert avg_time < 2.0, f"Average response time {avg_time}s exceeds 2s limit"
    
    def test_concurrent_requests(self):
        """Test concurrent API requests"""
        pokemon_list = ["pikachu", "charizard", "blastoise", "venusaur", "mewtwo"]
        
        def fetch_pokemon(name):
            start_time = time.time()
            response = self.client.get_pokemon(name)
            end_time = time.time()
            return {
                "name": name,
                "status_code": response.status_code,
                "response_time": end_time - start_time
            }
        
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(fetch_pokemon, name) for name in pokemon_list]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        total_time = time.time() - start_time
        
        # Validate all requests succeeded
        for result in results:
            assert result["status_code"] == 200
            assert result["response_time"] < 5.0
        
        # Concurrent requests should be faster than sequential
        assert total_time < 10.0, f"Concurrent requests took {total_time}s, too slow"
    
    @pytest.mark.parametrize("endpoint_method,identifier", [
        ("get_pokemon", "1"),
        ("get_ability", "1"),
        ("get_item", "1"),
        ("get_move", "1"),
        ("get_type", "1")
    ])
    def test_different_endpoints_performance(self, endpoint_method, identifier):
        """Test performance across different API endpoints"""
        method = getattr(self.client, endpoint_method)
        
        start_time = time.time()
        response = method(identifier)
        end_time = time.time()
        
        self.utils.validate_response_status(response, 200)
        response_time = end_time - start_time
        assert response_time < 3.0, f"{endpoint_method} response time {response_time}s exceeds 3s limit"
    
    def test_large_response_performance(self):
        """Test performance with larger response payloads"""
        # Get Pokemon list with larger limit
        start_time = time.time()
        response = self.client.get_pokemon_list(limit=100, offset=0)
        end_time = time.time()
        
        self.utils.validate_response_status(response, 200)
        data = self.utils.validate_json_response(response)
        
        response_time = end_time - start_time
        assert response_time < 5.0, f"Large response time {response_time}s exceeds 5s limit"
        assert len(data["results"]) == 100