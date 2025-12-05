"""
Comprehensive Unit Tests for SQL Data Generator
================================================
Tests all core functionality, database managers, generators, and validators
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import Config
from core.generator import SQLDataGenerator, MultiCoreGenerator, PerformanceMonitor
from utils.validators import validate_connection, validate_schema, format_error, get_table_icon


class TestConfig(unittest.TestCase):
    """Test Configuration Management"""
    
    def test_database_types(self):
        """Test database type definitions"""
        self.assertIn("MySQL", Config.DATABASE_TYPES)
        self.assertIn("PostgreSQL", Config.DATABASE_TYPES)
        self.assertIn("MongoDB", Config.DATABASE_TYPES)
        self.assertEqual(Config.DATABASE_TYPES["MySQL"], "mysql")
    
    def test_default_ports(self):
        """Test default port configurations"""
        self.assertEqual(Config.get_default_port("mysql"), 3306)
        self.assertEqual(Config.get_default_port("postgresql"), 5432)
        self.assertEqual(Config.get_default_port("mongodb"), 27017)
    
    def test_table_schemas(self):
        """Test table schema definitions"""
        self.assertIn("users", Config.TABLE_SCHEMAS)
        self.assertIn("products", Config.TABLE_SCHEMAS)
        self.assertIn("orders", Config.TABLE_SCHEMAS)
        
        # Check users schema
        users_schema = Config.get_table_schema("users")
        self.assertIn("columns", users_schema)
        self.assertGreater(len(users_schema["columns"]), 0)
        
        # Check for primary key
        has_primary = any(col.get("primary") for col in users_schema["columns"])
        self.assertTrue(has_primary, "Users table should have a primary key")
    
    def test_operation_types(self):
        """Test operation type definitions"""
        self.assertIn("➕ INSERT Only", Config.OPERATION_TYPES)
        self.assertIn("✏️ UPDATE Only", Config.OPERATION_TYPES)
        self.assertIn("🗑️ DELETE Only", Config.OPERATION_TYPES)
        self.assertIn("🎲 Random Mix", Config.OPERATION_TYPES)
    
    def test_performance_settings(self):
        """Test performance configuration"""
        self.assertEqual(Config.PERFORMANCE["min_ops_per_sec"], 1)
        self.assertEqual(Config.PERFORMANCE["max_ops_per_sec"], 100)
        self.assertGreater(Config.PERFORMANCE["batch_size"], 0)
    
    def test_port_validation(self):
        """Test port validation"""
        self.assertTrue(Config.validate_port(3306))
        self.assertTrue(Config.validate_port(5432))
        self.assertFalse(Config.validate_port(0))
        self.assertFalse(Config.validate_port(70000))
    
    def test_get_all_tables(self):
        """Test getting all table names"""
        tables = Config.get_all_tables()
        self.assertIsInstance(tables, list)
        self.assertIn("users", tables)
        self.assertIn("products", tables)
        self.assertIn("orders", tables)


class TestSQLDataGenerator(unittest.TestCase):
    """Test SQL Data Generator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = SQLDataGenerator(seed=42)
    
    def test_generate_uuid(self):
        """Test UUID generation"""
        uuid = self.generator.generate_uuid()
        self.assertIsInstance(uuid, str)
        self.assertEqual(len(uuid), 36)  # UUID format
        self.assertIn("-", uuid)
    
    def test_generate_integer(self):
        """Test integer generation"""
        num = self.generator.generate_integer(1, 100)
        self.assertIsInstance(num, int)
        self.assertGreaterEqual(num, 1)
        self.assertLessEqual(num, 100)
    
    def test_generate_float(self):
        """Test float generation"""
        num = self.generator.generate_float(0.0, 100.0, 2)
        self.assertIsInstance(num, float)
        self.assertGreaterEqual(num, 0.0)
        self.assertLessEqual(num, 100.0)
    
    def test_generate_datetime(self):
        """Test datetime generation"""
        dt = self.generator.generate_datetime()
        self.assertIsInstance(dt, str)
        # Should be in format YYYY-MM-DD HH:MM:SS
        self.assertRegex(dt, r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
    
    def test_generate_email(self):
        """Test email generation"""
        email = self.generator.generate_email()
        self.assertIsInstance(email, str)
        self.assertIn("@", email)
        self.assertRegex(email, r'.+@.+\..+')
    
    def test_generate_phone(self):
        """Test phone number generation"""
        phone = self.generator.generate_phone()
        self.assertIsInstance(phone, str)
        self.assertIn("(", phone)
        self.assertIn(")", phone)
        self.assertIn("-", phone)
    
    def test_generate_user(self):
        """Test user record generation"""
        user = self.generator.generate_user()
        
        # Check required fields
        required_fields = ["id", "username", "email", "first_name", "last_name", 
                          "phone", "city", "state", "country", "is_active", 
                          "created_at", "updated_at"]
        
        for field in required_fields:
            self.assertIn(field, user, f"User should have {field} field")
        
        # Check data types
        self.assertIsInstance(user["id"], str)
        self.assertIsInstance(user["username"], str)
        self.assertIsInstance(user["email"], str)
        self.assertIsInstance(user["is_active"], bool)
    
    def test_generate_product(self):
        """Test product record generation"""
        product = self.generator.generate_product()
        
        required_fields = ["id", "sku", "name", "category", "price", 
                          "stock_quantity", "is_available", "created_at", "updated_at"]
        
        for field in required_fields:
            self.assertIn(field, product, f"Product should have {field} field")
        
        # Check data types
        self.assertIsInstance(product["price"], float)
        self.assertIsInstance(product["stock_quantity"], int)
        self.assertIsInstance(product["is_available"], bool)
    
    def test_generate_order(self):
        """Test order record generation"""
        order = self.generator.generate_order()
        
        required_fields = ["id", "order_number", "user_id", "product_id", 
                          "quantity", "unit_price", "subtotal", "tax", "total",
                          "payment_method", "status", "created_at", "updated_at"]
        
        for field in required_fields:
            self.assertIn(field, order, f"Order should have {field} field")
        
        # Check calculations
        expected_subtotal = round(order["quantity"] * order["unit_price"], 2)
        self.assertAlmostEqual(order["subtotal"], expected_subtotal, places=2)
    
    def test_generate_insert_statement(self):
        """Test INSERT statement generation"""
        user = self.generator.generate_user()
        stmt = self.generator.generate_insert_statement("users", user)
        
        self.assertIsInstance(stmt, str)
        self.assertTrue(stmt.startswith("INSERT INTO users"))
        self.assertIn("VALUES", stmt)
        self.assertTrue(stmt.endswith(";"))
    
    def test_generate_update_statement(self):
        """Test UPDATE statement generation"""
        user = self.generator.generate_user()
        stmt = self.generator.generate_update_statement("users", user)
        
        self.assertIsInstance(stmt, str)
        self.assertTrue(stmt.startswith("UPDATE users"))
        self.assertIn("SET", stmt)
        self.assertIn("WHERE", stmt)
        self.assertTrue(stmt.endswith(";"))
    
    def test_generate_delete_statement(self):
        """Test DELETE statement generation"""
        user_id = self.generator.generate_uuid()
        stmt = self.generator.generate_delete_statement("users", user_id)
        
        self.assertIsInstance(stmt, str)
        self.assertTrue(stmt.startswith("DELETE FROM users"))
        self.assertIn("WHERE", stmt)
        self.assertTrue(stmt.endswith(";"))
    
    def test_generate_batch(self):
        """Test batch generation"""
        statements = self.generator.generate_batch("user", 10, "insert")
        
        self.assertIsInstance(statements, list)
        self.assertEqual(len(statements), 10)
        
        for stmt in statements:
            self.assertIsInstance(stmt, str)
            self.assertTrue(stmt.startswith("INSERT INTO users"))
    
    def test_generate_batch_operations(self):
        """Test different operation types in batch"""
        for operation in ["insert", "update", "delete"]:
            statements = self.generator.generate_batch("user", 5, operation)
            self.assertEqual(len(statements), 5)


class TestMultiCoreGenerator(unittest.TestCase):
    """Test Multi-Core Generator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = MultiCoreGenerator(num_cores=2)
    
    def test_initialization(self):
        """Test multi-core generator initialization"""
        self.assertIsNotNone(self.generator)
        self.assertGreaterEqual(self.generator.num_cores, 1)
    
    def test_generate_parallel(self):
        """Test parallel generation"""
        result = self.generator.generate_parallel("user", 20, "insert")
        
        self.assertIn("statements", result)
        self.assertIn("count", result)
        self.assertIn("duration", result)
        self.assertIn("cores_used", result)
        
        self.assertEqual(result["count"], 20)
        self.assertGreater(result["duration"], 0)


class TestPerformanceMonitor(unittest.TestCase):
    """Test Performance Monitor"""
    
    def test_get_cpu_usage(self):
        """Test CPU usage monitoring"""
        cpu = PerformanceMonitor.get_cpu_usage()
        self.assertIsInstance(cpu, float)
        self.assertGreaterEqual(cpu, 0.0)
        self.assertLessEqual(cpu, 100.0)
    
    def test_get_memory_usage(self):
        """Test memory usage monitoring"""
        mem = PerformanceMonitor.get_memory_usage()
        
        self.assertIn("total_gb", mem)
        self.assertIn("used_gb", mem)
        self.assertIn("available_gb", mem)
        self.assertIn("percent", mem)
        
        self.assertGreater(mem["total_gb"], 0)
        self.assertGreaterEqual(mem["percent"], 0)
        self.assertLessEqual(mem["percent"], 100)
    
    def test_get_system_info(self):
        """Test system information"""
        info = PerformanceMonitor.get_system_info()
        
        self.assertIn("cpu_count", info)
        self.assertIn("total_memory_gb", info)
        
        self.assertGreater(info["cpu_count"], 0)
        self.assertGreater(info["total_memory_gb"], 0)


class TestValidators(unittest.TestCase):
    """Test Validation Functions"""
    
    def test_validate_connection_valid(self):
        """Test valid connection configuration"""
        config = {
            "database": {
                "host": "localhost",
                "port": 3306,
                "username": "user",
                "password": "pass"
            },
            "ssh": {
                "enabled": False
            }
        }
        
        result = validate_connection(config)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["errors"]), 0)
    
    def test_validate_connection_missing_fields(self):
        """Test connection validation with missing fields"""
        config = {
            "database": {
                "host": "localhost"
            },
            "ssh": {
                "enabled": False
            }
        }
        
        result = validate_connection(config)
        self.assertFalse(result["valid"])
        self.assertGreater(len(result["errors"]), 0)
    
    def test_validate_connection_invalid_port(self):
        """Test connection validation with invalid port"""
        config = {
            "database": {
                "host": "localhost",
                "port": 70000,
                "username": "user",
                "password": "pass"
            },
            "ssh": {
                "enabled": False
            }
        }
        
        result = validate_connection(config)
        self.assertFalse(result["valid"])
    
    def test_validate_connection_ssh_missing(self):
        """Test SSH validation when enabled"""
        config = {
            "database": {
                "host": "localhost",
                "port": 3306,
                "username": "user",
                "password": "pass"
            },
            "ssh": {
                "enabled": True
            }
        }
        
        result = validate_connection(config)
        self.assertFalse(result["valid"])
    
    def test_validate_schema_valid(self):
        """Test valid schema validation"""
        schema = {
            "columns": [
                {"name": "id", "type": "VARCHAR(36)", "primary": True},
                {"name": "name", "type": "VARCHAR(100)"}
            ]
        }
        
        result = validate_schema(schema)
        self.assertTrue(result["valid"])
    
    def test_validate_schema_no_columns(self):
        """Test schema validation with no columns"""
        schema = {"columns": []}
        
        result = validate_schema(schema)
        self.assertFalse(result["valid"])
    
    def test_validate_schema_no_primary_key(self):
        """Test schema validation without primary key"""
        schema = {
            "columns": [
                {"name": "name", "type": "VARCHAR(100)"}
            ]
        }
        
        result = validate_schema(schema)
        self.assertFalse(result["valid"])
    
    def test_validate_schema_duplicate_columns(self):
        """Test schema validation with duplicate column names"""
        schema = {
            "columns": [
                {"name": "id", "type": "VARCHAR(36)", "primary": True},
                {"name": "id", "type": "INT"}
            ]
        }
        
        result = validate_schema(schema)
        self.assertFalse(result["valid"])
    
    def test_format_error(self):
        """Test error formatting"""
        error = Exception("Access denied for user")
        formatted = format_error(error)
        
        self.assertIsInstance(formatted, str)
        self.assertIn("❌", formatted)
    
    def test_get_table_icon(self):
        """Test table icon retrieval"""
        self.assertEqual(get_table_icon("users"), "👤")
        self.assertEqual(get_table_icon("products"), "📦")
        self.assertEqual(get_table_icon("orders"), "🛒")
        self.assertEqual(get_table_icon("unknown"), "📄")


class TestDatabaseManagers(unittest.TestCase):
    """Test Database Manager Classes"""
    
    def test_mysql_manager_initialization(self):
        """Test MySQL manager initialization"""
        from core.database import MySQLManager
        
        config = {
            "db_type": "mysql",
            "database": {
                "host": "localhost",
                "port": 3306,
                "username": "user",
                "password": "pass",
                "database": "testdb"
            },
            "ssh": {"enabled": False}
        }
        
        manager = MySQLManager(config)
        self.assertEqual(manager.db_type, "mysql")
        self.assertIsNone(manager.connection)
    
    def test_postgresql_manager_initialization(self):
        """Test PostgreSQL manager initialization"""
        from core.database import PostgreSQLManager
        
        config = {
            "db_type": "postgresql",
            "database": {
                "host": "localhost",
                "port": 5432,
                "username": "user",
                "password": "pass",
                "database": "testdb"
            },
            "ssh": {"enabled": False}
        }
        
        manager = PostgreSQLManager(config)
        self.assertEqual(manager.db_type, "postgresql")
    
    def test_mongodb_manager_initialization(self):
        """Test MongoDB manager initialization"""
        from core.database import MongoDBManager
        
        config = {
            "db_type": "mongodb",
            "database": {
                "host": "localhost",
                "port": 27017,
                "username": "user",
                "password": "pass",
                "database": "testdb"
            },
            "ssh": {"enabled": False}
        }
        
        manager = MongoDBManager(config)
        self.assertEqual(manager.db_type, "mongodb")


def run_tests():
    """Run all tests and generate report"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestSQLDataGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestMultiCoreGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceMonitor))
    suite.addTests(loader.loadTestsFromTestCase(TestValidators))
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseManagers))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("="*70)
    
    return result


if __name__ == "__main__":
    run_tests()
