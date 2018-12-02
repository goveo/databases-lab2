from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Musician(Base):
    __tablename__ = "musician"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=False, nullable=False)
    status = Column(String(80), unique=False, nullable=False)
    members = Column(String(120), unique=False, nullable=False)

class Release(Base):
    __tablename__ = "release"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=False, nullable=False)
    date = Column(Date, unique=False, nullable=False)
    style = Column(String(80), unique=False, nullable=False)
    is_video = Column(Boolean, unique=False, nullable=False)

    musician_id = Column(Integer, ForeignKey('musician.id'), unique=False, nullable=False)
    musician = relationship('Musician', backref='releases')

class Listener(Base):
    __tablename__ = "listener"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=False, nullable=False)
    date = Column(Date, unique=False, nullable=False)
    services = Column(String(80), unique=False, nullable=False)

    release_id = Column(Integer, ForeignKey('release.id'), unique=False, nullable=False)
    release = relationship('Release', backref='listeners')

class Database():
    def __init__(self, link):
        engine = create_engine(link, echo=True)
        Base.metadata.create_all(engine) #create tables
        self.session = sessionmaker(bind=engine)()

    def create_musician(self, name, status, members):
        musician = Musician(name=name, status=status, members=members)
        self.session.add(musician)
        self.session.commit()

    def create_release(self, name, date, style, is_video, musician_id):
        release = Release(self, name=name, date=date, style=style, is_video=is_video, musician_id=musician_id)
        self.session.add(release)
        self.session.commit()

    def create_listener(self, name, date, services, release_id):
        listener = Listener(name=name, date=date, services=services, release_id=release_id)
        self.session.add(listener)
        self.session.commit()

    def get_all_musicians(self):
        return list(map(lambda x: vars(x), self.session.query(Musician).all()))

    def get_all_releases(self):
        return list(map(lambda x: vars(x), self.session.query(Release).all()))

    def get_all_listeners(self):
        return list(map(lambda x: vars(x), self.session.query(Listener).all()))
            

# class Musician(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=False, nullable=False)
#     status = db.Column(db.String(80), unique=False, nullable=False)
#     members = db.Column(db.String(120), unique=False, nullable=False)


# class Release(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=False, nullable=False)
#     date = db.Column(db.Date, unique=False, nullable=False)
#     style = db.Column(db.String(80), unique=False, nullable=False)
#     is_video = db.Column(db.Boolean, unique=False, nullable=False)
#     musician_id = db.Column(db.Integer, db.ForeignKey('musician.id'), unique=False, nullable=False)
#     musician = db.relationship('Musician', backref=db.backref('releases', lazy=True))

# class Listener(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=False, nullable=False)
#     date = db.Column(db.Date, unique=False, nullable=False)
#     services = db.Column(db.String(80), unique=False, nullable=False)

#     release_id = db.Column(db.Integer, db.ForeignKey('release.id'), unique=False, nullable=False)
#     release = db.relationship('Release', backref=db.backref('listeners', lazy=True))