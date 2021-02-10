import sqlalchemy
from sqlalchemy.orm import relationship
# from sqlalchemy import Column, Integer, Text, ForeignKey
from backend.config import settings
from sqlalchemy import Table, Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



metadata = sqlalchemy.MetaData()


# from .database import Base
# class Dataset2(Base):
#     __tablename__ = 'datasets'
#     id = Column(Integer, primary_key=True)
#     name = Column(Text )
#     description = Column(Text)
#     children = relationship("User")

# class User2(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(Text )
#     surname = Column(Text)
#     parent_id = Column(Integer, ForeignKey('Dataset.id'))

datasets_table = sqlalchemy.Table(
    "datasets",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.Text),
    sqlalchemy.Column("description", sqlalchemy.Text),
    # users = relationship("User", back_populates="owner")
)

users_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.Text),
    sqlalchemy.Column("surname", sqlalchemy.Text),
    # sqlalchemy.Column("test", sqlalchemy.Text),
    # owner = relationship("Dataset", back_populates="users")
    # sqlalchemy.ForeignKey('dataset_id'),
    # sqlalchemy.Column('dataset_id', sqlalchemy.ForeignKey('datasets.id'), nullable=True),
)

users2_table = sqlalchemy.Table(
    "users2",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.Text),
    sqlalchemy.Column("surname", sqlalchemy.Text),
    # sqlalchemy.Column("test", sqlalchemy.Text),
    # owner = relationship("Dataset", back_populates="users")
    # sqlalchemy.ForeignKey('dataset_id'),
    sqlalchemy.Column('dataset_id', sqlalchemy.ForeignKey('datasets.id'), nullable=True),
)


engine = sqlalchemy.create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)
