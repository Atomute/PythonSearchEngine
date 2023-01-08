import sqlite3

# Connect to the database
conn = sqlite3.connect("search.db")
cursor = conn.cursor()

# Create the FTS virtual table
cursor.execute("CREATE VIRTUAL TABLE IF NOT EXISTS documents USING FTS4(title, body)")

# Populate the virtual table with data
# cursor.execute("INSERT INTO documents(title, body) VALUES (?, ?)", ("SQLite Full-Text Search", "SQLite supports full-text search through the use of the FTS module"))
# cursor.execute("INSERT INTO documents(title, body) VALUES (?, ?)", ("SQLite FTS Features", "The FTS module supports tokenizers, prefix searches, and phrase searches"))

# Perform a full-text search
cursor.execute("SELECT * FROM documents")

# Print the search results
print(cursor.fetchall())

# Close the database connection
conn.close()
