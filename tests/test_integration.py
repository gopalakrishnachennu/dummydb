"""
Integration Tests for SQL Data Generator
=========================================
Tests end-to-end workflows and integration between components
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import Config
from core.generator import SQLDataGenerator
from utils.validators import validate_connection, validate_schema


class TestEndToEndWorkflow(unittest.TestCase):
    """Test complete workflows"""
    
    def test_user_data_generation_workflow(self):
        """Test complete user data generation workflow"""
        # 1. Initialize generator
        generator = SQLDataGenerator(seed=42)
        
        # 2. Generate user data
        user = generator.generate_user()
        self.assertIsNotNone(user)
        
        # 3. Generate INSERT statement
        insert_stmt = generator.generate_insert_statement("users", user)
        self.assertTrue(insert_stmt.startswith("INSERT INTO users"))
        
        # 4. Generate UPDATE statement
        update_stmt = generator.generate_update_statement("users", user)
        self.assertTrue(update_stmt.startswith("UPDATE users"))
        
        # 5. Generate DELETE statement
        delete_stmt = generator.generate_delete_statement("users", user["id"])
        self.assertTrue(delete_stmt.startswith("DELETE FROM users"))
    
    def test_batch_generation_workflow(self):
        """Test batch generation workflow"""
        generator = SQLDataGenerator(seed=42)
        
        # Generate batch of different operations
        for operation in ["insert", "update", "delete"]:
            statements = generator.generate_batch("user", 10, operation)
            self.assertEqual(len(statements), 10)
            
            for stmt in statements:
                self.assertIsInstance(stmt, str)
                self.assertTrue(stmt.endswith(";"))
    
    def test_multi_table_generation(self):
        """Test generation across multiple tables"""
        generator = SQLDataGenerator(seed=42)
        
        # Generate data for all table types
        tables = ["user", "product", "order"]
        
        for table in tables:
            statements = generator.generate_batch(table, 5, "insert")
            self.assertEqual(len(statements), 5)
    
    def test_schema_validation_workflow(self):
        """Test schema validation workflow"""
        # Get schema from config
        schema = Config.get_table_schema("users")
        
        # Validate schema
        result = validate_schema(schema)
        self.assertTrue(result["valid"], f"Schema validation failed: {result.get('errors')}")
    
    def test_configuration_to_generation(self):
        """Test using configuration for generation"""
        # Get all tables from config
        tables = Config.get_all_tables()
        
        generator = SQLDataGenerator()
        
        # Generate data for each configured table
        for table in tables:
            schema = Config.get_table_schema(table)
            self.assertIsNotNone(schema)
            
            # Generate appropriate data
            if table == "users":
                data = generator.generate_user()
            elif table == "products":
                data = generator.generate_product()
            elif table == "orders":
                data = generator.generate_order()
            
            self.assertIsNotNone(data)


class TestDataIntegrity(unittest.TestCase):
    """Test data integrity and consistency"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = SQLDataGenerator(seed=42)
    
    def test_user_email_format(self):
        """Test user email format consistency"""
        for _ in range(10):
            user = self.generator.generate_user()
            email = user["email"]
            
            # Check email format
            self.assertIn("@", email)
            self.assertRegex(email, r'.+@.+\..+')
    
    def test_product_price_validity(self):
        """Test product price validity"""
        for _ in range(10):
            product = self.generator.generate_product()
            price = product["price"]
            
            # Price should be positive
            self.assertGreater(price, 0)
            # Price should have max 2 decimal places
            self.assertEqual(price, round(price, 2))
    
    def test_order_calculations(self):
        """Test order calculation accuracy"""
        for _ in range(10):
            order = self.generator.generate_order()
            
            # Verify subtotal
            expected_subtotal = round(order["quantity"] * order["unit_price"], 2)
            self.assertAlmostEqual(order["subtotal"], expected_subtotal, places=2)
            
            # Verify tax (8%)
            expected_tax = round(order["subtotal"] * 0.08, 2)
            self.assertAlmostEqual(order["tax"], expected_tax, places=2)
            
            # Verify total
            expected_total = round(order["subtotal"] + order["tax"], 2)
            self.assertAlmostEqual(order["total"], expected_total, places=2)
    
    def test_uuid_uniqueness(self):
        """Test UUID uniqueness"""
        uuids = set()
        
        for _ in range(100):
            uuid = self.generator.generate_uuid()
            self.assertNotIn(uuid, uuids, "UUID should be unique")
            uuids.add(uuid)
    
    def test_sql_injection_prevention(self):
        """Test SQL injection prevention in statements"""
        # Create data with potential SQL injection
        malicious_data = {
            "id": "1' OR '1'='1",
            "name": "Robert'); DROP TABLE users;--",
            "email": "test@test.com"
        }
        
        stmt = self.generator.generate_insert_statement("users", malicious_data)
        
        # Check that quotes are properly escaped
        self.assertIn("''", stmt)  # Single quotes should be doubled


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = SQLDataGenerator()
    
    def test_invalid_data_type(self):
        """Test handling of invalid data type"""
        with self.assertRaises(ValueError):
            self.generator.generate_batch("invalid_type", 10, "insert")
    
    def test_invalid_operation(self):
        """Test handling of invalid operation"""
        with self.assertRaises(ValueError):
            self.generator.generate_batch("user", 10, "invalid_operation")
    
    def test_zero_count_batch(self):
        """Test batch generation with zero count"""
        statements = self.generator.generate_batch("user", 0, "insert")
        self.assertEqual(len(statements), 0)
    
    def test_large_batch_generation(self):
        """Test large batch generation"""
        # This should not crash or timeout
        statements = self.generator.generate_batch("user", 1000, "insert")
        self.assertEqual(len(statements), 1000)


class TestPerformance(unittest.TestCase):
    """Test performance characteristics"""
    
    def test_generation_speed(self):
        """Test data generation speed"""
        import time
        
        generator = SQLDataGenerator()
        
        start_time = time.time()
        statements = generator.generate_batch("user", 100, "insert")
        duration = time.time() - start_time
        
        # Should generate 100 statements in less than 1 second
        self.assertLess(duration, 1.0, "Generation should be fast")
        self.assertEqual(len(statements), 100)
    
    def test_memory_efficiency(self):
        """Test memory efficiency"""
        import sys
        
        generator = SQLDataGenerator()
        
        # Generate large batch
        statements = generator.generate_batch("user", 1000, "insert")
        
        # Check memory usage is reasonable
        size = sys.getsizeof(statements)
        # Should be less than 10MB for 1000 statements
        self.assertLess(size, 10 * 1024 * 1024)


def run_integration_tests():
    """Run all integration tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestEndToEndWorkflow))
    suite.addTests(loader.loadTestsFromTestCase(TestDataIntegrity))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandling))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("INTEGRATION TEST SUMMARY")
    print("="*70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("="*70)
    
    return result


if __name__ == "__main__":
    run_integration_tests()
