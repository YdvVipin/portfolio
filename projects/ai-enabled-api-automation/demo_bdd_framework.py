#!/usr/bin/env python3
"""
BDD Framework Demo Script
Demonstrates the PokéAPI BDD automation framework capabilities
"""

import subprocess
import sys
import os
from datetime import datetime

def print_header():
    """Print demo header"""
    print("🎮" + "="*60)
    print("    PokéAPI BDD Automation Framework Demo")
    print("="*62)
    print(f"    Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*62)

def demo_smoke_tests():
    """Demo smoke tests"""
    print("\n🔥 DEMO 1: Smoke Tests")
    print("-" * 30)
    print("Testing basic Pokemon and Ability retrieval...")
    
    result = subprocess.run([
        sys.executable, "run_bdd_tests.py", "--suite", "smoke"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Smoke tests PASSED")
        print("   - Pokemon retrieval by ID and name")
        print("   - Ability retrieval by identifier")
        print("   - Response time validation")
    else:
        print("❌ Smoke tests FAILED")

def demo_negative_tests():
    """Demo negative tests"""
    print("\n❌ DEMO 2: Negative Tests")
    print("-" * 30)
    print("Testing error handling with invalid inputs...")
    
    result = subprocess.run([
        sys.executable, "run_bdd_tests.py", "--suite", "negative"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Negative tests PASSED")
        print("   - Invalid Pokemon IDs return 404")
        print("   - Invalid Pokemon names return 404")
        print("   - Proper error handling validated")
    else:
        print("❌ Negative tests FAILED")

def demo_validation_tests():
    """Demo validation tests"""
    print("\n🔍 DEMO 3: Validation Tests")
    print("-" * 30)
    print("Testing response structure and schema validation...")
    
    result = subprocess.run([
        sys.executable, "run_bdd_tests.py", "--suite", "validation"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Validation tests PASSED")
        print("   - JSON schema validation")
        print("   - Required fields verification")
        print("   - Data structure validation")
    else:
        print("❌ Validation tests FAILED")

def demo_performance_tests():
    """Demo performance tests"""
    print("\n⚡ DEMO 4: Performance Tests")
    print("-" * 30)
    print("Testing API response times...")
    
    result = subprocess.run([
        sys.executable, "run_bdd_tests.py", "--suite", "performance"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Performance tests PASSED")
        print("   - Response times under acceptable limits")
        print("   - Multiple endpoint performance validated")
        print("   - Pagination performance tested")
    else:
        print("❌ Performance tests FAILED")

def show_reports():
    """Show generated reports"""
    print("\n📊 DEMO 5: Generated Reports")
    print("-" * 30)
    
    reports_dir = "reports"
    if os.path.exists(reports_dir):
        reports = [f for f in os.listdir(reports_dir) if f.endswith('.html')]
        if reports:
            print("HTML Reports generated:")
            for report in reports:
                print(f"   📄 {report}")
            print(f"\n   📁 All reports available in: {os.path.abspath(reports_dir)}")
        else:
            print("   No HTML reports found")
    else:
        print("   Reports directory not found")

def show_framework_features():
    """Show framework features"""
    print("\n🎯 BDD Framework Features Demonstrated:")
    print("-" * 45)
    print("✅ Gherkin Feature Files - Natural language scenarios")
    print("✅ Page Object Pattern - Encapsulated API operations")
    print("✅ API Collections - Organized endpoint methods")
    print("✅ Reusable Functions - Common utility operations")
    print("✅ Data-Driven Testing - JSON test data management")
    print("✅ Tag-Based Execution - Flexible test categorization")
    print("✅ Comprehensive Reporting - HTML and XML reports")
    print("✅ Response Validation - Schema and structure checks")
    print("✅ Performance Testing - Response time validation")
    print("✅ Error Handling - Negative scenario testing")

def main():
    """Main demo function"""
    print_header()
    
    # Run demo test suites
    demo_smoke_tests()
    demo_negative_tests()
    demo_validation_tests()
    demo_performance_tests()
    
    # Show reports and features
    show_reports()
    show_framework_features()
    
    print("\n🎉 BDD Framework Demo Completed!")
    print("="*62)
    print("💡 To run individual test suites:")
    print("   python3 run_bdd_tests.py --suite smoke")
    print("   python3 run_bdd_tests.py --suite negative")
    print("   python3 run_bdd_tests.py --suite validation")
    print("   python3 run_bdd_tests.py --suite performance")
    print("   python3 run_bdd_tests.py --suite all")
    print("="*62)

if __name__ == "__main__":
    main()