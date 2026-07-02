from behave import given, when, then
from pages.pokemon_page import PokemonPage
from reusable_functions import ReusableFunctions
import allure

@given('the Pokemon API is available')
@allure.step("Initialize Pokemon API client")
def step_api_available(context):
    """Initialize Pokemon page object"""
    context.pokemon_page = PokemonPage()
    context.functions = ReusableFunctions()

@when('I request Pokemon with ID "{pokemon_id}"')
@allure.step("Request Pokemon by ID: {pokemon_id}")
def step_request_pokemon_by_id(context, pokemon_id):
    """Request Pokemon by ID"""
    with allure.step(f"Making API call to get Pokemon with ID {pokemon_id}"):
        context.pokemon_page.get_pokemon_by_identifier(pokemon_id)

@when('I request Pokemon with name "{pokemon_name}"')
@allure.step("Request Pokemon by name: {pokemon_name}")
def step_request_pokemon_by_name(context, pokemon_name):
    """Request Pokemon by name"""
    with allure.step(f"Making API call to get Pokemon with name {pokemon_name}"):
        context.pokemon_page.get_pokemon_by_identifier(pokemon_name)

@when('I request Pokemon list with limit {limit:d} and offset {offset:d}')
@allure.step("Request Pokemon list with pagination")
def step_request_pokemon_list(context, limit, offset):
    """Request Pokemon list with pagination"""
    with allure.step(f"Getting Pokemon list with limit={limit}, offset={offset}"):
        context.pokemon_page.get_pokemon_list_with_pagination(limit, offset)

@when('I request ability with identifier "{identifier}"')
@allure.step("Request ability: {identifier}")
def step_request_ability(context, identifier):
    """Request ability by identifier"""
    with allure.step(f"Making API call to get ability {identifier}"):
        context.pokemon_page.get_ability_by_identifier(identifier)

@when('I request "{endpoint}" with identifier "{identifier}"')
@allure.step("Request {endpoint} endpoint with identifier: {identifier}")
def step_request_endpoint(context, endpoint, identifier):
    """Request any endpoint with identifier"""
    with allure.step(f"Making API call to {endpoint} endpoint"):
        if endpoint == "pokemon":
            context.pokemon_page.get_pokemon_by_identifier(identifier)
        elif endpoint == "ability":
            context.pokemon_page.get_ability_by_identifier(identifier)
        elif endpoint == "item":
            context.pokemon_page.get_item_by_identifier(identifier)

@when('I get the species information for the Pokemon')
@allure.step("Get Pokemon species information")
def step_get_species_info(context):
    """Get species information for current Pokemon"""
    pokemon_data = context.pokemon_page.parse_response_data()
    species_url = pokemon_data["species"]["url"]
    species_id = context.functions.extract_id_from_url(species_url)
    context.pokemon_page.api.get_species(species_id)

@when('I get the evolution chain for the species')
@allure.step("Get evolution chain information")
def step_get_evolution_chain(context):
    """Get evolution chain for current species"""
    species_data = context.pokemon_page.parse_response_data()
    evolution_url = species_data["evolution_chain"]["url"]
    chain_id = context.functions.extract_id_from_url(evolution_url)
    context.pokemon_page.api.get_evolution_chain(chain_id)

@then('the response status should be {expected_status:d}')
@allure.step("Validate response status code: {expected_status}")
def step_validate_status(context, expected_status):
    """Validate response status code"""
    actual_status = context.pokemon_page.last_response.status_code
    allure.attach(f"Expected: {expected_status}, Actual: {actual_status}", "Status Code Validation", allure.attachment_type.TEXT)
    assert context.pokemon_page.validate_response_status(expected_status), \
        f"Expected status {expected_status}, got {actual_status}"

@then('the response time should be less than {max_time:d} seconds')
@allure.step("Validate response time < {max_time} seconds")
def step_validate_response_time(context, max_time):
    """Validate response time"""
    response_time = context.pokemon_page.last_response.elapsed.total_seconds()
    allure.attach(f"Response time: {response_time:.3f}s (limit: {max_time}s)", "Response Time", allure.attachment_type.TEXT)
    assert context.pokemon_page.validate_response_time(float(max_time)), \
        f"Response time {response_time:.3f}s exceeded {max_time} seconds"

@then('the response should contain valid Pokemon data')
@allure.step("Validate Pokemon response schema")
def step_validate_pokemon_data(context):
    """Validate Pokemon response structure"""
    with allure.step("Validating Pokemon response against JSON schema"):
        assert context.pokemon_page.validate_pokemon_schema(), \
            "Pokemon response does not match expected schema"

@then('the response should contain valid ability data')
@allure.step("Validate ability response schema")
def step_validate_ability_data(context):
    """Validate ability response structure"""
    with allure.step("Validating ability response against JSON schema"):
        assert context.pokemon_page.validate_ability_schema(), \
            "Ability response does not match expected schema"

@then('the Pokemon ID should be {expected_id:d}')
@allure.step("Validate Pokemon ID: {expected_id}")
def step_validate_pokemon_id(context, expected_id):
    """Validate Pokemon ID"""
    actual_id = context.pokemon_page.get_pokemon_id()
    allure.attach(f"Expected ID: {expected_id}, Actual ID: {actual_id}", "Pokemon ID Validation", allure.attachment_type.TEXT)
    assert actual_id == expected_id, f"Expected ID {expected_id}, got {actual_id}"

@then('the Pokemon name should be "{expected_name}"')
@allure.step("Validate Pokemon name: {expected_name}")
def step_validate_pokemon_name(context, expected_name):
    """Validate Pokemon name"""
    actual_name = context.pokemon_page.get_pokemon_name()
    allure.attach(f"Expected name: {expected_name}, Actual name: {actual_name}", "Pokemon Name Validation", allure.attachment_type.TEXT)
    assert actual_name == expected_name, f"Expected name {expected_name}, got {actual_name}"

@then('the response should contain required fields')
@allure.step("Validate required fields presence")
def step_validate_required_fields(context):
    """Validate required fields are present"""
    required_fields = [row['field'] for row in context.table]
    allure.attach(f"Required fields: {required_fields}", "Field Validation", allure.attachment_type.TEXT)
    assert context.pokemon_page.validate_required_fields(required_fields), \
        f"Missing required fields from response"

@then('the ability response should contain required fields')
@allure.step("Validate ability required fields")
def step_validate_ability_required_fields(context):
    """Validate ability required fields are present"""
    required_fields = [row['field'] for row in context.table]
    allure.attach(f"Required fields: {required_fields}", "Ability Field Validation", allure.attachment_type.TEXT)
    assert context.pokemon_page.validate_required_fields(required_fields), \
        f"Missing required fields from ability response"

@then('the Pokemon should have at least one ability')
@allure.step("Validate Pokemon has abilities")
def step_validate_pokemon_abilities(context):
    """Validate Pokemon has abilities"""
    assert context.pokemon_page.validate_pokemon_has_abilities(), \
        "Pokemon should have at least one ability"

@then('the Pokemon should have at least one type')
@allure.step("Validate Pokemon has types")
def step_validate_pokemon_types(context):
    """Validate Pokemon has types"""
    assert context.pokemon_page.validate_pokemon_has_types(), \
        "Pokemon should have at least one type"

@then('the response should contain {count:d} Pokemon entries')
@allure.step("Validate Pokemon list count: {count}")
def step_validate_pokemon_count(context, count):
    """Validate Pokemon list count"""
    data = context.pokemon_page.parse_response_data()
    actual_count = len(data.get("results", []))
    allure.attach(f"Expected count: {count}, Actual count: {actual_count}", "Pokemon Count Validation", allure.attachment_type.TEXT)
    assert actual_count == count, f"Expected {count} Pokemon, got {actual_count}"

@then('the evolution chain should contain species information')
@allure.step("Validate evolution chain structure")
def step_validate_evolution_chain(context):
    """Validate evolution chain structure"""
    data = context.pokemon_page.parse_response_data()
    assert "chain" in data, "Evolution chain should contain 'chain' field"
    assert "species" in data["chain"], "Evolution chain should contain species information"