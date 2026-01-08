import psycopg2
from psycopg2 import sql
import os

def setup_database():
    db_url = os.environ.get('POSTGRES_SETUP_URL', 'dbname=postgres user=postgres password=comps2026 host=localhost')
    new_db_name = 'comps_db'

    try:
        # Connect to default 'postgres' database
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor()

        # Check if database exists
        cur.execute(sql.SQL("SELECT 1 FROM pg_catalog.pg_database WHERE datname = {}").format(sql.Literal(new_db_name)))
        exists = cur.fetchone()
        
        if not exists:
            print(f"Creating database {new_db_name}...")
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_db_name)))
        else:
            print(f"Database {new_db_name} already exists.")

        cur.close()
        conn.close()

        # Connect to the new database to create tables
        conn = psycopg2.connect(os.environ.get('DATABASE_URL', f'dbname={new_db_name} user=postgres password=comps2026 host=localhost'))
        cur = conn.cursor()

        print("Creating tables...")
        # Create participants table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS participants (
                participant_id TEXT PRIMARY KEY,
                name TEXT,
                prompted BOOLEAN,
                consent BOOLEAN,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create responses table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS responses (
                participant_id TEXT PRIMARY KEY REFERENCES participants(participant_id),
                task1_id TEXT,
                task1_r1 TEXT,
                task1_r2 TEXT,
                task1_r3 TEXT,
                task2_id TEXT,
                task2_r1 TEXT,
                task2_r2 TEXT,
                task2_r3 TEXT,
                task3_id TEXT,
                task3_r1 TEXT,
                task3_r2 TEXT,
                task3_r3 TEXT,
                task4_id TEXT,
                task4_r1 TEXT,
                task4_r2 TEXT,
                task4_r3 TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        cur.close()
        conn.close()
        print("Setup complete!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    setup_database()
