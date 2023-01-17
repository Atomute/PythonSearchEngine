import tkinter as tk
import sqlite3

class SearchEngine(tk.Tk):
    def __init__(self):
        #create frame
        tk.Tk.__init__(self)
        frame = tk.Frame(self)
        self.entry = tk.Entry(frame, width=50)
        self.button = tk.Button(frame, text="Search", command=self.on_search)
        self.results_text = tk.Text(self, width=100, height=30 )
        update_frame = tk.Frame(self)
        self.entry2 = tk.Entry(update_frame, width=50)
        self.button2 = tk.Button(update_frame, text="Update", command=self.on_update)

        self.entry.pack(side="left")
        self.button.pack(side="left")
        frame.pack()
        self.entry2.pack(side="left")
        self.button2.pack(side="left")
        update_frame.pack()
        self.results_text.pack()

    def on_update(self):
        #get text from input 
        pass

    def on_search(self):
        # get text from input 
        query = self.entry.get()

        #Use query find match text
        results = self.perform_search(query)
        #Display data
        self.display_results(results)

    def perform_search(self, query):
        # Connect to the database
        conn = sqlite3.connect("test.sqlite")
        c = conn.cursor()
        query = "%" + query + "%"
        #Query Find exact word from user input
        c.execute("SELECT * FROM websites WHERE content LIKE ?", (query,))
        
        results = c.fetchall()

        # disconnection database
        conn.close()

        return results
    def display_results(self, results):
        print(len(results))
        # Clear the results text widget
        self.results_text.delete("1.0", "end")
        # Insert the results into the widget
        for result in results:
            print('id=',result[0])
            title, url = result[2], result[1]
            result_str = f"{title}\n : {url}"
            self.results_text.insert("end", result_str + "\n")


if __name__ == "__main__":
    app = SearchEngine()
    app.mainloop()