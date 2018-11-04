from app import db

class Musician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Enum, unique=False, nullable=False)
    members = db.Column(db.String(120), unique=False, nullable=False)
