import mysql.connector
from serpapi import GoogleSearch

def connect_to_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nugget101!",
        database="internship_data"
    )

def insert_into_mysql(job, title, link):
    conn = connect_to_mysql()
    cursor = conn.cursor()
    
    # Check if the entry already exists
    cursor.execute("SELECT id FROM search_results WHERE job = %s AND title = %s AND link = %s", (job, title, link))
    existing_entry = cursor.fetchone()
    if existing_entry:
        print(f"Entry already exists: Job='{job}', Title='{title}', Link='{link}'")
    else:
        # Insert the entry if it doesn't exist
        sql = "INSERT INTO search_results (job, title, link) VALUES (%s, %s, %s)"
        values = (job, title, link)
        cursor.execute(sql, values)
        conn.commit()
        print(f"Inserted new entry: Job='{job}', Title='{title}', Link='{link}'")
    
    cursor.close()
    conn.close()

def search_and_store_internships(job):
    params = { 
        "q": job + " internship",
        "location": "Sterling, Virginia, United States",
        "hl": "en",
        "gl": "us",
        "engine": "google",
        "api_key": "c3edd2244f509a56c14fa9061eb3042e7a708dc4167235dc24764a9a954a41f9"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    
    print(f"Search Results for '{job}' Internships:")
    print("=" * 50)  
    
    for i, result in enumerate(results['organic_results'], 1):
        title = result['title']
        link = result['link']
        print(f"RESULT #{i}:")
        print(f"Title: {title}")
        print(f"Link: {link}")
        print("-" * 50)
        
        insert_into_mysql(job, title, link)


search_and_store_internships("Data Analytic")
