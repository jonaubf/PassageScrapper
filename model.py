#!./pdf_python/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref

engine = create_engine('sqlite:///rstv.db', convert_unicode=True)
Base = declarative_base()


class Book(Base):
    """
    class Book describes table, that contains info about the current book of the Bible
    name - Book's name
    shortnames - list of the sorten names of the book
    chapters - backref for the chapters of the current book
    """
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    shortname = Column(String(50))
    chapters = relationship("Chapter", backref="book")

    def __repr__(self):
        return "<Book title(name='%s', shortnames='%s')>" % (
                                self.name, self.shortname)


class Chapter(Base):
    """
    class Chapter describes table, that contains info about the current chapter
    name - textual number of the chapter
    number - Integer number of the chapter
    book_id - Foreign key that points to the book chapter belongs
    verses - backref for the verses of the chapter
    """
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
    """
    class Verse describes table, that contains info about each verse
    text - text of the verse
    number - it's number
    chapter_id - reference to the chapter this verse belongs
    """
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

