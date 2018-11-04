from app import db

class Release(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    date = db.Column(db.Date, unique=False, nullable=False)
    style = db.Column(db.String(80), unique=False, nullable=False)
    is_video = db.Column(db.Boolean, unique=False, nullable=False)
    musician_id = db.Column(db.Integer, db.ForeignKey('musician.id'), unique=False, nullable=False)
    musician = db.relationship('Musician', backref=db.backref('releases', lazy=True))