import pyodbc

conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=localhost,1436;"
                      "Database=testDB;"
                      "UID=sa;"
                      "PWD=1Secure*Password1;")

cursor = conn.cursor()        
createWebsites = """CREATE TABLE websites (
                    ID int,
                    URL text,
                    title text,
                    content text,
                    last_crawl DATETIME)"""

cursor.execute(createWebsites)

createkeywords = """CREATE TABLE keywords (
                    keywordID int,
                    keyword text,
                    URL text,
                    count int)"""

cursor.execute(createkeywords)

cursor.commit()
conn.close()