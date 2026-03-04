import sqlite3
import pandas as pd
import os

DB_PATH = 'db/medicine_info.db'
CSV_PATH = 'dataset/medicine_info_dataset.csv'


def initialize_db():
    """
    Create SQLite database and schema.
    Drops existing table and creates fresh one.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Drop existing table if it exists
    cursor.execute('DROP TABLE IF EXISTS medicines')
    
    # Create medicines table
    cursor.execute('''
        CREATE TABLE medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_name TEXT NOT NULL,
            composition TEXT NOT NULL,
            manufacturer TEXT,
            uses TEXT,
            side_effects TEXT
        )
    ''')
    
    # Drop existing indexes if they exist
    cursor.execute('DROP INDEX IF EXISTS idx_medicine_name')
    cursor.execute('DROP INDEX IF EXISTS idx_composition')
    
    # Create indexes for faster queries
    cursor.execute('CREATE INDEX idx_medicine_name ON medicines(medicine_name)')
    cursor.execute('CREATE INDEX idx_composition ON medicines(composition)')

    conn.commit()
    conn.close()
    print("✓ Database schema created successfully!")


def insert_medicines_from_csv():
    """
    Initialize database schema and read CSV file to insert medicine data into database.
    """
    
    # Initialize database schema first
    initialize_db()
    
    # Check if CSV exists
    if not os.path.exists(CSV_PATH):
        print(f"Error: CSV file not found at {CSV_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Read CSV file
    df = pd.read_csv(CSV_PATH)
    
    skipped_rows = []
    
    # Insert data row by row
    for idx, row in df.iterrows():
        try:
            cursor.execute('''
                INSERT INTO medicines (medicine_name, composition, manufacturer, uses, side_effects)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                row['Medicine Name'],
                row['Composition'],
                row['Manufacturer'],
                row['Uses'],        
                row['Side_effects'] 
            ))
        except Exception as e:
            skipped_rows.append((idx, row['Medicine Name'], str(e)))
    
    conn.commit()
    
    # Verify import
    cursor.execute('SELECT COUNT(*) FROM medicines')
    count = cursor.fetchone()[0]
    
    print(f"✓ Data imported successfully!")
    print(f"✓ Total medicines inserted: {count}")
    
    if skipped_rows:
        print(f"\n⚠️  Skipped {len(skipped_rows)} rows:")
        for idx, medicine, error in skipped_rows:
            print(f"  Row {idx}: {medicine}")
    
    conn.close()


def get_medicine_by_name(medicine_name):
    """
    Query medicine by brand name (case-insensitive partial match).
    Returns up to 5 results for LLM to choose from.
    """
    if not medicine_name or not isinstance(medicine_name, str):
        return None
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT medicine_name, composition, manufacturer, uses, side_effects
            FROM medicines 
            WHERE LOWER(medicine_name) LIKE LOWER(?)
            LIMIT 5
        ''', (f'%{medicine_name}%',))
        
        results = cursor.fetchall()
        conn.close()
        
        if results:
            # Return list of results (max 5)
            return [
                {
                    "medicine_name": result[0],
                    "composition": result[1],
                    "manufacturer": result[2],
                    "uses": result[3],
                    "side_effects": result[4]
                } for result in results
            ]
        
        return None
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    
def get_medicine_by_composition(composition):
    """
    Query medicine by generic name/composition (case-insensitive partial match).
    Returns up to 5 results for LLM to choose from.
    """
    if not composition or not isinstance(composition, str):
        return None
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT medicine_name, composition, manufacturer, uses, side_effects
            FROM medicines 
            WHERE LOWER(composition) LIKE LOWER(?)
            LIMIT 5
        ''', (f'%{composition}%',))
        
        results = cursor.fetchall()
        conn.close()
        
        if results:
            return [
                {
                    "medicine_name": result[0],
                    "composition": result[1],
                    "manufacturer": result[2],
                    "uses": result[3],
                    "side_effects": result[4]
                } for result in results
            ]
        
        return None
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

def get_medicine_info(search_term):
    """
    Search for medicine by brand name OR generic name (composition).
    Returns up to 5 results. Tries brand name first, then generic name.
    """
    if not search_term or not isinstance(search_term, str):
        return None
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # First try searching by medicine name (brand)
        cursor.execute('''
            SELECT medicine_name, composition, manufacturer, uses, side_effects
            FROM medicines 
            WHERE LOWER(medicine_name) LIKE LOWER(?)
            LIMIT 5
        ''', (f'%{search_term}%',))
        
        results = cursor.fetchall()
        
        # If no results, try searching by composition (generic name)
        if not results:
            cursor.execute('''
                SELECT medicine_name, composition, manufacturer, uses, side_effects
                FROM medicines 
                WHERE LOWER(composition) LIKE LOWER(?)
                LIMIT 5
            ''', (f'%{search_term}%',))
            
            results = cursor.fetchall()
        
        conn.close()
        
        if results:
            return [
                {
                    "medicine_name": result[0],
                    "composition": result[1],
                    "manufacturer": result[2],
                    "uses": result[3],
                    "side_effects": result[4]
                } for result in results
            ]
        
        return None
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None