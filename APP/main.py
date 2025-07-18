import pymysql
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class UserDatabase:
    def __init__(self):
        self.connection = None
        self.connect()
        self.create_table()
    
    def connect(self):
        """Connect to MySQL database"""
        try:
            # Database configuration - you can modify these values
            host = os.getenv('DB_HOST', 'localhost')
            user = os.getenv('DB_USER', 'root')
            password = os.getenv('DB_PASSWORD', 'password')
            database = os.getenv('DB_NAME', 'user_db')
            port = int(os.getenv('DB_PORT', 3306))
            
            self.connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("✅ Successfully connected to MySQL database!")
            
        except pymysql.Error as e:
            print(f"❌ Error connecting to MySQL: {e}")
            print("\nPlease make sure:")
            print("1. MySQL server is running")
            print("2. Database 'user_db' exists")
            print("3. User credentials are correct")
            print("4. Create a .env file with your database configuration")
            exit(1)
    
    def create_table(self):
        """Create users table if it doesn't exist"""
        try:
            with self.connection.cursor() as cursor:
                sql = """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
                cursor.execute(sql)
                self.connection.commit()
                print("✅ Users table ready!")
                
        except pymysql.Error as e:
            print(f"❌ Error creating table: {e}")
    
    def add_user(self, name):
        """Add a new user to the database"""
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO users (name) VALUES (%s)"
                cursor.execute(sql, (name,))
                self.connection.commit()
                print(f"✅ User '{name}' added successfully!")
                return True
                
        except pymysql.IntegrityError:
            print(f"❌ User '{name}' already exists!")
            return False
        except pymysql.Error as e:
            print(f"❌ Error adding user: {e}")
            return False
    
    def get_all_users(self):
        """Get all users from the database"""
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM users ORDER BY created_at DESC"
                cursor.execute(sql)
                return cursor.fetchall()
                
        except pymysql.Error as e:
            print(f"❌ Error fetching users: {e}")
            return []
    
    def delete_user(self, user_id):
        """Delete a user by ID"""
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM users WHERE id = %s"
                cursor.execute(sql, (user_id,))
                self.connection.commit()
                if cursor.rowcount > 0:
                    print(f"✅ User with ID {user_id} deleted successfully!")
                    return True
                else:
                    print(f"❌ User with ID {user_id} not found!")
                    return False
                    
        except pymysql.Error as e:
            print(f"❌ Error deleting user: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("🔌 Database connection closed.")

def display_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("           USER MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Add new user")
    print("2. View all users")
    print("3. Delete user")
    print("4. Exit")
    print("="*50)

def add_user_interface(db):
    """Handle adding a new user"""
    print("\n--- ADD NEW USER ---")
    name = input("Enter user name: ").strip()
    
    if not name:
        print("❌ Name cannot be empty!")
        return
    
    if len(name) > 100:
        print("❌ Name is too long! Maximum 100 characters.")
        return
    
    db.add_user(name)

def view_users_interface(db):
    """Handle viewing all users"""
    print("\n--- ALL USERS ---")
    users = db.get_all_users()
    
    if not users:
        print("No users found in the database.")
        return
    
    print(f"{'ID':<5} {'Name':<20} {'Created At':<20}")
    print("-" * 50)
    for user in users:
        created_at = user['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        print(f"{user['id']:<5} {user['name']:<20} {created_at:<20}")

def delete_user_interface(db):
    """Handle deleting a user"""
    print("\n--- DELETE USER ---")
    
    # First show all users
    users = db.get_all_users()
    if not users:
        print("No users found in the database.")
        return
    
    print("Available users:")
    print(f"{'ID':<5} {'Name':<20}")
    print("-" * 25)
    for user in users:
        print(f"{user['id']:<5} {user['name']:<20}")
    
    try:
        user_id = int(input("\nEnter user ID to delete: "))
        db.delete_user(user_id)
    except ValueError:
        print("❌ Please enter a valid number!")

def main():
    """Main application function"""
    print("🚀 Starting User Management System...")
    
    # Initialize database
    db = UserDatabase()
    
    while True:
        display_menu()
        
        try:
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == '1':
                add_user_interface(db)
            elif choice == '2':
                view_users_interface(db)
            elif choice == '3':
                delete_user_interface(db)
            elif choice == '4':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice! Please enter 1-4.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
    
    # Close database connection
    db.close()

if __name__ == "__main__":
    main()
