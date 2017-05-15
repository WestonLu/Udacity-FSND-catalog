from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import backref

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer,ForeignKey('category.id'))
    name = Column(String(250), nullable=False)
    parent = relationship(lambda: Category, remote_side=id,)
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        try:
            return {
                'id': self.name,
                'name': self.id,
                'parent_id':self.parent.id,
                'parentname':self.parent.name,
            }
        except:
            return {
                'id': self.name,
                'name': self.id,
                'parent_id':"None",
                'parentname':"None",
            }


class Item(Base):
    __tablename__ = 'item'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    shop_id = Column(Integer, ForeignKey('shop.id'))
    shop = relationship(Shop, backref=backref("item", cascade="all,delete"))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
        }

# engine = create_engine('postgresql://catalog:catalog@localhost/shopwithusers')
engine = create_engine('sqlite:///shopwithusers.db')
if not database_exists(engine.url):
    create_database(engine.url)
Base.metadata.create_all(engine)

L11 = Category(name='Clothing, Shoes & Jewelry')
L211 = Category(name='Clothing', parent=L11)
L212 = Category(name='Shoes', parent=L11)
L213 = Category(name='Jewelry', parent=L11)

L12 = Category(name='Electronics & Computers')
L221 = Category(name='Electronics', parent=L12)
L222 = Category(name='Computers', parent=L12)

DBSession = scoped_session(sessionmaker(bind=engine))
session = DBSession()
session.add_all((L11, L211, L212, L213, L12, L221, L222))
session.commit()
session.close()