from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String
 
engine = create_engine('sqlite:///example.db', echo=True)
Base = declarative_base()
 
########################################################################
class Book(Base):
    """"""
    __tablename__ = "books"
 
    id = Column(Integer, primary_key = True)
    title = Column(String)
    author = Column(String)
 
    #----------------------------------------------------------------------
    def __init__(self, title, author):
        """Constructor"""
        self.title = title
        self.author = author
 
 
########################################################################
class Character(Base):
    """"""
    __tablename__ = "characters"
 
    id = Column(Integer, primary_key = True)
    first_name = Column(String)
    last_name = Column(String)
    book_id = Column(ForeignKey("books.id"))
    book = relationship("Book", backref=backref("characters", order_by=id))
 
    #----------------------------------------------------------------------
    def __init__(self, first_name, last_name):
        """Constructor"""
        self.first_name = first_name
        self.last_name = last_name
 
 
    #----------------------------------------------------------------------
    @property
    def fullname(self):
        """"""
        return "%s %s" % (self.first_name, self.last_name)
 
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return "<Character('%s')>" % self.fullname
 
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
print
new_char = Character("Hermione", "Granger")
new_char.book = Book("Harry Potter", "JK Rowling")
session.add(new_char)
new_char = Character("Sherlock", "Holmes")
new_char.book = Book("The Adventure of the Creeping Man", "Arthur Conan Doyle")
session.add(new_char)
session.commit()
