from flask import Flask, request, render_template
from voters import *

app = Flask(__name__, template_folder="html")

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        keyword, birthdate = request.form['keyword'], request.form['birthdate']
        if len(keyword) > 1 and len(birthdate) == 8:
            query = True
            lista = listPages(birthdate)
            results = search(lista, keyword)

            return render_template("index.html", results=results, query=query)

        else:
            error = True
            return render_template("index.html", error=error)

    return render_template("index.html")

if __name__ == '__main__':
    app.run()