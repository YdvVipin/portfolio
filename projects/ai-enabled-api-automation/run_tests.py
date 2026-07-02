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
    """Run quick smoke tests"""
    print("🔥 Running Smoke Tests...")
    cmd = ["pytest", "test_pokemon_api.py::TestPokemonAPI::test_get_pokemon_by_name_valid", "-v"]
    return subprocess.run(cmd)

def run_regression_tests():
    """Run full regression test suite"""
    print("🧪 Running Regression Tests...")
    cmd = ["pytest", "test_pokemon_api.py", "-v"]
    return subprocess.run(cmd)

def run_performance_tests():
    """Run performance tests"""
    print("⚡ Running Performance Tests...")
    cmd = ["pytest", "test_performance.py", "-v"]
    return subprocess.run(cmd)

def run_all_tests():
    """Run all tests"""
    print("🚀 Running All Tests...")
    cmd = ["pytest", "-v"]
    return subprocess.run(cmd)

def main():
    parser = argparse.ArgumentParser(description="PokéAPI Test Runner")
    parser.add_argument("--suite", choices=["smoke", "regression", "performance", "all"], 
                       default="all", help="Test suite to run")
    parser.add_argument("--install-deps", action="store_true", 
                       help="Install dependencies before running tests")
    
    args = parser.parse_args()
    
    # Install dependencies if requested
    if args.install_deps:
        print("📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Create reports directory
    create_reports_dir()
    
    # Run selected test suite
    print(f"\n🎯 Starting test execution at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if args.suite == "smoke":
        result = run_smoke_tests()
    elif args.suite == "regression":
        result = run_regression_tests()
    elif args.suite == "performance":
        result = run_performance_tests()
    else:
        result = run_all_tests()
    
    print(f"\n✅ Test execution completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Check reports/ directory for detailed results")
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())