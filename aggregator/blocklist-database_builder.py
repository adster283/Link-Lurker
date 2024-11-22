import yaml
import requests
import sqlite3
import logging

def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def normalize_url(line):
    prefixes_to_remove = [
        '127.0.0.1 ', '||', '[]', '0.0.0.0', '127.0.0.1\t', '0.0.0.0\t'
    ]
    suffixes_to_remove = ['\n', '^', ' - Malware']

    for prefix in prefixes_to_remove:
        line = line.removeprefix(prefix)
    for suffix in suffixes_to_remove:
        line = line.removesuffix(suffix)
    
    if '#' in line:
        line = line.split('#')[0]

    return line.strip()

def get_or_create_url_id(cursor, url):
    """
    Insert a URL into the `urls` table if it doesn't exist, and return its ID.
    """
    cursor.execute('SELECT id FROM urls WHERE url = ?', (url,))
    result = cursor.fetchone()
    if result:
        return result[0]
    
    cursor.execute('INSERT INTO urls (url) VALUES (?)', (url,))
    return cursor.lastrowid

def insert_url_flag(cursor, url_id, category, source):
    """
    Insert a flagging record into the `url_flags` table.
    """
    cursor.execute('''
        INSERT INTO url_flags (url_id, category, source)
        VALUES (?, ?, ?)
    ''', (url_id, category, source))

def search_url(cursor, search_url):
    """
    Search for a URL and return all associated categories and sources.
    """
    cursor.execute('''
        SELECT u.url, f.category, f.source
        FROM urls u
        JOIN url_flags f ON u.id = f.url_id
        WHERE u.url = ?
    ''', (search_url,))
    return cursor.fetchall()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Connect to the database
    conn = sqlite3.connect('../domain.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY,
            url TEXT NOT NULL UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS url_flags (
            id INTEGER PRIMARY KEY,
            url_id INTEGER NOT NULL,
            category TEXT,
            source TEXT,
            FOREIGN KEY (url_id) REFERENCES urls(id)
        )
    ''')
    conn.commit()

    # Load config and process URLs
    config = load_config('config.yaml')
    for category, urls in config['blocklists'].items():
        for url in urls:
            logging.info(f"Processing {url} under category '{category}'")
            
            response = requests.get(url)
            raw_urls = response.text.splitlines()

            # Process and normalize URLs
            unique_urls = {
                normalize_url(line) for line in raw_urls
                if len(line) > 1 and not line.startswith('#') and 'localhost' not in line
            }

            # Insert URLs and flags
            for line in unique_urls:
                url_id = get_or_create_url_id(cursor, line)
                insert_url_flag(cursor, url_id, category, url)
            
            conn.commit()

    # Search example
    search_result = search_url(cursor, 'go.gisma.com')
    logging.info(f"Search results for 'go.gisma.com': {search_result}")

    # Close the connection
    conn.close()
