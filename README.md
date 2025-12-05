# ⚡ SQL Data Generator - Corporate Edition

Professional multi-page application for database testing and data generation.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The app will open at `http://localhost:8501`

## ✨ Features

### 🗄️ Multi-Database Support
- **MySQL** - Full support with SSH tunnel
- **PostgreSQL** - Complete PostgreSQL integration
- **MongoDB** - NoSQL database support

### 📄 Multi-Page Architecture
1. **🔌 Database Connection** - Secure connection setup
2. **🛠️ Schema Setup** - Database and table creation
3. **⚡ Data Generation** - Live data generation

### 🔒 Security
- SSH tunnel support for all databases
- File upload for SSH keys (.pem, .key, .ppk)
- Password masking
- Secure connection handling

### ⚡ Live Generation
- Real-time SQL execution
- 1-100 operations per second
- Auto-reconnect on connection loss
- Batch processing with retry logic

## 📋 Requirements

```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
pymysql>=1.1.0
psycopg2-binary>=2.9.9
pymongo>=4.6.0
sshtunnel>=0.4.0
psutil>=5.9.0
paramiko<3.0
faker>=20.0.0
```

## 🛠️ Usage

### Step 1: Database Connection

1. Select database type (MySQL/PostgreSQL/MongoDB)
2. Configure SSH tunnel (optional)
3. Upload SSH key or enter path
4. Enter database credentials
5. Click "Connect to Database"

### Step 2: Schema Setup

1. Create database
2. Select tables to create (users, products, orders)
3. Or create custom tables
4. Click "Create Selected Tables"

### Step 3: Data Generation

1. Select table and operation type
2. Adjust speed (ops/sec)
3. Click "START" to begin generation
4. Monitor metrics and statistics

## 📁 Project Structure

```
data-generator/
├── app.py                          # Main entry point
├── pages/
│   ├── 1_🔌_Database_Connection.py  # Connection page
│   ├── 2_🛠️_Schema_Setup.py         # Schema page
│   └── 3_⚡_Data_Generation.py      # Generation page
├── core/
│   ├── database.py                 # Database managers
│   ├── generator.py                # Data generation
│   └── config.py                   # Configuration
├── utils/
│   ├── validators.py               # Validation functions
│   └── helpers.py                  # Helper utilities
└── requirements.txt                # Dependencies
```

## 🎯 Use Cases

- **Load Testing** - Generate millions of records
- **Development** - Create realistic test data
- **Performance Testing** - Benchmark database performance
- **Schema Validation** - Test table structures

## 🐛 Troubleshooting

### Connection Issues
- Verify database host and port
- Check username and password
- Ensure database is running
- Check firewall/security group rules
- Verify SSH key permissions (chmod 400)

### Schema Issues
- Ensure database exists
- Check user privileges
- Verify table names are unique

### Generation Issues
- Reduce operations per second
- Check database connection stability
- Monitor Recent Statements for errors

## 🌐 Deployment

### Streamlit Cloud
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Deploy from repository
4. Configure secrets

### Local
```bash
streamlit run app.py --server.port 8501
```

## 📖 Documentation

### Database Types

**MySQL:**
- Default port: 3306
- Connection string format
- SSH tunnel support

**PostgreSQL:**
- Default port: 5432
- Type conversion handling
- Advanced features

**MongoDB:**
- Default port: 27017
- Collection-based storage
- Document operations

### Table Schemas

**Users Table:**
- id, username, email
- first_name, last_name
- phone, city, state, country
- is_active, created_at, updated_at

**Products Table:**
- id, sku, name, category
- price, stock_quantity
- is_available, timestamps

**Orders Table:**
- id, order_number
- user_id, product_id
- quantity, pricing fields
- payment_method, status

## 🔧 Configuration

Edit `core/config.py` to customize:
- Database types
- Table schemas
- Operation types
- Performance settings
- UI settings

## 📝 License

Free to use for any purpose.

---

**Built with Streamlit | Corporate-Grade Quality | Production-Ready**
