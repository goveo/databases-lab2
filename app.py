from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from database import database

app = Flask(__name__)

app.config['SECRET_KEY'] = 'asysasamba228dtu123'
# app.config['SQLALCHEMY_DATABASE_URI'] = ""
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
