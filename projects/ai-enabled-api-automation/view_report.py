#!/usr/bin/env python3
"""
Script to open the detailed HTML report in the default browser
"""

import os
import webbrowser
import sys

def open_detailed_report():
    """Open the detailed HTML report in browser"""
    report_path = "reports/detailed_report.html"
    
    if not os.path.exists(report_path):
        print("❌ Detailed report not found!")
        print("💡 Run tests first: python3 run_bdd_tests.py --suite smoke")
        return False
    
    # Get absolute path
    abs_path = os.path.abspath(report_path)
    file_url = f"file://{abs_path}"
    
    print(f"🌐 Opening detailed report: {file_url}")
    
    try:
        webbrowser.open(file_url)
        print("✅ Report opened in default browser")
        return True
    except Exception as e:
        print(f"❌ Error opening report: {e}")
        print(f"📁 Manual path: {abs_path}")
        return False

def list_available_reports():
    """List all available reports"""
    reports_dir = "reports"
    
    if not os.path.exists(reports_dir):
        print("❌ Reports directory not found!")
        return
    
    print("📊 Available Reports:")
    print("-" * 30)
    
    html_reports = []
    other_reports = []
    
    for file in os.listdir(reports_dir):
        if file.endswith('.html'):
            html_reports.append(file)
        elif file.endswith(('.xml', '.json', '.txt')):
            other_reports.append(file)
    
    if html_reports:
        print("🌐 HTML Reports:")
        for report in sorted(html_reports):
            size = os.path.getsize(os.path.join(reports_dir, report))
            print(f"   📄 {report} ({size:,} bytes)")
    
    if other_reports:
        print("\n📋 Other Reports:")
        for report in sorted(other_reports):
            size = os.path.getsize(os.path.join(reports_dir, report))
            print(f"   📄 {report} ({size:,} bytes)")

def main():
    """Main function"""
    print("🎮 PokéAPI BDD Report Viewer")
    print("=" * 40)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        list_available_reports()
    else:
        if not open_detailed_report():
            print("\n📋 Available reports:")
            list_available_reports()

if __name__ == "__main__":
    main()