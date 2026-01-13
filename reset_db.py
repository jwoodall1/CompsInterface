import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('credentials.env')

def reset_db():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get('DB_NAME', 'comps_db'),
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASS', 'comps2026'),
            host=os.environ.get('DB_HOST', 'localhost'),
            port=os.environ.get('DB_PORT', '5432')
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        print("Dropping existing tables...")
        cur.execute("DROP TABLE IF EXISTS responses CASCADE;")
        cur.execute("DROP TABLE IF EXISTS participants CASCADE;")
        
        print("Recreating tables with new schema...")
        # Create participants table
        cur.execute('''
            CREATE TABLE participants (
                participant_id INT PRIMARY KEY,
                name TEXT,
                prompted BOOLEAN,
                consent BOOLEAN,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create responses table
        cur.execute('''
            CREATE TABLE responses (
                participant_id INT PRIMARY KEY REFERENCES participants(participant_id),
                task1_id INT,
                task1_r1 TEXT,
                task1_r2 TEXT,
                task1_r3 TEXT,
                task2_id INT,
                task2_r1 TEXT,
                task2_r2 TEXT,
                task2_r3 TEXT,
                task3_id INT,
                task3_r1 TEXT,
                task3_r2 TEXT,
                task3_r3 TEXT,
                task4_id INT,
                task4_r1 TEXT,
                task4_r2 TEXT,
                task4_r3 TEXT,
                expert_id INT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        print("Database reset successfully!")
        cur.close()
    except Exception as e:
        print(f"Error resetting database: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    confirm = input("This will DELETE ALL DATA in the database. Are you sure? (y/n): ")
    if confirm.lower() == 'y':
        reset_db()
    else:
        print("Reset cancelled.")
