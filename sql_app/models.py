from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


from database import Base


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    last_name = Column(String(50), index=True)
    email = Column(String(50), unique=True, index=True)

    dogs = relationship('Dog', passive_deletes=True)


class Dog(Base):
    __tablename__ = "dogs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    picture = Column(String(200), index=True)
    is_adopted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    id_user = Column(Integer, ForeignKey('Users.id', ondelete='CASCADE'))
