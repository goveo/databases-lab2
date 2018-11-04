from app import db

class Listener(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    date = db.Column(db.Date, unique=False, nullable=False)
    services = db.Column(db.String(80), unique=False, nullable=False)

    release_id = db.Column(db.Integer, db.ForeignKey('release.id'), unique=False, nullable=False)
    release = db.relationship('Release', backref=db.backref('listeners', lazy=True))
