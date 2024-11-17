import sqlite3
import os

def create_database():
    # Ensure examples directory exists
    os.makedirs('docs/examples', exist_ok=True)
    
    # Create and connect to database
    conn = sqlite3.connect('docs/examples/population.sqlite')
    c = conn.cursor()

    # Create countries table
    c.execute('''
    CREATE TABLE countries (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        population INTEGER,
        area_km2 REAL,
        gdp_usd REAL,
        continent TEXT
    )
    ''')

    # Create cities table
    c.execute('''
    CREATE TABLE cities (
        id INTEGER PRIMARY KEY,
        country_id INTEGER,
        name TEXT NOT NULL,
        population INTEGER,
        is_capital BOOLEAN,
        latitude REAL,
        longitude REAL,
        FOREIGN KEY (country_id) REFERENCES countries(id)
    )
    ''')

    # Insert sample country data
    countries_data = [
        (1, 'China', 1439323776, 9596961, 14342903, 'Asia'),
        (2, 'India', 1380004385, 3287263, 2875142, 'Asia'),
        (3, 'United States', 331002651, 9833517, 21433226, 'North America'),
        (4, 'Indonesia', 273523615, 1904569, 1058424, 'Asia'),
        (5, 'Pakistan', 220892340, 881913, 278222, 'Asia'),
        (6, 'Brazil', 212559417, 8515770, 1839758, 'South America'),
        (7, 'Nigeria', 206139589, 923768, 448120, 'Africa'),
        (8, 'Bangladesh', 164689383, 147570, 302571, 'Asia'),
        (9, 'Russia', 145912025, 17098246, 1699877, 'Europe'),
        (10, 'Mexico', 128932753, 1964375, 1212831, 'North America')
    ]
    
    c.executemany('INSERT INTO countries VALUES (?,?,?,?,?,?)', countries_data)

    # Insert sample city data
    cities_data = [
        (1, 1, 'Beijing', 20462610, True, 39.9042, 116.4074),
        (2, 1, 'Shanghai', 27058480, False, 31.2304, 121.4737),
        (3, 2, 'New Delhi', 32941000, True, 28.6139, 77.2090),
        (4, 2, 'Mumbai', 20667656, False, 19.0760, 72.8777),
        (5, 3, 'Washington DC', 705749, True, 38.9072, -77.0369),
        (6, 3, 'New York', 8336817, False, 40.7128, -74.0060),
        (7, 4, 'Jakarta', 10562088, True, -6.2088, 106.8456),
        (8, 5, 'Islamabad', 1095064, True, 33.6844, 73.0479),
        (9, 6, 'Brasília', 3055149, True, -15.7975, -47.8919),
        (10, 7, 'Abuja', 1235880, True, 9.0765, 7.3986)
    ]
    
    c.executemany('INSERT INTO cities VALUES (?,?,?,?,?,?,?)', cities_data)

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
