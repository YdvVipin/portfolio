# PokéAPI BDD Automation Framework with Allure Reporting

A comprehensive BDD (Behavior-Driven Development) API automation testing framework built for the PokéAPI using Behave and Allure reporting.

## 🚀 Features

- **BDD Architecture**: Feature files, step definitions, and page objects
- **Allure Reporting**: Rich interactive reports with charts, graphs, and attachments
- **Modular Design**: Separate API collections, page objects, and utilities
- **Comprehensive Testing**: Smoke, negative, performance, validation, and integration tests
- **Reusable Functions**: Common operations abstracted into reusable components
- **Data-Driven**: JSON-based test data management
- **Step Attachments**: API response details and JSON payloads in reports
- **Tag-Based Execution**: Run specific test categories using tags

## 📁 Project Structure

```
AiEnabledAPIAutomation/
├── features/
│   ├── pokemon_api.feature      # Pokemon API scenarios
│   ├── abilities_api.feature    # Abilities API scenarios
│   ├── performance.feature      # Performance test scenarios
│   ├── environment.py           # Behave hooks and Allure attachments
│   └── steps/
│       └── pokemon_steps.py     # Step definitions with Allure decorators
├── pages/
│   └── pokemon_page.py          # Page object for Pokemon operations
├── api_collections/
│   └── pokemon_api.py           # API endpoint collections
├── utils/
│   └── bdd_utils.py             # BDD-specific utilities
├── data/
│   └── test_data.json           # Test data in JSON format
├── reusable_functions.py        # Common reusable functions
├── run_bdd_tests.py            # BDD test runner with Allure integration
├── view_allure_report.py       # Allure report viewer
└── reports/                    # Generated reports
    ├── allure-results/         # Raw Allure test data
    └── allure-report/          # Generated HTML report
```

## 🛠️ Setup & Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Allure CLI** (for report generation):
   ```bash
   npm install -g allure-commandline
   ```

3. **Run Tests**:
   ```bash
   # Run all tests
   python3 run_bdd_tests.py --suite all

   # Run specific test suites
   python3 run_bdd_tests.py --suite smoke
   python3 run_bdd_tests.py --suite negative
   python3 run_bdd_tests.py --suite performance
   python3 run_bdd_tests.py --suite validation

   # Run with tags
   python3 run_bdd_tests.py --tags @smoke,@negative
   ```

4. **View Allure Reports**:
   ```bash
   # Serve interactive report (recommended)
   python3 view_allure_report.py --serve
   
   # Generate static HTML report
   python3 view_allure_report.py --generate
   
   # Open static report in browser
   python3 view_allure_report.py --open
   ```

## 🧪 Test Categories

- **@smoke** - Basic functionality tests
- **@negative** - Error handling tests  
- **@performance** - Response time tests
- **@validation** - Schema and structure tests
- **@integration** - Multi-endpoint tests

## 📊 Allure Report Features

- **Interactive Dashboard**: Visual charts and graphs
- **Step-by-Step Execution**: Detailed test execution flow
- **Rich Attachments**: API responses, performance metrics, error details
- **Timeline View**: Chronological test execution
- **Filterable Results**: By tags, features, and status

This BDD framework with Allure reporting provides comprehensive API testing capabilities with rich, interactive reports! 🎮✨