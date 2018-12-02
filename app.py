from flask import Flask, render_template, request
from database.database import Database
from pprint import pprint
import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = 'asysasamba228dtu123'

database = Database("postgres://postgres:1@127.0.0.1:5432/postgres")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/musicians")
def get_musicians():
    # database.create_musician(name="goveo", status="rock", members="goveo")
    musicians = database.get_all_musicians()
    return render_template('musicians.html', musicians=musicians)

@app.route("/musicians/<int:id>", methods = ['GET'])
def get_musician(id):
    if request.method == 'GET':
        # print('id : ', id)
        musician = database.get_musician_by_id(id)
        # print("musician: ", musician)
        return render_template('musician.html', musician=musician)

@app.route("/releases")
def get_releases():
    releases = database.get_all_releases()
    return render_template('releases.html', releases=releases)

@app.route("/listeners")
def get_listeners():
    listeners = database.get_all_listeners()
    return render_template('listeners.html', listeners=listeners)


if __name__ == '__main__':
    app.run(debug=True)
    database.create_musician(name="musician1", status="solo artist", members="Yury")
    database.create_release(name="release1", date=datetime.date(1999, 5, 1), style="rap", is_video=False, musician_id=1)
    database.create_listener(name="listener1", date=datetime.date(1999, 5, 1), services="facebook", release_id=1)