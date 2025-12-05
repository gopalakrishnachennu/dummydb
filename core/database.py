"""
Database Connection Management
Corporate-level database managers with proper error handling and connection pooling
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import time
from sshtunnel import SSHTunnelForwarder


class DatabaseManager(ABC):
    """Abstract base class for database managers"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize database manager
        
        Args:
            config: Database configuration dictionary
        """
        self.config = config
        self.connection = None
        self.tunnel = None
        self.db_type = config.get('db_type')
        
    @abstractmethod
    def connect(self) -> bool:
        """Establish database connection"""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Close database connection"""
        pass
    
    @abstractmethod
    def test_connection(self) -> Dict[str, Any]:
        """Test database connection"""
        pass
    
    @abstractmethod
    def execute_query(self, query: str, params: Optional[tuple] = None) -> Dict[str, Any]:
        """Execute a database query"""
        pass
    
    @abstractmethod
    def create_database(self, db_name: str) -> Dict[str, Any]:
        """Create a database"""
        pass
    
    @abstractmethod
    def create_table(self, table_name: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Create a table"""
        pass
    
    @abstractmethod
    def get_tables(self) -> List[str]:
        """Get list of tables in database"""
        pass
    
    def is_connected(self) -> bool:
        """Check if database connection is alive"""
        if not self.connection:
            return False
        try:
            result = self.test_connection()
            return result.get('success', False)
        except:
            return False
    
    def ensure_connection(self) -> None:
        """Ensure connection is alive, reconnect if needed"""
        if not self.is_connected():
            try:
                self.disconnect()
                self.connect()
            except Exception as e:
                raise Exception(f"Failed to reconnect: {str(e)}")


class MySQLManager(DatabaseManager):
    """MySQL database manager"""
    
    def connect(self) -> bool:
        """Establish MySQL connection with optional SSH tunnel"""
        try:
            import pymysql
            
            ssh_config = self.config.get('ssh', {})
            db_config = self.config.get('database', {})
            
            # Setup SSH tunnel if enabled
            if ssh_config.get('enabled'):
                self.tunnel = SSHTunnelForwarder(
                    (ssh_config['host'], 22),
                    ssh_username=ssh_config['username'],
                    ssh_pkey=ssh_config.get('key_file'),
                    remote_bind_address=(db_config['host'], db_config['port'])
                )
                self.tunnel.start()
                
                # Connect through tunnel
                self.connection = pymysql.connect(
                    host='127.0.0.1',
                    port=self.tunnel.local_bind_port,
                    user=db_config['username'],
                    password=db_config['password'],
                    database=db_config.get('database'),
                    connect_timeout=10
                )
            else:
                # Direct connection
                self.connection = pymysql.connect(
                    host=db_config['host'],
                    port=db_config['port'],
                    user=db_config['username'],
                    password=db_config['password'],
                    database=db_config.get('database'),
                    connect_timeout=10
                )
            
            return True
            
        except Exception as e:
            self.disconnect()
            raise Exception(f"MySQL connection failed: {str(e)}")
    
    def disconnect(self) -> None:
        """Close MySQL connection and SSH tunnel"""
        if self.connection:
            try:
                self.connection.close()
            except:
                pass
            self.connection = None
        
        if self.tunnel:
            try:
                self.tunnel.stop()
            except:
                pass
            self.tunnel = None
    
    def test_connection(self) -> Dict[str, Any]:
        """Test MySQL connection"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return {'success': True, 'message': 'Connection successful'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> Dict[str, Any]:
        """Execute MySQL query"""
        start_time = time.time()
        
        try:
            self.ensure_connection()
            cursor = self.connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            self.connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            
            duration = time.time() - start_time
            
            return {
                'success': True,
                'affected_rows': affected_rows,
                'duration': duration,
                'error': None
            }
        except Exception as e:
            duration = time.time() - start_time
            try:
                if self.connection:
                    self.connection.rollback()
            except:
                pass
            
            return {
                'success': False,
                'affected_rows': 0,
                'duration': duration,
                'error': str(e)
            }
    
    def create_database(self, db_name: str) -> Dict[str, Any]:
        """Create MySQL database"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
            cursor.execute(f"USE `{db_name}`")
            self.connection.commit()
            cursor.close()
            return {'success': True, 'message': f'Database {db_name} created'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_table(self, table_name: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Create MySQL table"""
        try:
            columns = schema.get('columns', [])
            column_defs = []
            primary_keys = []
            
            for col in columns:
                col_def = f"`{col['name']}` {col['type']}"
                if col.get('primary'):
                    primary_keys.append(col['name'])
                column_defs.append(col_def)
            
            if primary_keys:
                column_defs.append(f"PRIMARY KEY ({', '.join([f'`{k}`' for k in primary_keys])})")
            
            query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({', '.join(column_defs)})"
            
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            cursor.close()
            
            return {'success': True, 'message': f'Table {table_name} created', 'query': query}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_tables(self) -> List[str]:
        """Get list of MySQL tables"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return tables
        except:
            return []


class PostgreSQLManager(DatabaseManager):
    """PostgreSQL database manager"""
    
    def connect(self) -> bool:
        """Establish PostgreSQL connection with optional SSH tunnel"""
        try:
            import psycopg2
            
            ssh_config = self.config.get('ssh', {})
            db_config = self.config.get('database', {})
            
            # Setup SSH tunnel if enabled
            if ssh_config.get('enabled'):
                self.tunnel = SSHTunnelForwarder(
                    (ssh_config['host'], 22),
                    ssh_username=ssh_config['username'],
                    ssh_pkey=ssh_config.get('key_file'),
                    remote_bind_address=(db_config['host'], db_config['port'])
                )
                self.tunnel.start()
                
                # Connect through tunnel
                self.connection = psycopg2.connect(
                    host='127.0.0.1',
                    port=self.tunnel.local_bind_port,
                    user=db_config['username'],
                    password=db_config['password'],
                    database=db_config.get('database'),
                    connect_timeout=10
                )
            else:
                # Direct connection
                self.connection = psycopg2.connect(
                    host=db_config['host'],
                    port=db_config['port'],
                    user=db_config['username'],
                    password=db_config['password'],
                    database=db_config.get('database'),
                    connect_timeout=10
                )
            
            return True
            
        except Exception as e:
            self.disconnect()
            raise Exception(f"PostgreSQL connection failed: {str(e)}")
    
    def disconnect(self) -> None:
        """Close PostgreSQL connection and SSH tunnel"""
        if self.connection:
            try:
                self.connection.close()
            except:
                pass
            self.connection = None
        
        if self.tunnel:
            try:
                self.tunnel.stop()
            except:
                pass
            self.tunnel = None
    
    def test_connection(self) -> Dict[str, Any]:
        """Test PostgreSQL connection"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return {'success': True, 'message': 'Connection successful'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> Dict[str, Any]:
        """Execute PostgreSQL query"""
        start_time = time.time()
        
        try:
            self.ensure_connection()
            cursor = self.connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            self.connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            
            duration = time.time() - start_time
            
            return {
                'success': True,
                'affected_rows': affected_rows,
                'duration': duration,
                'error': None
            }
        except Exception as e:
            duration = time.time() - start_time
            try:
                if self.connection:
                    self.connection.rollback()
            except:
                pass
            
            return {
                'success': False,
                'affected_rows': 0,
                'duration': duration,
                'error': str(e)
            }
    
    def create_database(self, db_name: str) -> Dict[str, Any]:
        """Create PostgreSQL database"""
        try:
            # PostgreSQL requires autocommit for CREATE DATABASE
            self.connection.autocommit = True
            cursor = self.connection.cursor()
            cursor.execute(f"CREATE DATABASE {db_name}")
            cursor.close()
            self.connection.autocommit = False
            return {'success': True, 'message': f'Database {db_name} created'}
        except Exception as e:
            self.connection.autocommit = False
            return {'success': False, 'error': str(e)}
    
    def create_table(self, table_name: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Create PostgreSQL table"""
        try:
            columns = schema.get('columns', [])
            column_defs = []
            primary_keys = []
            
            for col in columns:
                # Convert MySQL types to PostgreSQL
                pg_type = col['type'].replace('DATETIME', 'TIMESTAMP').replace('BOOLEAN', 'BOOL')
                col_def = f'"{col["name"]}" {pg_type}'
                if col.get('primary'):
                    primary_keys.append(col['name'])
                column_defs.append(col_def)
            
            if primary_keys:
                pk_columns = ', '.join([f'"{k}"' for k in primary_keys])
                column_defs.append(f'PRIMARY KEY ({pk_columns})')
            
            query = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({", ".join(column_defs)})'
            
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            cursor.close()
            
            return {'success': True, 'message': f'Table {table_name} created', 'query': query}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_tables(self) -> List[str]:
        """Get list of PostgreSQL tables"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname='public'")
            tables = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return tables
        except:
            return []


class MongoDBManager(DatabaseManager):
    """MongoDB database manager"""
    
    def connect(self) -> bool:
        """Establish MongoDB connection with optional SSH tunnel"""
        try:
            from pymongo import MongoClient
            
            ssh_config = self.config.get('ssh', {})
            db_config = self.config.get('database', {})
            
            # Setup SSH tunnel if enabled
            if ssh_config.get('enabled'):
                self.tunnel = SSHTunnelForwarder(
                    (ssh_config['host'], 22),
                    ssh_username=ssh_config['username'],
                    ssh_pkey=ssh_config.get('key_file'),
                    remote_bind_address=(db_config['host'], db_config['port'])
                )
                self.tunnel.start()
                
                # Connect through tunnel
                connection_string = f"mongodb://{db_config['username']}:{db_config['password']}@127.0.0.1:{self.tunnel.local_bind_port}/{db_config.get('database', 'admin')}"
                self.connection = MongoClient(connection_string, serverSelectionTimeoutMS=10000)
            else:
                # Direct connection
                connection_string = f"mongodb://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config.get('database', 'admin')}"
                self.connection = MongoClient(connection_string, serverSelectionTimeoutMS=10000)
            
            # Test connection
            self.connection.admin.command('ping')
            return True
            
        except Exception as e:
            self.disconnect()
            raise Exception(f"MongoDB connection failed: {str(e)}")
    
    def disconnect(self) -> None:
        """Close MongoDB connection and SSH tunnel"""
        if self.connection:
            try:
                self.connection.close()
            except:
                pass
            self.connection = None
        
        if self.tunnel:
            try:
                self.tunnel.stop()
            except:
                pass
            self.tunnel = None
    
    def test_connection(self) -> Dict[str, Any]:
        """Test MongoDB connection"""
        try:
            self.connection.admin.command('ping')
            return {'success': True, 'message': 'Connection successful'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> Dict[str, Any]:
        """Execute MongoDB operation (not applicable for MongoDB)"""
        return {'success': False, 'error': 'Use MongoDB-specific methods'}
    
    def create_database(self, db_name: str) -> Dict[str, Any]:
        """Create MongoDB database (implicit in MongoDB)"""
        try:
            # MongoDB creates database implicitly when you insert data
            db = self.connection[db_name]
            # Create a dummy collection to initialize the database
            db.create_collection('_init')
            db.drop_collection('_init')
            return {'success': True, 'message': f'Database {db_name} ready'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_table(self, table_name: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Create MongoDB collection"""
        try:
            db_name = self.config['database'].get('database', 'testdb')
            db = self.connection[db_name]
            
            # Create collection
            db.create_collection(table_name)
            
            # Create indexes for primary keys
            columns = schema.get('columns', [])
            for col in columns:
                if col.get('primary'):
                    db[table_name].create_index(col['name'], unique=True)
            
            return {'success': True, 'message': f'Collection {table_name} created'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_tables(self) -> List[str]:
        """Get list of MongoDB collections"""
        try:
            db_name = self.config['database'].get('database', 'testdb')
            db = self.connection[db_name]
            return db.list_collection_names()
        except:
            return []
