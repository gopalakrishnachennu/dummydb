"""
Utility functions for validation and helpers
"""

from typing import Dict, Any


def validate_connection(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate connection configuration
    
    Args:
        config: Connection configuration dictionary
        
    Returns:
        Validation result with success status and errors
    """
    errors = []
    
    # Check required fields
    db_config = config.get('database', {})
    required_fields = ['host', 'port', 'username', 'password']
    
    for field in required_fields:
        if not db_config.get(field):
            errors.append(f"Missing required field: {field}")
    
    # Validate port
    port = db_config.get('port')
    if port and (port < 1 or port > 65535):
        errors.append(f"Invalid port number: {port}")
    
    # Validate SSH config if enabled
    ssh_config = config.get('ssh', {})
    if ssh_config.get('enabled'):
        if not ssh_config.get('host'):
            errors.append("SSH host is required when SSH tunnel is enabled")
        if not ssh_config.get('username'):
            errors.append("SSH username is required when SSH tunnel is enabled")
        if not ssh_config.get('key_file'):
            errors.append("SSH key file is required when SSH tunnel is enabled")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }


def validate_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate table schema
    
    Args:
        schema: Table schema dictionary
        
    Returns:
        Validation result
    """
    errors = []
    
    columns = schema.get('columns', [])
    if not columns:
        errors.append("Schema must have at least one column")
    
    # Check for primary key
    has_primary = any(col.get('primary') for col in columns)
    if not has_primary:
        errors.append("Schema must have at least one primary key")
    
    # Validate column names
    column_names = [col.get('name') for col in columns]
    if len(column_names) != len(set(column_names)):
        errors.append("Duplicate column names found")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }


def format_error(error: Exception) -> str:
    """
    Format error message for user display
    
    Args:
        error: Exception object
        
    Returns:
        Formatted error message
    """
    error_str = str(error)
    
    # Common error patterns and user-friendly messages
    error_mappings = {
        'Access denied': '❌ Authentication failed. Check username and password.',
        'Unknown database': '❌ Database does not exist. Create it first.',
        'Can\'t connect': '❌ Cannot connect to database. Check host and port.',
        'Connection refused': '❌ Connection refused. Check if database is running.',
        'Timeout': '❌ Connection timeout. Check network and firewall settings.',
        'SSH': '❌ SSH tunnel error. Check SSH key and host.',
        'Permission denied': '❌ Permission denied. Check user privileges.',
    }
    
    for pattern, message in error_mappings.items():
        if pattern in error_str:
            return message
    
    # Return truncated error if no pattern matches
    return f"❌ Error: {error_str[:150]}"


def get_table_icon(table_name: str) -> str:
    """
    Get icon for table name
    
    Args:
        table_name: Name of the table
        
    Returns:
        Icon emoji
    """
    icons = {
        'users': '👤',
        'products': '📦',
        'orders': '🛒',
        'customers': '👥',
        'transactions': '💳',
        'inventory': '📊',
        'logs': '📝',
        'sessions': '🔐'
    }
    
    return icons.get(table_name.lower(), '📄')
