#!/usr/bin/env python3
"""
Test Runner for SQL Data Generator
===================================
Runs all unit and integration tests with detailed reporting
"""

import unittest
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test modules
from tests.test_all_features import (
    TestConfig, TestSQLDataGenerator, TestMultiCoreGenerator,
    TestPerformanceMonitor, TestValidators, TestDatabaseManagers
)
from tests.test_integration import (
    TestEndToEndWorkflow, TestDataIntegrity, 
    TestErrorHandling, TestPerformance
)


def print_header(title):
    """Print formatted header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def print_section(title):
    """Print formatted section"""
    print("\n" + "-"*80)
    print(f"  {title}")
    print("-"*80)


def run_all_tests():
    """Run all tests with comprehensive reporting"""
    
    print_header("SQL DATA GENERATOR - COMPREHENSIVE TEST SUITE")
    print(f"Test Run Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Unit Tests
    print_section("UNIT TESTS")
    
    unit_test_classes = [
        ("Configuration Tests", TestConfig),
        ("SQL Data Generator Tests", TestSQLDataGenerator),
        ("Multi-Core Generator Tests", TestMultiCoreGenerator),
        ("Performance Monitor Tests", TestPerformanceMonitor),
        ("Validator Tests", TestValidators),
        ("Database Manager Tests", TestDatabaseManagers)
    ]
    
    for name, test_class in unit_test_classes:
        print(f"\n📋 {name}")
        suite.addTests(loader.loadTestsFromTestCase(test_class))
    
    # Integration Tests
    print_section("INTEGRATION TESTS")
    
    integration_test_classes = [
        ("End-to-End Workflow Tests", TestEndToEndWorkflow),
        ("Data Integrity Tests", TestDataIntegrity),
        ("Error Handling Tests", TestErrorHandling),
        ("Performance Tests", TestPerformance)
    ]
    
    for name, test_class in integration_test_classes:
        print(f"\n📋 {name}")
        suite.addTests(loader.loadTestsFromTestCase(test_class))
    
    # Run all tests
    print_section("RUNNING ALL TESTS")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Calculate statistics
    total_tests = result.testsRun
    successes = total_tests - len(result.failures) - len(result.errors)
    failures = len(result.failures)
    errors = len(result.errors)
    success_rate = (successes / total_tests * 100) if total_tests > 0 else 0
    
    # Print detailed summary
    print_header("TEST RESULTS SUMMARY")
    
    print(f"📊 Total Tests Run:     {total_tests}")
    print(f"✅ Successful Tests:    {successes}")
    print(f"❌ Failed Tests:        {failures}")
    print(f"⚠️  Errors:              {errors}")
    print(f"📈 Success Rate:        {success_rate:.1f}%")
    
    # Test categories breakdown
    print_section("TEST CATEGORIES BREAKDOWN")
    
    print(f"Unit Tests:        {len(unit_test_classes)} categories")
    print(f"Integration Tests: {len(integration_test_classes)} categories")
    print(f"Total Categories:  {len(unit_test_classes) + len(integration_test_classes)}")
    
    # Feature coverage
    print_section("FEATURE COVERAGE")
    
    features = [
        "✅ Configuration Management",
        "✅ Data Generation (Users, Products, Orders)",
        "✅ SQL Statement Generation (INSERT, UPDATE, DELETE)",
        "✅ Batch Processing",
        "✅ Multi-Core Processing",
        "✅ Performance Monitoring",
        "✅ Input Validation",
        "✅ Error Handling",
        "✅ Database Managers (MySQL, PostgreSQL, MongoDB)",
        "✅ Data Integrity Checks",
        "✅ SQL Injection Prevention",
        "✅ End-to-End Workflows"
    ]
    
    for feature in features:
        print(f"  {feature}")
    
    # Detailed failure report
    if failures > 0 or errors > 0:
        print_section("FAILURE DETAILS")
        
        if failures > 0:
            print("\n❌ FAILURES:")
            for test, traceback in result.failures:
                print(f"\n  Test: {test}")
                print(f"  {traceback}")
        
        if errors > 0:
            print("\n⚠️  ERRORS:")
            for test, traceback in result.errors:
                print(f"\n  Test: {test}")
                print(f"  {traceback}")
    
    # Final verdict
    print_section("FINAL VERDICT")
    
    if success_rate == 100:
        print("🎉 ALL TESTS PASSED! Application is ready for production.")
    elif success_rate >= 90:
        print("✅ Most tests passed. Minor issues detected.")
    elif success_rate >= 70:
        print("⚠️  Some tests failed. Review and fix issues.")
    else:
        print("❌ Many tests failed. Significant issues detected.")
    
    print(f"\nTest Run Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")
    
    # Return exit code
    return 0 if success_rate == 100 else 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
