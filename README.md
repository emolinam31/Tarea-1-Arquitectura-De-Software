# User Management System

A simple command-line application that allows you to add, view, and delete user names stored in a MySQL database.

## Features

- ✅ Add new users with name validation
- ✅ View all users in a formatted table
- ✅ Delete users by ID
- ✅ MySQL database integration
- ✅ Duplicate name prevention
- ✅ Error handling and user feedback

## Prerequisites

1. **MySQL Server** - Make sure MySQL is installed and running
2. **Python 3.6+** - The application requires Python 3.6 or higher
3. **Database** - Create a database named `user_db` (or configure your own)

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database

1. Create a MySQL database:
```sql
CREATE DATABASE user_db;
```

2. Copy the environment configuration:
```bash
cp env_example.txt .env
```

3. Edit the `.env` file with your MySQL credentials:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_actual_password
DB_NAME=user_db
DB_PORT=3306
```

### 3. Run the Application

```bash
cd APP
python main.py
```

## Usage

The application provides a simple menu-driven interface:

```
==================================================
           USER MANAGEMENT SYSTEM
==================================================
1. Add new user
2. View all users
3. Delete user
4. Exit
==================================================
```

### Adding a User
- Select option 1
- Enter the user's name
- The system will validate the input and save to database

### Viewing Users
- Select option 2
- All users will be displayed in a formatted table with ID, name, and creation date

### Deleting a User
- Select option 3
- View the list of available users
- Enter the ID of the user you want to delete

## Database Schema

The application automatically creates a `users` table with the following structure:

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Error Handling

The application includes comprehensive error handling for:
- Database connection issues
- Invalid user input
- Duplicate names
- Database operation failures

## Troubleshooting

### Common Issues

1. **Connection Error**: Make sure MySQL is running and credentials are correct
2. **Database Not Found**: Create the `user_db` database first
3. **Permission Denied**: Ensure your MySQL user has proper permissions

### MySQL Setup Commands

If you need to set up MySQL from scratch:

```sql
-- Create database
CREATE DATABASE user_db;

-- Create user (optional)
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON user_db.* TO 'app_user'@'localhost';
FLUSH PRIVILEGES;
```

## Project Structure

```
Tarea-1-Arquitectura-De-Software/
├── APP/
│   └── main.py              # Main application file
├── requirements.txt         # Python dependencies
├── env_example.txt         # Environment configuration template
└── README.md              # This file
```

## Security Notes

- Never commit your `.env` file with real credentials
- Use strong passwords for your MySQL database
- Consider using environment variables in production 