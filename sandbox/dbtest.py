import pyodbc 

conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=localhost,1433;"
                      "Database=myDB;"
                      "UID=sa;"
                      "PWD=yourStrong(!)Password;")

cursor = conn.cursor()

# query = """CREATE TABLE websites(
#         ID int,
#         URL varchar(255),
#         title varchar(255),
#         contents varchar(255),
#         last_crawl varchar(255)
# )"""

query = "INSERT INTO keywords VALUES (0,'Atom','https://atomute.github.io/',1)"
cursor.execute(query)

cursor.commit()
conn.close()


