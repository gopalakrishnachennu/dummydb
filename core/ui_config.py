"""
UI Configuration - All Text, Labels, and Branding
Centralized configuration for easy customization
"""

class UIConfig:
    """UI Text and Branding Configuration"""
    
    # Application Info
    APP_NAME = "Dummy DB"
    APP_VERSION = "1.0"
    APP_TAGLINE = "Enterprise Database Testing & Synthetic Data Generation"
    APP_DESCRIPTION = "Professional multi-database platform for generating realistic test data at scale"
    
    # Founder Information
    FOUNDER = {
        "name": "Gopala Krishna Chennu",
        "github": "https://github.com/gopalakrishnachennu",
        "linkedin": "https://www.linkedin.com/in/gchennu/",
        "title": "Creator & Lead Developer"
    }
    
    # Page Titles
    PAGE_TITLES = {
        "home": f"Welcome to {APP_NAME}",
        "connection": "Database Connection",
        "schema": "Schema Management",
        "generation": "Data Generation Engine"
    }
    
    # Icons (Professional Font Awesome & Custom SVG)
    # Using Font Awesome 6 Free icons
    ICONS = {
        "app": '<i class="fas fa-fire" style="color: #ff6b6b;"></i>',
        "database": '<i class="fas fa-database" style="color: #4facfe;"></i>',
        "connection": '<i class="fas fa-plug" style="color: #00f2fe;"></i>',
        "schema": '<i class="fas fa-sitemap" style="color: #667eea;"></i>',
        "generation": '<i class="fas fa-cogs" style="color: #764ba2;"></i>',
        "success": '<i class="fas fa-check-circle" style="color: #10b981;"></i>',
        "warning": '<i class="fas fa-exclamation-triangle" style="color: #fbbf24;"></i>',
        "error": '<i class="fas fa-times-circle" style="color: #ef4444;"></i>',
        "info": '<i class="fas fa-info-circle" style="color: #3b82f6;"></i>',
        "mysql": '<i class="fas fa-database" style="color: #00758F;"></i>',
        "postgresql": '<i class="fas fa-database" style="color: #336791;"></i>',
        "mongodb": '<i class="fas fa-leaf" style="color: #47A248;"></i>',
        "user": '<i class="fas fa-user" style="color: #667eea;"></i>',
        "product": '<i class="fas fa-box" style="color: #f093fb;"></i>',
        "order": '<i class="fas fa-shopping-cart" style="color: #4facfe;"></i>',
        "settings": '<i class="fas fa-cog" style="color: #764ba2;"></i>',
        "performance": '<i class="fas fa-chart-line" style="color: #10b981;"></i>',
        "security": '<i class="fas fa-shield-alt" style="color: #ef4444;"></i>',
        "speed": '<i class="fas fa-bolt" style="color: #fbbf24;"></i>',
        "cloud": '<i class="fas fa-cloud" style="color: #4facfe;"></i>',
        "rocket": '<i class="fas fa-rocket" style="color: #f093fb;"></i>',
        "star": '<i class="fas fa-star" style="color: #fbbf24;"></i>',
        "check": '<i class="fas fa-check" style="color: #10b981;"></i>',
        "cross": '<i class="fas fa-times" style="color: #ef4444;"></i>',
        "clock": '<i class="fas fa-clock" style="color: #667eea;"></i>',
        "chart": '<i class="fas fa-chart-bar" style="color: #764ba2;"></i>',
        "folder": '<i class="fas fa-folder" style="color: #4facfe;"></i>',
        "link": '<i class="fas fa-link" style="color: #667eea;"></i>',
        "github": '<i class="fab fa-github" style="color: #333;"></i>',
        "linkedin": '<i class="fab fa-linkedin" style="color: #0077b5;"></i>'
    }
    
    # Icon sizes for different contexts
    ICON_SIZES = {
        "small": "16px",
        "medium": "24px",
        "large": "32px",
        "xlarge": "48px"
    }
    
    # Database Types (for compatibility with pages)
    DATABASES = {
        "mysql": {
            "name": "MySQL",
            "icon": "🐬",
            "default_port": 3306
        },
        "postgresql": {
            "name": "PostgreSQL",
            "icon": "🐘",
            "default_port": 5432
        },
        "mongodb": {
            "name": "MongoDB",
            "icon": "🍃",
            "default_port": 27017
        }
    }
    
    # Operation Types (for compatibility with pages)
    OPERATIONS = {
        "insert": "INSERT Only",
        "update": "UPDATE Only",
        "delete": "DELETE Only",
        "random": "Random Mix",
        "lock": "Lock Test",
        "deadlock": "Deadlock Test"
    }
    
    # Navigation Steps
    STEPS = [
        {
            "number": "1",
            "icon": "🔌",
            "title": "Database Connection",
            "description": "Connect securely to MySQL, PostgreSQL, or MongoDB"
        },
        {
            "number": "2",
            "icon": "🗂️",
            "title": "Schema Management",
            "description": "Design and deploy database schemas effortlessly"
        },
        {
            "number": "3",
            "icon": "⚙️",
            "title": "Data Generation",
            "description": "Generate millions of realistic records instantly"
        }
    ]
    
    # Features
    FEATURES = {
        "left": [
            {
                "icon": "💾",
                "title": "Multi-Database Support",
                "description": "MySQL, PostgreSQL, MongoDB"
            },
            {
                "icon": "🔒",
                "title": "Secure SSH Tunneling",
                "description": "Enterprise-grade security"
            },
            {
                "icon": "⚡",
                "title": "Real-Time Generation",
                "description": "Live SQL execution engine"
            }
        ],
        "right": [
            {
                "icon": "🗂️",
                "title": "Schema Designer",
                "description": "Visual database modeling"
            },
            {
                "icon": "📊",
                "title": "Performance Analytics",
                "description": "Real-time metrics dashboard"
            },
            {
                "icon": "🚀",
                "title": "Production Ready",
                "description": "Enterprise-grade reliability"
            }
        ]
    }
    
    # Status Messages
    STATUS = {
        "connected": {
            "icon": "✅",
            "title": "Database Connected",
            "color": "success"
        },
        "not_connected": {
            "icon": "⏳",
            "title": "Not Connected",
            "description": "Configure database connection",
            "color": "warning"
        },
        "schema_created": {
            "icon": "✅",
            "title": "Schema Deployed",
            "color": "success"
        },
        "schema_pending": {
            "icon": "⏳",
            "title": "Schema Pending",
            "description": "Complete connection first",
            "color": "warning"
        },
        "ready": {
            "icon": "🚀",
            "title": "Ready for Generation",
            "description": "All systems operational",
            "color": "success"
        },
        "setup_required": {
            "icon": "ℹ️",
            "title": "Setup Required",
            "description": "Follow setup steps",
            "color": "info"
        }
    }
    
    
    # Table Types
    TABLES = {
        "users": {
            "icon": "👤",
            "title": "Users",
            "description": "User profiles and authentication"
        },
        "products": {
            "icon": "📦",
            "title": "Products",
            "description": "Product catalog and inventory"
        },
        "orders": {
            "icon": "🛒",
            "title": "Orders",
            "description": "Transaction and order history"
        }
    }
    
    # Button Labels
    BUTTONS = {
        "connect": "Connect to Database",
        "disconnect": "Disconnect",
        "test": "Test Connection",
        "create_db": "Create Database",
        "create_tables": "Deploy Schema",
        "start": "Start Generation",
        "stop": "Stop",
        "reset": "Reset Counters",
        "refresh": "Refresh Metrics"
    }
    
    # Help Text
    HELP = {
        "ssh_key": "Upload your SSH private key (.pem, .key, .ppk)",
        "connection": "Enter your database connection details",
        "schema": "Select tables to create or design custom schema",
        "generation": "Configure data generation parameters"
    }
    
    # Footer
    FOOTER = {
        "copyright": f"© 2024 {APP_NAME}",
        "tagline": "Enterprise Edition | Multi-Database Support",
        "features": "🎨 Modern Design | ⚡ High Performance | 🔒 Secure"
    }
    
    @staticmethod
    def get_icon(key: str) -> str:
        """Get icon by key"""
        return UIConfig.ICONS.get(key, "•")
    
    @staticmethod
    def get_database_info(db_type: str) -> dict:
        """Get database information"""
        return UIConfig.DATABASES.get(db_type, {})
    
    @staticmethod
    def get_status_info(status_key: str) -> dict:
        """Get status information"""
        return UIConfig.STATUS.get(status_key, {})
