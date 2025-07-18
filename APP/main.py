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
        self.create_database()
        self.create_table()
    
    def connect(self):
        """Connect to MySQL server (without specific database first)"""
        try:
            # Database configuration
            host = os.getenv('DB_HOST', 'localhost')
            user = os.getenv('DB_USER', 'root') 
            password = os.getenv('DB_PASSWORD')  
            port = int(os.getenv('DB_PORT', 3306))
            
            print(f"🔌 Attempting to connect to MySQL server at {host}:{port}")
            print(f"📝 Using user: {user}")
            
            # Verificar que la contraseña esté configurada
            if not password:
                print("❌ DB_PASSWORD not found in .env file!")
                print("Please check your .env file contains: DB_PASSWORD=your_password")
                exit(1)
            
            # First connect without database to create it if needed
            self.connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                port=port,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("✅ Successfully connected to MySQL server!")
            
        except pymysql.Error as e:
            print(f"❌ Error connecting to MySQL: {e}")
            print(f"Error code: {e.args[0]}")
            print("\nPlease check:")
            print("1. MySQL server is running")
            print("2. Host and port are correct")
            print("3. Username and password are correct")
            print("4. .env file exists and has correct values")
            print("\nCurrent configuration:")
            print(f"   Host: {os.getenv('DB_HOST', 'localhost')}")
            print(f"   User: {os.getenv('DB_USER', 'root')}")
            print(f"   Port: {os.getenv('DB_PORT', 3306)}")
            print(f"   Password set: {'Yes' if os.getenv('DB_PASSWORD') else 'No'}")
            exit(1)
    
    def create_database(self):
        """Create database if it doesn't exist"""
        try:
            database = os.getenv('DB_NAME', 'user_db')
            with self.connection.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
                self.connection.commit()
                print(f"✅ Database '{database}' ready!")
                
                # Now connect to the specific database
                cursor.execute(f"USE {database}")
                
        except pymysql.Error as e:
            print(f"❌ Error creating database: {e}")
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
    
    def test_connection(self):
        """Test database connection and show info"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                print(f"📊 MySQL version: {version['VERSION()']}")
                
                cursor.execute("SELECT DATABASE()")
                current_db = cursor.fetchone()
                print(f"🗃️ Current database: {current_db['DATABASE()']}")
                
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                print(f"📋 Tables in database: {len(tables)}")
                
                # Mostrar cuántos usuarios hay
                cursor.execute("SELECT COUNT(*) as count FROM users")
                user_count = cursor.fetchone()
                print(f"👥 Total users in database: {user_count['count']}")
                
        except pymysql.Error as e:
            print(f"❌ Error testing connection: {e}")
    
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
    
    def search_user(self, search_term):
        """Search users by name"""
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE name LIKE %s ORDER BY created_at DESC"
                cursor.execute(sql, (f"%{search_term}%",))
                return cursor.fetchall()
                
        except pymysql.Error as e:
            print(f"❌ Error searching users: {e}")
            return []
    
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
    print("3. Search user")
    print("4. Delete user")
    print("5. Test connection")
    print("6. Exit")
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
    
    print(f"{'ID':<5} {'Name':<30} {'Created At':<20}")
    print("-" * 60)
    for user in users:
        created_at = user['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        print(f"{user['id']:<5} {user['name']:<30} {created_at:<20}")
    
    print(f"\nTotal users: {len(users)}")

def search_user_interface(db):
    """Handle searching users"""
    print("\n--- SEARCH USER ---")
    search_term = input("Enter search term: ").strip()
    
    if not search_term:
        print("❌ Search term cannot be empty!")
        return
    
    users = db.search_user(search_term)
    
    if not users:
        print(f"No users found matching '{search_term}'.")
        return
    
    print(f"\n--- SEARCH RESULTS FOR '{search_term}' ---")
    print(f"{'ID':<5} {'Name':<30} {'Created At':<20}")
    print("-" * 60)
    for user in users:
        created_at = user['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        print(f"{user['id']:<5} {user['name']:<30} {created_at:<20}")
    
    print(f"\nFound {len(users)} user(s)")

def delete_user_interface(db):
    """Handle deleting a user"""
    print("\n--- DELETE USER ---")
    
    # First show all users
    users = db.get_all_users()
    if not users:
        print("No users found in the database.")
        return
    
    print("Available users:")
    print(f"{'ID':<5} {'Name':<30}")
    print("-" * 35)
    for user in users:
        print(f"{user['id']:<5} {user['name']:<30}")
    
    try:
        user_id = int(input("\nEnter user ID to delete: "))
        confirm = input(f"Are you sure you want to delete user with ID {user_id}? (y/N): ").strip().lower()
        
        if confirm == 'y' or confirm == 'yes':
            db.delete_user(user_id)
        else:
            print("❌ Delete operation cancelled.")
            
    except ValueError:
        print("❌ Please enter a valid number!")

def main():
    """Main application function"""
    print("🚀 Starting User Management System...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please create a .env file with your database configuration.")
        print("Example:")
        print("DB_HOST=127.0.0.1")
        print("DB_USER=root")
        print("DB_PASSWORD=your_password")
        print("DB_NAME=user_db")
        print("DB_PORT=3306")
        exit(1)
    
    # Initialize database
    try:
        db = UserDatabase()
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        exit(1)
    
    while True:
        display_menu()
        
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                add_user_interface(db)
            elif choice == '2':
                view_users_interface(db)
            elif choice == '3':
                search_user_interface(db)
            elif choice == '4':
                delete_user_interface(db)
            elif choice == '5':
                db.test_connection()
            elif choice == '6':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice! Please enter 1-6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
    
    # Close database connection
    db.close()

if __name__ == "__main__":
    main()