import logging
import time
import json
import os
from behave import fixture, use_fixture
from pages.pokemon_page import PokemonPage
import allure

# Global variables to collect metrics
test_metrics = {
    'scenarios': [],
    'performance_data': [],
    'start_time': None,
    'end_time': None
}

def before_all(context):
    """Setup before all tests"""
    global test_metrics
    test_metrics['start_time'] = time.time()
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize shared resources
    context.config.setup_logging()
    context.test_metrics = test_metrics

def before_scenario(context, scenario):
    """Setup before each scenario"""
    # Initialize page objects for each scenario
    context.pokemon_page = PokemonPage()
    context.scenario_start_time = time.time()
    
    # Log scenario start
    logging.info(f"Starting scenario: {scenario.name}")

def after_scenario(context, scenario):
    """Cleanup after each scenario"""
    global test_metrics
    
    # Calculate scenario execution time
    scenario_time = time.time() - context.scenario_start_time
    
    # Collect scenario metrics
    scenario_data = {
        'name': scenario.name,
        'status': scenario.status.name,
        'duration': scenario_time,
        'tags': [tag for tag in scenario.tags],
        'feature': scenario.feature.name
    }
    
    test_metrics['scenarios'].append(scenario_data)
    
    # Collect performance data if available
    if hasattr(context, 'pokemon_page') and context.pokemon_page.last_response:
        response_time = context.pokemon_page.last_response.elapsed.total_seconds()
        test_metrics['performance_data'].append({
            'scenario': scenario.name,
            'response_time': response_time,
            'status_code': context.pokemon_page.last_response.status_code
        })
        
        # Attach response details to Allure
        allure.attach(
            f"Status Code: {context.pokemon_page.last_response.status_code}\n"
            f"Response Time: {response_time:.3f}s\n"
            f"Response Size: {len(context.pokemon_page.last_response.content)} bytes",
            "API Response Details",
            allure.attachment_type.TEXT
        )
        
        # Attach response body if it's JSON
        try:
            response_json = context.pokemon_page.last_response.json()
            allure.attach(
                json.dumps(response_json, indent=2),
                "Response Body",
                allure.attachment_type.JSON
            )
        except:
            allure.attach(
                context.pokemon_page.last_response.text,
                "Response Body",
                allure.attachment_type.TEXT
            )
    
    # Log scenario completion
    status = "PASSED" if scenario.status.name == "passed" else "FAILED"
    logging.info(f"Scenario {scenario.name} - {status}")
    
    # Clean up any resources if needed
    if hasattr(context, 'pokemon_page'):
        context.pokemon_page = None

def after_all(context):
    """Cleanup after all tests"""
    global test_metrics
    test_metrics['end_time'] = time.time()
    
    # Save metrics to file for report generation
    metrics_file = "reports/test_metrics.json"
    os.makedirs("reports", exist_ok=True)
    
    with open(metrics_file, 'w') as f:
        json.dump(test_metrics, f, indent=2)
    
    logging.info("All BDD tests completed")
    logging.info(f"Test metrics saved to {metrics_file}")