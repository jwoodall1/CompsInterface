import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('credentials.env')

def verify_data():
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get('DB_NAME', 'comps_db'),
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASS', 'comps2026'),
            host=os.environ.get('DB_HOST', 'localhost'),
            port=os.environ.get('DB_PORT', '5432')
        )
        cur = conn.cursor()

        print("--- Participants ---")
        cur.execute("SELECT * FROM participants ORDER BY timestamp DESC LIMIT 5;")
        participants = cur.fetchall()
        for p in participants:
            print(p)

        print("\n--- Responses (Latest Row) ---")
        cur.execute("SELECT * FROM responses ORDER BY timestamp DESC LIMIT 1;")
        response_row = cur.fetchone()
        if response_row:
            print(f"Participant ID: {response_row[0]}")
            print(f"Task 1 ID: {response_row[1]}, Response: {response_row[2][:30]}...")
            print(f"Task 2 ID: {response_row[5]}, Response: {response_row[6][:30]}...")
        else:
            print("No responses found yet.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    verify_data()
