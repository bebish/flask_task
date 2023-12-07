from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from sqlalchemy.orm import Session
from config import DATABASE_URL

#DATABASE_URL = "postgresql://begimai:1@localhost/task11"
engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Item(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    author = Column(String)
    genre = Column(String)
    created_at = Column(Date)
Base.metadata.create_all(bind=engine)
print('successfully created')



ItemPydantic = sqlalchemy_to_pydantic(Item, exclude=["id"])

db_item = ItemPydantic(title='Kassandra', author='Ch Aitmatov',genre='Fantastic',created_at = '2000-06-08')

def create_item(db_item:ItemPydantic): # C - CRUD
    db_item = Item(**db_item.dict())
    with Sessionlocal() as db:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
    return db_item
create_item(db_item)
# print('succesffully created')



def get_item():
    result = []
    with Sessionlocal() as db:
        items = db.query(Item).all()
        for item in items:
            result.append({'title':item.title, 'author':item.author, 'genre':item.genre, 'created_at':item.created_at})
    return result
# print(get_item())



def update_item(item_id:int, item:ItemPydantic):          #update
    with Sessionlocal() as db:
        db_item = db.query(Item).filter(Item.id==item_id).first()

        if db_item is None:
            return None

        for field, value in item.dict().items():
            setattr(db_item, field, value)
        db.commit()
        db.refresh(db_item)
        return db_item
# print(update_item(1,db_item))


def delete_item(item_id: int):
    with Session(engine) as session:
        item = session.query(Item).get(item_id)
        if item:
            session.delete(item)
            session.commit()
            return {'message': 'Item deleted successfully'}
        else:
            return {'message': 'Item not found'}
#print(delete_item(3))


def retrieve(item_id):          # retrieve
    with Sessionlocal() as db:
        db_item = db.query(Item).filter(Item.id==item_id).first()
         
        if db_item is None:
            return None
        return {
            'title':db_item.title,
            'author':db_item.author,
            'genre':db_item.genre,
            'created_at':db_item.created_at
        }
    
#print(retrieve(1))
