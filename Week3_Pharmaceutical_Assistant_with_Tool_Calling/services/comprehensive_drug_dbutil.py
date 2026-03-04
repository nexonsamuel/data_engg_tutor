import json
import sqlite3
import pandas as pd
import os


DB_PATH = 'db/comprehensive_drug.db'
CSV_PATH = 'dataset/comprehensive_drug_database.csv'

def initialize_comprehensive_drug_db():
    """
    Create SQLite database and schema.
    Drops existing table and creates fresh one.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Drop existing table if it exists
    cursor.execute('DROP TABLE IF EXISTS drugs')
    
    # Create drug_interactions table
    cursor.execute('''
        CREATE TABLE drugs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            generic_name TEXT NOT NULL UNIQUE,
            drug_class TEXT NOT NULL,
            indications TEXT,
            dosage_form TEXT,
            strength TEXT,
            route_of_administration TEXT,
            side_effects TEXT,
            contraindications TEXT,
            interaction_warnings TEXT,
            availability TEXT
            )
        ''')
    
    #Drop existing indexes if they exist
    cursor.execute('DROP INDEX IF EXISTS idx_generic_name')
    cursor.execute('DROP INDEX IF EXISTS idx_drug_class')
    cursor.execute('DROP INDEX IF EXISTS idx_availability')

    #-- Index on generic_name for fast lookup
    cursor.execute('CREATE INDEX idx_generic_name ON drugs(generic_name);')

    #-- Index on drug_class for finding therapeutic alternatives
    cursor.execute('CREATE INDEX idx_drug_class ON drugs(drug_class);')

    #-- Index on availability (OTC vs Prescription)
    cursor.execute('CREATE INDEX idx_availability ON drugs(availability);')

    conn.commit()
    conn.close()
    print("✓ Database schema created successfully!")
        

def insert_comprehensive_drugs_from_csv():
    """
    Read drug data from CSV and insert into database.
    """

    initialize_comprehensive_drug_db()  # Ensure DB is initialized before inserting data

    if not os.path.exists(CSV_PATH):
        print(f"Error: CSV file not found at {CSV_PATH}")
        return
    
    try:
        df = pd.read_csv(CSV_PATH)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for _, row in df.iterrows():
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO drugs (
                    generic_name, drug_class, indications, dosage_form, strength,
                    route_of_administration, side_effects, contraindications,
                    interaction_warnings, availability
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['Generic Name'],
                row['Drug Class'],
                row['Indications'],
                row['Dosage Form'],
                row['Strength'],
                row['Route of Administration'],
                row['Side Effects'],
                row['Contraindications'],
                row['Interaction Warnings & Precautions'],
                row['Availability']
            ))
        except Exception as e:
            print(f"Error inserting row into database: {e}")
    
    conn.commit()
    
    # Verify import
    cursor.execute('SELECT COUNT(*) FROM drugs')
    count = cursor.fetchone()[0]
    
    conn.close()
    print(f"✓ Drug data inserted successfully!")
    print(f"✓ Total records inserted: {count}")


def get_drugs_by_class(drug_class):
    """
    Retrieve all drugs in a specific drug class (for therapeutic alternatives).
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT generic_name, drug_class, indications, side_effects, availability
        FROM drugs
        WHERE drug_class = ?
    ''', (drug_class,))
    
    results = cursor.fetchall()
    conn.close()
    
    if results:
        return [
            {
                "generic_name": row[0],
                "drug_class": row[1],
                "indications": row[2],
                "side_effects": row[3],
                "availability": row[4]
            } for row in results
        ]
    
    return None

def get_drug_details(generic_name):
    """
    Get complete details of a specific drug by generic name.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT generic_name, drug_class, indications, dosage_form, strength,
               route_of_administration, side_effects, contraindications,
               interaction_warnings, availability
        FROM drugs
        WHERE generic_name = ?
    ''', (generic_name,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            "generic_name": result[0],
            "drug_class": result[1],
            "indications": result[2],
            "dosage_form": result[3],
            "strength": result[4],
            "route_of_administration": result[5],
            "side_effects": result[6],
            "contraindications": result[7],
            "interaction_warnings": result[8],
            "availability": result[9]
        }
    
    return None