#!./pdf_python/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref

engine = create_engine('sqlite:///rstv.db', convert_unicode=True)
Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    shortname = Column(String(50))
    chapters = relationship("Chapter", backref="book")

    def __repr__(self):
        return "<Book title(name='%s', shortnames='%s')>" % (
                                self.name, self.shortname)


class Chapter(Base):
    __tablename__ = 'chapters'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    number = Column(Integer)
    book_id = Column(Integer, ForeignKey('books.id'))
    verses = relationship("Verse", backref="chapter")

    def __repr__(self):
        return "<Chapter (name='%s', book='%s')>" % (
                self.name, self.book)


class Verse(Base):
    __tablename__ = 'verses'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    number = Column(Integer)
    chapter_id = Column(Integer, ForeignKey('chapters.id'))

    def __repr__(self):
        return "Verse number:'%s'; unique_id:'%s'" % (
                self.number, self.id)

Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

