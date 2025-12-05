"""
Configuration Management
Corporate-level configuration for the SQL Data Generator
"""

from typing import Dict, List, Any


class Config:
    """Central configuration management"""
    
    # Database Types
    DATABASE_TYPES = {
        "MySQL": "mysql",
        "PostgreSQL": "postgresql",
        "MongoDB": "mongodb"
    }
    
    # Default Ports
    DEFAULT_PORTS = {
        "mysql": 3306,
        "postgresql": 5432,
        "mongodb": 27017
    }
    
    # Table Schemas
    TABLE_SCHEMAS = {
        "users": {
            "columns": [
                {"name": "id", "type": "VARCHAR(36)", "primary": True},
                {"name": "username", "type": "VARCHAR(100)"},
                {"name": "email", "type": "VARCHAR(100)"},
                {"name": "first_name", "type": "VARCHAR(50)"},
                {"name": "last_name", "type": "VARCHAR(50)"},
                {"name": "phone", "type": "VARCHAR(20)"},
                {"name": "city", "type": "VARCHAR(50)"},
                {"name": "state", "type": "VARCHAR(2)"},
                {"name": "country", "type": "VARCHAR(50)"},
                {"name": "is_active", "type": "BOOLEAN"},
                {"name": "created_at", "type": "DATETIME"},
                {"name": "updated_at", "type": "DATETIME"}
            ],
            "icon": "👤",
            "description": "User profiles and authentication"
        },
        "products": {
            "columns": [
                {"name": "id", "type": "VARCHAR(36)", "primary": True},
                {"name": "sku", "type": "VARCHAR(20)"},
                {"name": "name", "type": "VARCHAR(100)"},
                {"name": "category", "type": "VARCHAR(50)"},
                {"name": "price", "type": "DECIMAL(10,2)"},
                {"name": "stock_quantity", "type": "INT"},
                {"name": "is_available", "type": "BOOLEAN"},
                {"name": "created_at", "type": "DATETIME"},
                {"name": "updated_at", "type": "DATETIME"}
            ],
            "icon": "📦",
            "description": "Product catalog and inventory"
        },
        "orders": {
            "columns": [
                {"name": "id", "type": "VARCHAR(36)", "primary": True},
                {"name": "order_number", "type": "VARCHAR(20)"},
                {"name": "user_id", "type": "VARCHAR(36)"},
                {"name": "product_id", "type": "VARCHAR(36)"},
                {"name": "quantity", "type": "INT"},
                {"name": "unit_price", "type": "DECIMAL(10,2)"},
                {"name": "subtotal", "type": "DECIMAL(10,2)"},
                {"name": "tax", "type": "DECIMAL(10,2)"},
                {"name": "total", "type": "DECIMAL(10,2)"},
                {"name": "payment_method", "type": "VARCHAR(50)"},
                {"name": "status", "type": "VARCHAR(20)"},
                {"name": "created_at", "type": "DATETIME"},
                {"name": "updated_at", "type": "DATETIME"}
            ],
            "icon": "🛒",
            "description": "Order transactions and history"
        }
    }
    
    # Operation Types
    OPERATION_TYPES = {
        "➕ INSERT Only": "insert",
        "✏️ UPDATE Only": "update",
        "🗑️ DELETE Only": "delete",
        "🎲 Random Mix": "random",
        "🔒 Lock Simulation": "lock",
        "⚠️ Deadlock Simulation": "deadlock"
    }
    
    # Operation Descriptions
    OPERATION_DESCRIPTIONS = {
        "insert": "Insert new records into the database",
        "update": "Update existing records",
        "delete": "Delete records from the database",
        "random": "Random mix of INSERT, UPDATE, and DELETE operations",
        "lock": "Simulate row-level locks with SELECT FOR UPDATE",
        "deadlock": "Simulate deadlock scenarios for testing"
    }
    
    # Performance Settings
    PERFORMANCE = {
        "min_ops_per_sec": 1,
        "max_ops_per_sec": 100,
        "default_ops_per_sec": 10,
        "batch_size": 20,
        "max_retries": 2,
        "retry_delay": 0.1
    }
    
    # UI Settings
    UI = {
        "page_icon": "⚡",
        "page_title": "SQL Data Generator",
        "layout": "wide",
        "sidebar_state": "expanded"
    }
    
    # Validation Rules
    VALIDATION = {
        "min_port": 1,
        "max_port": 65535,
        "required_fields": ["host", "port", "username", "password"],
        "ssh_key_extensions": ["pem", "key", "ppk"]
    }
    
    @staticmethod
    def get_table_schema(table_name: str) -> Dict[str, Any]:
        """Get schema for a specific table"""
        return Config.TABLE_SCHEMAS.get(table_name, {})
    
    @staticmethod
    def get_all_tables() -> List[str]:
        """Get list of all table names"""
        return list(Config.TABLE_SCHEMAS.keys())
    
    @staticmethod
    def get_default_port(db_type: str) -> int:
        """Get default port for database type"""
        return Config.DEFAULT_PORTS.get(db_type, 3306)
    
    @staticmethod
    def validate_port(port: int) -> bool:
        """Validate port number"""
        return Config.VALIDATION["min_port"] <= port <= Config.VALIDATION["max_port"]
