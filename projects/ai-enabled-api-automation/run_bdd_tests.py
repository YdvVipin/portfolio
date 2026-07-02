#!/usr/bin/env python3
import subprocess
import sys
import os
import argparse
from datetime import datetime

def create_reports_dir():
    """Create reports directory if it doesn't exist"""
    if not os.path.exists("reports"):
        os.makedirs("reports")

def run_smoke_tests():
    """Run smoke tests"""
    print("🔥 Running BDD Smoke Tests...")
    cmd = [sys.executable, "-m", "behave", "--tags=@smoke", "-f", "allure_behave.formatter:AllureFormatter", "-o", "reports/allure-results", "-f", "pretty"]
    return subprocess.run(cmd)

def run_negative_tests():
    """Run negative tests"""
    print("❌ Running BDD Negative Tests...")
    cmd = [sys.executable, "-m", "behave", "--tags=@negative", "-f", "allure_behave.formatter:AllureFormatter", "-o", "reports/allure-results", "-f", "pretty"]
    return subprocess.run(cmd)

def run_performance_tests():
    """Run performance tests"""
    print("⚡ Running BDD Performance Tests...")
    cmd = [sys.executable, "-m", "behave", "--tags=@performance", "-f", "allure_behave.formatter:AllureFormatter", "-o", "reports/allure-results", "-f", "pretty"]
    return subprocess.run(cmd)

def run_validation_tests():
    """Run validation tests"""
    print("✅ Running BDD Validation Tests...")
    cmd = [sys.executable, "-m", "behave", "--tags=@validation", "-f", "allure_behave.formatter:AllureFormatter", "-o", "reports/allure-results", "-f", "pretty"]
    return subprocess.run(cmd)

def run_integration_tests():
    """Run integration tests"""
    print("🔗 Running BDD Integration Tests...")
    cmd = [sys.executable, "-m", "behave", "--tags=@integration", "-f", "allure_behave.formatter:AllureFormatter", "-o", "reports/allure-results", "-f", "pretty"]
    return subprocess.run(cmd)

def run_all_tests():
    """Run all BDD tests"""
    print("🚀 Running All BDD Tests...")
    cmd = [sys.executable, "-m", "behave", "-f", "allure_behave.formatter:AllureFormatter", "-o", "reports/allure-results", "-f", "pretty"]
    return subprocess.run(cmd)

def run_specific_feature(feature_name):
    """Run specific feature file"""
    print(f"🎯 Running Feature: {feature_name}")
    cmd = [sys.executable, "-m", "behave", f"features/{feature_name}.feature", "-f", "allure_behave.formatter:AllureFormatter", "-o", "reports/allure-results", "-f", "pretty"]
    return subprocess.run(cmd)

def main():
    parser = argparse.ArgumentParser(description="PokéAPI BDD Test Runner")
    parser.add_argument("--suite", choices=["smoke", "negative", "performance", "validation", "integration", "all"], 
                       default="all", help="Test suite to run")
    parser.add_argument("--feature", help="Specific feature file to run (without .feature extension)")
    parser.add_argument("--install-deps", action="store_true", 
                       help="Install dependencies before running tests")
    parser.add_argument("--tags", help="Run tests with specific tags (e.g., @smoke,@negative)")
    
    args = parser.parse_args()
    
    # Install dependencies if requested
    if args.install_deps:
        print("📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Create reports directory
    create_reports_dir()
    
    print(f"\n🎯 Starting BDD test execution at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run specific feature if provided
    if args.feature:
        result = run_specific_feature(args.feature)
    # Run tests with specific tags if provided
    elif args.tags:
        print(f"🏷️ Running tests with tags: {args.tags}")
        cmd = [sys.executable, "-m", "behave", f"--tags={args.tags}", "-f", "allure_behave.formatter:AllureFormatter", "-o", "reports/allure-results", "-f", "pretty"]
        result = subprocess.run(cmd)
    # Run selected test suite
    elif args.suite == "smoke":
        result = run_smoke_tests()
    elif args.suite == "negative":
        result = run_negative_tests()
    elif args.suite == "performance":
        result = run_performance_tests()
    elif args.suite == "validation":
        result = run_validation_tests()
    elif args.suite == "integration":
        result = run_integration_tests()
    else:
        result = run_all_tests()
    
    print(f"\n✅ BDD test execution completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Check reports/allure-results for test data")
    
    # Generate Allure report
    print("\n📈 Generating Allure HTML report...")
    try:
        allure_cmd = ["allure", "generate", "reports/allure-results", "-o", "reports/allure-report", "--clean"]
        subprocess.run(allure_cmd, check=True)
        print("✅ Allure report generated: reports/allure-report/index.html")
        print("🔗 To serve report: allure serve reports/allure-results")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️ Allure CLI not found. Install with: npm install -g allure-commandline")
        print("📁 Raw results available in: reports/allure-results")
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())