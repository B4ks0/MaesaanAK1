# MySQL Configuration Guide

## Current Settings (Development)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ak1_db',
        'USER': 'root',
        'PASSWORD': '',  # Empty password (development only)
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
        'CONN_MAX_AGE': 600,
    }
}
```

## Production Configuration (Recommended)
Update `ak1/settings.py` to use environment variables:

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Database - MySQL Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'ak1_db'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
        'CONN_MAX_AGE': 600,
    }
}
```

## Environment Variables (.env file)
Create `.env` file in project root:
```
DB_NAME=ak1_db
DB_USER=ak1_user
DB_PASSWORD=your_secure_password_here
DB_HOST=localhost
DB_PORT=3306
```

## MySQL User Setup (Linux/Windows Server)
```sql
-- Create new user for AK1 application
CREATE USER 'ak1_user'@'localhost' IDENTIFIED BY 'your_secure_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON ak1_db.* TO 'ak1_user'@'localhost';
FLUSH PRIVILEGES;

-- Verify
SELECT User, Host FROM mysql.user WHERE User='ak1_user';
```

## Character Set Considerations
- **utf8mb4**: Full Unicode support (recommended)
- **utf8**: Limited Unicode support (legacy)
- Current setting: `utf8mb4` - supports emojis and all Unicode characters

## Connection Pool Settings
- **CONN_MAX_AGE**: 600 seconds (10 minutes)
  - Keeps database connections alive for performance
  - Adjust based on server requirements
  - Set to 0 to disable pooling

## Troubleshooting

### Connection Issues
```bash
# Test MySQL connection
mysql -u root -h localhost -p

# Check if ak1_db exists
SHOW DATABASES;
USE ak1_db;
SHOW TABLES;
```

### Django Errors
```bash
# Clear old migrations cache
python manage.py migrate --fake-initial

# Check database configuration
python manage.py dbshell

# Verify connection
python manage.py check
```

### Performance Tuning
- Add `'init_command': "SET SESSION sql_mode='STRICT_TRANS_TABLES'"` for strictness
- Use `'charset': 'utf8mb4'` for full Unicode
- Monitor connection pool size based on traffic

## Installation Verification
```bash
# Verify mysqlclient is installed
python -c "import MySQLdb; print(MySQLdb.__version__)"

# Verify MySQL is running
mysql -u root -e "SELECT VERSION();"

# Test Django connection
python manage.py migrate --plan
```

## Backup & Recovery

### MySQL Backup
```bash
# Full backup
mysqldump -u root ak1_db > ak1_backup.sql

# With password
mysqldump -u ak1_user -p ak1_db > ak1_backup.sql

# Backup all databases
mysqldump -u root --all-databases > all_backup.sql
```

### Restore from Backup
```bash
# Restore database
mysql -u root ak1_db < ak1_backup.sql

# Restore with password
mysql -u ak1_user -p ak1_db < ak1_backup.sql
```

## Django-MySQL Specific Features
The application uses these MySQL-specific optimizations:
- UTF8MB4 character encoding
- InnoDB storage engine (default)
- Connection pooling via CONN_MAX_AGE
- Strict SQL mode for data integrity
