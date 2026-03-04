import json
import sqlite3
import pandas as pd
import os


DB_PATH = 'db/drug_interactions.db'
JSON_PATH = 'dataset/drug_interactions_dataset.json'

def initialize_interaction_db():
    """
    Create SQLite database and schema.
    Drops existing table and creates fresh one.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Drop existing table if it exists
    cursor.execute('DROP TABLE IF EXISTS drug_interactions')
    
    # Create drug_interactions table
    cursor.execute('''
        CREATE TABLE drug_interactions (
            interaction_id INTEGER PRIMARY KEY,
            drug_a TEXT NOT NULL,
            drug_b TEXT NOT NULL,
            severity TEXT NOT NULL,
            mechanism TEXT,
            clinical_effect TEXT,
            safer_alternative TEXT,
            clinical_management TEXT,
            reference TEXT
            )
        ''')
    

    #Drop existing indexes if they exist
    cursor.execute('DROP INDEX IF EXISTS idx_drug_a')
    cursor.execute('DROP INDEX IF EXISTS idx_drug_b')
    cursor.execute('DROP INDEX IF EXISTS idx_severity')
    cursor.execute('DROP INDEX IF EXISTS idx_drug_pair')
    
    # -- Index on drug_a for fast lookup
    cursor.execute('CREATE INDEX idx_drug_a ON drug_interactions(drug_a);')
    
    # -- Index on drug_b for fast lookup
    cursor.execute('CREATE INDEX idx_drug_b ON drug_interactions(drug_b);')

    # -- Index on severity for filtering by severity level
    cursor.execute('CREATE INDEX idx_severity ON drug_interactions(severity);')

    # -- Composite index for checking interactions between two drugs
    cursor.execute('CREATE INDEX idx_drug_pair ON drug_interactions(drug_a, drug_b);')

    conn.commit()
    conn.close()
    print("✓ Database schema created successfully!")


def insert_interactions_from_json():
    """
    Initialize database schema and read JSON file to insert drug interaction data into database.
    """
    
    # Initialize database schema first
    initialize_interaction_db()
    
    # Check if JSON exists
    if not os.path.exists(JSON_PATH):
        print(f"Error: JSON file not found at {JSON_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    with open(JSON_PATH, 'r') as f:
        data = json.load(f)
        interactions = data['ddi_database']
        for interaction in interactions:
            cursor.execute('''
                INSERT INTO drug_interactions (
                    interaction_id, drug_a, drug_b, severity, mechanism, clinical_effect, safer_alternative, clinical_management, reference
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                interaction.get('interaction_id'),
                interaction.get('drug_a'),
                interaction.get('drug_b'),
                interaction.get('severity'),
                interaction.get('mechanism'),
                interaction.get('clinical_effect'),
                interaction.get('safer_alternative'),
                interaction.get('clinical_management'),
                interaction.get('reference')
            ))
    conn.commit()
    
    # Verify import
    cursor.execute('SELECT COUNT(*) FROM drug_interactions')
    count = cursor.fetchone()[0]
    
    conn.close()
    print(f"✓ Drug interaction data inserted successfully!")
    print(f"✓ Total interactions inserted: {count}")


def check_drug_interaction(drug_a, drug_b):
    """
    Check if there is a known interaction between drug_a and drug_b.
    Returns interaction details if found, else returns None.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check for interaction in both directions (drug_a, drug_b) and (drug_b, drug_a)
    cursor.execute('''
        SELECT * FROM drug_interactions 
        WHERE (drug_a = ? AND drug_b = ?) OR (drug_a = ? AND drug_b = ?)
    ''', (drug_a, drug_b, drug_b, drug_a))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            "interaction_id": result[0],
            "drug_a": result[1],
            "drug_b": result[2],
            "severity": result[3],
            "mechanism": result[4],
            "clinical_effect": result[5],
            "safer_alternative": result[6],
            "clinical_management": result[7],
            "reference": result[8]
        }
    else:
        return None