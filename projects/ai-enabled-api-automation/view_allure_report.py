#!/usr/bin/env python3
"""
Allure Report Viewer for PokéAPI BDD Framework
"""

import subprocess
import sys
import os
import webbrowser
import time

def check_allure_installation():
    """Check if Allure CLI is installed"""
    try:
        result = subprocess.run(["allure", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Allure CLI found: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Allure CLI not found!")
    print("📦 Install with: npm install -g allure-commandline")
    print("🔗 Or download from: https://github.com/allure-framework/allure2/releases")
    return False

def generate_allure_report():
    """Generate Allure HTML report"""
    if not os.path.exists("reports/allure-results"):
        print("❌ No Allure results found!")
        print("💡 Run tests first: python3 run_bdd_tests.py --suite smoke")
        return False
    
    print("📊 Generating Allure HTML report...")
    try:
        cmd = ["allure", "generate", "reports/allure-results", "-o", "reports/allure-report", "--clean"]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Allure report generated successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating report: {e}")
        return False

def serve_allure_report():
    """Serve Allure report with built-in server"""
    if not os.path.exists("reports/allure-results"):
        print("❌ No Allure results found!")
        print("💡 Run tests first: python3 run_bdd_tests.py --suite smoke")
        return False
    
    print("🚀 Starting Allure server...")
    print("📊 Report will open in your browser automatically")
    print("🛑 Press Ctrl+C to stop the server")
    
    try:
        cmd = ["allure", "serve", "reports/allure-results"]
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 Allure server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error serving report: {e}")

def open_static_report():
    """Open static Allure report in browser"""
    report_path = "reports/allure-report/index.html"
    
    if not os.path.exists(report_path):
        print("❌ Static report not found!")
        if generate_allure_report():
            if os.path.exists(report_path):
                print("✅ Report generated successfully!")
            else:
                return False
        else:
            return False
    
    abs_path = os.path.abspath(report_path)
    file_url = f"file://{abs_path}"
    
    print(f"🌐 Opening Allure report: {file_url}")
    
    try:
        webbrowser.open(file_url)
        print("✅ Report opened in default browser")
        return True
    except Exception as e:
        print(f"❌ Error opening report: {e}")
        print(f"📁 Manual path: {abs_path}")
        return False

def list_available_results():
    """List available Allure results"""
    results_dir = "reports/allure-results"
    
    if not os.path.exists(results_dir):
        print("❌ No Allure results directory found!")
        return
    
    files = os.listdir(results_dir)
    if not files:
        print("❌ No Allure result files found!")
        return
    
    print("📊 Available Allure Results:")
    print("-" * 40)
    
    for file in sorted(files):
        if file.endswith('.json'):
            size = os.path.getsize(os.path.join(results_dir, file))
            print(f"   📄 {file} ({size:,} bytes)")

def main():
    """Main function"""
    print("🎮 PokéAPI BDD - Allure Report Viewer")
    print("=" * 45)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--serve":
            if check_allure_installation():
                serve_allure_report()
        elif command == "--generate":
            if check_allure_installation():
                generate_allure_report()
        elif command == "--open":
            if check_allure_installation():
                open_static_report()
        elif command == "--list":
            list_available_results()
        elif command == "--help":
            print("📖 Available commands:")
            print("   --serve     Start Allure server (recommended)")
            print("   --generate  Generate static HTML report")
            print("   --open      Open static report in browser")
            print("   --list      List available result files")
            print("   --help      Show this help message")
        else:
            print(f"❌ Unknown command: {command}")
            print("💡 Use --help to see available commands")
    else:
        # Default behavior - try to serve report
        if check_allure_installation():
            serve_allure_report()
        else:
            list_available_results()

if __name__ == "__main__":
    main()