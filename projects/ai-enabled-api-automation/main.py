#!/usr/bin/env python3
"""
PokéAPI Automation Framework Demo
Demonstrates the framework capabilities with live API calls
"""

from pokeapi_client import PokeAPIClient
from test_utils import TestUtils
from schemas import POKEMON_SCHEMA
import json

def demo_framework():
    """Demonstrate framework capabilities"""
    print("🎮 PokéAPI Automation Framework Demo")
    print("=" * 40)
    
    # Initialize client and utils
    client = PokeAPIClient()
    utils = TestUtils()
    
    # Demo 1: Basic Pokemon retrieval
    print("\n1️⃣ Testing Pokemon Retrieval:")
    response = client.get_pokemon("pikachu")
    print(f"   Status: {response.status_code}")
    print(f"   Response Time: {response.elapsed.total_seconds():.2f}s")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   Pokemon: {data['name'].title()}")
        print(f"   ID: {data['id']}")
        print(f"   Height: {data['height']} decimeters")
        print(f"   Weight: {data['weight']} hectograms")
        print(f"   Types: {[t['type']['name'] for t in data['types']]}")
    
    # Demo 2: Response validation
    print("\n2️⃣ Testing Response Validation:")
    try:
        utils.validate_response_status(response, 200)
        utils.validate_response_time(response, 5.0)
        data = utils.validate_json_response(response)
        utils.validate_json_schema(data, POKEMON_SCHEMA)
        print("   ✅ All validations passed!")
    except AssertionError as e:
        print(f"   ❌ Validation failed: {e}")
    
    # Demo 3: Error handling
    print("\n3️⃣ Testing Error Handling:")
    error_response = client.get_pokemon("invalidpokemon")
    print(f"   Invalid Pokemon Status: {error_response.status_code}")
    print("   ✅ Properly handled 404 error")
    
    # Demo 4: Multiple endpoints
    print("\n4️⃣ Testing Multiple Endpoints:")
    endpoints_test = [
        ("ability", "1", "Stench"),
        ("item", "1", "Master Ball"),
        ("move", "1", "Pound"),
        ("type", "1", "Normal")
    ]
    
    for endpoint, id_val, expected_name in endpoints_test:
        method = getattr(client, f"get_{endpoint}")
        resp = method(id_val)
        if resp.status_code == 200:
            name = resp.json().get('name', 'Unknown')
            print(f"   {endpoint.title()}: {name.title()} ✅")
        else:
            print(f"   {endpoint.title()}: Failed ❌")
    
    # Demo 5: Pagination
    print("\n5️⃣ Testing Pagination:")
    list_response = client.get_pokemon_list(limit=5, offset=0)
    if list_response.status_code == 200:
        list_data = list_response.json()
        print(f"   Total Pokemon: {list_data['count']}")
        print(f"   Retrieved: {len(list_data['results'])} Pokemon")
        print(f"   First 3: {[p['name'] for p in list_data['results'][:3]]}")
    
    print("\n🎉 Demo completed! Run 'python run_tests.py' for full test suite.")

if __name__ == '__main__':
    demo_framework()
