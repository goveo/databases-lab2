from flask import Flask, render_template, request
from database.database import Database
from pprint import pprint
app = Flask(__name__)
app.config['SECRET_KEY'] = 'asysasamba228dtu123'

database = Database("postgres://postgres:1@127.0.0.1:5432/postgres")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get")
def get():
    # database.create_musician(name="goveo", status="rock", members="goveo")
    musicians = database.get_all_musicians()
    return render_template('musicians.html', musicians=musicians)

if __name__ == '__main__':
    app.run()
    