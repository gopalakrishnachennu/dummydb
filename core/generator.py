#!/usr/bin/env python3
"""
Advanced SQL Data Generator with Multi-Processing Support
=========================================================
High-performance fake data generator with SQL statement generation,
multi-core processing, and database operations.
"""

import random
import string
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import multiprocessing as mp
from multiprocessing import Pool, cpu_count
import time
import psutil


class SQLDataGenerator:
    """Advanced SQL data generator with multi-processing support."""
    
    def __init__(self, seed: int = None):
        """Initialize the SQL data generator."""
        if seed is not None:
            random.seed(seed)
        
        # Data pools
        self.first_names = [
            "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
            "William", "Barbara", "David", "Elizabeth", "Richard", "Susan", "Joseph", "Jessica",
            "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
            "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
            "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle"
        ]
        
        self.last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
            "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
            "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker"
        ]
        
        self.cities = [
            "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
            "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville"
        ]
        
        self.states = ["CA", "TX", "FL", "NY", "PA", "IL", "OH", "GA", "NC", "MI"]
        self.countries = ["USA", "Canada", "UK", "Germany", "France", "Spain", "Italy"]
        self.product_categories = ["Electronics", "Clothing", "Books", "Home", "Sports", "Toys"]
        self.payment_methods = ["Credit Card", "Debit Card", "PayPal", "Bank Transfer", "Cash"]
        self.order_statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]
    
    # ==================== Basic Generators ====================
    
    def generate_uuid(self) -> str:
        """Generate a random UUID."""
        return str(uuid.uuid4())
    
    def generate_integer(self, min_val: int = 0, max_val: int = 1000) -> int:
        """Generate a random integer."""
        return random.randint(min_val, max_val)
    
    def generate_float(self, min_val: float = 0.0, max_val: float = 1000.0, decimals: int = 2) -> float:
        """Generate a random float."""
        return round(random.uniform(min_val, max_val), decimals)
    
    def generate_datetime(self, start_date: datetime = None, end_date: datetime = None) -> str:
        """Generate a random datetime."""
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)
        if end_date is None:
            end_date = datetime.now()
        
        time_between = end_date - start_date
        random_seconds = random.randint(0, int(time_between.total_seconds()))
        random_datetime = start_date + timedelta(seconds=random_seconds)
        return random_datetime.strftime("%Y-%m-%d %H:%M:%S")
    
    def generate_email(self, name: str = None) -> str:
        """Generate a random email."""
        if name is None:
            name = f"{random.choice(self.first_names).lower()}.{random.choice(self.last_names).lower()}"
        domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
        return f"{name}@{random.choice(domains)}"
    
    def generate_phone(self) -> str:
        """Generate a random phone number."""
        area = random.randint(200, 999)
        exchange = random.randint(200, 999)
        number = random.randint(1000, 9999)
        return f"({area}) {exchange}-{number}"
    
    # ==================== Complex Object Generators ====================
    
    def generate_user(self) -> Dict[str, Any]:
        """Generate a user record."""
        first_name = random.choice(self.first_names)
        last_name = random.choice(self.last_names)
        username = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 99)}"
        
        return {
            "id": self.generate_uuid(),
            "username": username,
            "email": self.generate_email(f"{first_name}.{last_name}"),
            "first_name": first_name,
            "last_name": last_name,
            "phone": self.generate_phone(),
            "city": random.choice(self.cities),
            "state": random.choice(self.states),
            "country": random.choice(self.countries),
            "is_active": random.choice([True, False]),
            "created_at": self.generate_datetime(),
            "updated_at": self.generate_datetime()
        }
    
    def generate_product(self) -> Dict[str, Any]:
        """Generate a product record."""
        adjectives = ["Premium", "Deluxe", "Pro", "Elite", "Smart", "Classic"]
        nouns = ["Widget", "Gadget", "Device", "Tool", "Kit", "System"]
        
        return {
            "id": self.generate_uuid(),
            "sku": f"{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}-{random.randint(100000, 999999)}",
            "name": f"{random.choice(adjectives)} {random.choice(nouns)}",
            "category": random.choice(self.product_categories),
            "price": self.generate_float(10.0, 1000.0, 2),
            "stock_quantity": self.generate_integer(0, 1000),
            "is_available": random.choice([True, False]),
            "created_at": self.generate_datetime(),
            "updated_at": self.generate_datetime()
        }
    
    def generate_order(self) -> Dict[str, Any]:
        """Generate an order record."""
        quantity = self.generate_integer(1, 10)
        unit_price = self.generate_float(10.0, 500.0, 2)
        subtotal = round(quantity * unit_price, 2)
        tax = round(subtotal * 0.08, 2)
        total = round(subtotal + tax, 2)
        
        return {
            "id": self.generate_uuid(),
            "order_number": f"ORD-{random.randint(100000, 999999)}",
            "user_id": self.generate_uuid(),
            "product_id": self.generate_uuid(),
            "quantity": quantity,
            "unit_price": unit_price,
            "subtotal": subtotal,
            "tax": tax,
            "total": total,
            "payment_method": random.choice(self.payment_methods),
            "status": random.choice(self.order_statuses),
            "created_at": self.generate_datetime(),
            "updated_at": self.generate_datetime()
        }
    
    # ==================== SQL Statement Generators ====================
    
    def generate_insert_statement(self, table_name: str, data: Dict[str, Any]) -> str:
        """Generate SQL INSERT statement."""
        columns = []
        values = []
        
        for key, value in data.items():
            columns.append(key)
            if value is None:
                values.append('NULL')
            elif isinstance(value, bool):
                values.append('TRUE' if value else 'FALSE')
            elif isinstance(value, (int, float)):
                values.append(str(value))
            else:
                escaped_value = str(value).replace("'", "''")
                values.append(f"'{escaped_value}'")
        
        columns_str = ', '.join(columns)
        values_str = ', '.join(values)
        
        return f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});"
    
    def generate_update_statement(self, table_name: str, data: Dict[str, Any], id_column: str = 'id') -> str:
        """Generate SQL UPDATE statement."""
        record_id = data.get(id_column)
        set_clauses = []
        
        for key, value in data.items():
            if key == id_column:
                continue
            
            if value is None:
                set_clauses.append(f"{key} = NULL")
            elif isinstance(value, bool):
                set_clauses.append(f"{key} = {'TRUE' if value else 'FALSE'}")
            elif isinstance(value, (int, float)):
                set_clauses.append(f"{key} = {value}")
            else:
                escaped_value = str(value).replace("'", "''")
                set_clauses.append(f"{key} = '{escaped_value}'")
        
        set_str = ', '.join(set_clauses)
        
        if isinstance(record_id, str):
            where_clause = f"{id_column} = '{record_id}'"
        else:
            where_clause = f"{id_column} = {record_id}"
        
        return f"UPDATE {table_name} SET {set_str} WHERE {where_clause};"
    
    def generate_delete_statement(self, table_name: str, record_id: Any, id_column: str = 'id') -> str:
        """Generate SQL DELETE statement."""
        if isinstance(record_id, str):
            where_clause = f"{id_column} = '{record_id}'"
        else:
            where_clause = f"{id_column} = {record_id}"
        
        return f"DELETE FROM {table_name} WHERE {where_clause};"
    
    # ==================== Batch Generators ====================
    
    def generate_batch(self, data_type: str, count: int, operation: str = 'insert') -> List[str]:
        """Generate a batch of SQL statements."""
        statements = []
        
        # Map data types to generators and table names
        generators = {
            'user': (self.generate_user, 'users'),
            'product': (self.generate_product, 'products'),
            'order': (self.generate_order, 'orders')
        }
        
        if data_type not in generators:
            raise ValueError(f"Unknown data type: {data_type}")
        
        generator_func, table_name = generators[data_type]
        
        for _ in range(count):
            data = generator_func()
            
            # Handle random operation - randomly choose INSERT, UPDATE, or DELETE
            if operation == 'random':
                actual_operation = random.choice(['insert', 'update', 'delete'])
            else:
                actual_operation = operation
            
            if actual_operation == 'insert':
                stmt = self.generate_insert_statement(table_name, data)
            elif actual_operation == 'update':
                stmt = self.generate_update_statement(table_name, data)
            elif actual_operation == 'delete':
                stmt = self.generate_delete_statement(table_name, data['id'])
            else:
                raise ValueError(f"Unknown operation: {actual_operation}")
            
            statements.append(stmt)
        
        return statements


class MultiCoreGenerator:
    """Multi-core data generation manager."""
    
    def __init__(self, num_cores: int = None):
        """Initialize multi-core generator."""
        self.num_cores = num_cores or cpu_count()
        self.generator = SQLDataGenerator()
    
    @staticmethod
    def _generate_chunk(args: Tuple[str, int, str, int]) -> Tuple[List[str], float, int]:
        """Generate a chunk of data (worker function)."""
        data_type, count, operation, seed = args
        
        # Create generator with seed for this worker
        generator = SQLDataGenerator(seed)
        
        start_time = time.time()
        start_cpu = psutil.Process().cpu_percent()
        
        statements = generator.generate_batch(data_type, count, operation)
        
        end_time = time.time()
        duration = end_time - start_time
        
        return statements, duration, len(statements)
    
    def generate_parallel(self, data_type: str, total_count: int, operation: str = 'insert') -> Dict[str, Any]:
        """Generate data using multiple cores."""
        start_time = time.time()
        
        # Calculate chunk size per core
        chunk_size = total_count // self.num_cores
        remainder = total_count % self.num_cores
        
        # Prepare arguments for each worker
        tasks = []
        for i in range(self.num_cores):
            count = chunk_size + (1 if i < remainder else 0)
            if count > 0:
                seed = random.randint(1, 1000000) + i
                tasks.append((data_type, count, operation, seed))
        
        # Execute in parallel
        with Pool(processes=self.num_cores) as pool:
            results = pool.map(self._generate_chunk, tasks)
        
        # Combine results
        all_statements = []
        total_duration = 0
        
        for statements, duration, count in results:
            all_statements.extend(statements)
            total_duration = max(total_duration, duration)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        return {
            'statements': all_statements,
            'count': len(all_statements),
            'duration': total_time,
            'cores_used': self.num_cores,
            'records_per_second': len(all_statements) / total_time if total_time > 0 else 0
        }


class PerformanceMonitor:
    """Monitor system performance during data generation."""
    
    @staticmethod
    def get_cpu_usage() -> float:
        """Get current CPU usage percentage."""
        return psutil.cpu_percent(interval=0.1)
    
    @staticmethod
    def get_cpu_per_core() -> List[float]:
        """Get CPU usage per core."""
        return psutil.cpu_percent(interval=0.1, percpu=True)
    
    @staticmethod
    def get_memory_usage() -> Dict[str, float]:
        """Get memory usage statistics."""
        mem = psutil.virtual_memory()
        return {
            'total_gb': mem.total / (1024**3),
            'used_gb': mem.used / (1024**3),
            'available_gb': mem.available / (1024**3),
            'percent': mem.percent
        }
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Get system information."""
        return {
            'cpu_count': cpu_count(),
            'cpu_freq': psutil.cpu_freq().current if psutil.cpu_freq() else 0,
            'total_memory_gb': psutil.virtual_memory().total / (1024**3)
        }


if __name__ == "__main__":
    # Test the generator
    generator = SQLDataGenerator()
    
    print("Testing SQL Data Generator...")
    print("\n=== INSERT Statement ===")
    user = generator.generate_user()
    print(generator.generate_insert_statement('users', user))
    
    print("\n=== UPDATE Statement ===")
    print(generator.generate_update_statement('users', user))
    
    print("\n=== DELETE Statement ===")
    print(generator.generate_delete_statement('users', user['id']))
    
    print("\n=== Multi-Core Generation ===")
    mc_gen = MultiCoreGenerator(num_cores=4)
    result = mc_gen.generate_parallel('user', 100, 'insert')
    print(f"Generated {result['count']} statements in {result['duration']:.2f}s")
    print(f"Speed: {result['records_per_second']:.2f} records/second")
    print(f"Cores used: {result['cores_used']}")
