from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import Boolean
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

listeners_releasesers = Table('listeners_releases',
    Base.metadata,
    Column('listener_id', Integer, ForeignKey('listener.id')),
    Column('release_id', Integer, ForeignKey('release.id'))
)

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
    musician = relationship('Musician', secondary="listeners_releasesers", backref='listeners_releasesers')

class Listener(Base):
    __tablename__ = "listener"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=False, nullable=False)
    date = Column(Date, unique=False, nullable=False)
    services = Column(String(80), unique=False, nullable=False)

    release_id = Column(Integer, ForeignKey('release.id'), unique=False, nullable=False)
    release = relationship('Release', secondary="listeners_releasesers", backref='listeners_releasesers')

    def add_release(self, release):
        self.release.append(release)
        return self

    def remove_release(self, release):
        self.release.remove(release)
        return self



# class ListenersToReleases(Base):
#     __tablename__ = "listeners_releases"

#     listener_id = Column(Integer, ForeignKey('listener.id'), unique=False, nullable=False)
#     release_id = Column(Integer, ForeignKey('release.id'), unique=False, nullable=False)
#     release = relationship('Release', backref='listeners')
#     listener = relationship('Listener', backref='releases')

    # release_id = Column(Integer, ForeignKey('release.id'), unique=False, nullable=False)

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

    # region get_all
    def get_all_musicians(self):
        return list(map(lambda x: vars(x), self.session.query(Musician).all()))

    def get_all_releases(self):
        return list(map(lambda x: vars(x), self.session.query(Release).all()))

    def get_all_listeners(self):
        return list(map(lambda x: vars(x), self.session.query(Listener).all()))
    # endregion

    # region get_by_id
    def get_musician_by_id(self, id):
        return vars(self.session.query(Musician).filter(Musician.id == id).first())
        
    def get_release_by_id(self, id):
        return vars(self.session.query(Release).filter(Release.id == id).first())

    def get_listener_by_id(self, id):
        return vars(self.session.query(Listener).filter(Listener.id == id).first())

    # def sample(self):
    #     Listener.add_release(get_release_by_id(0))
    # endregion

    # region get_by_id
    # def delete_musician_by_id(self, id):
    #     return vars(self.session.query(Musician).filter(Musician.id == id).first())
        
    # def delete_release_by_id(self, id):
    #     return vars(self.session.query(Release).filter(Release.id == id).first())

    # def delete_listener_by_id(self, id):
    #     return vars(self.session.query(Listener).filter(Listener.id == id).first())
    # endregion