from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)

conn = sqlite3.connect('test.db', check_same_thread=False)
conn.row_factory=sqlite3.Row
print("database opened")

cur = conn.cursor()


@app.route('/', methods=['GET', 'POST'])
def search():
    search_term = None
    if request.method == 'POST':
        search_term = request.form['search_term']
        if not search_term:
            # handle the case where the search term is not provided
            print("not search")
            return render_template('results.html', error='Please enter a search term')
        query = f"SELECT * FROM booktoScrape WHERE title LIKE '%{search_term}%'"
        try:
            cur.execute(query)
            results = cur.fetchall()
        except Exception as e:
            # handle errors that may occur while interacting with the database
            return render_template('results.html', error=str(e))
        # You can now use the search_term to search your database or perform some other task
        return render_template('results.html', results=results)
    return render_template('search.html')

if __name__ == '__main__':
    app.run()