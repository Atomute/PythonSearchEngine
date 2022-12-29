from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def search():
    search_term = None
    if request.method == 'POST':
        search_term = request.form['search_term']
        # You can now use the search_term to search your database or perform some other task
        return search_term
    return render_template('search.html')

if __name__ == '__main__':
    app.run()
