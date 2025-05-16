import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


viewers_table = sqlalchemy.Table(
        'viewers',
        SqlAlchemyBase.metadata,
        sqlalchemy.Column('book_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('books.id')),
        sqlalchemy.Column('user_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('users.id'))
    )


class Book(SqlAlchemyBase):
    __tablename__ = 'books'



    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    path = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, 
                                     default=datetime.datetime.now)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    views = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')
    categories = orm.relationship("Category",
                                  secondary="association",
                                  backref="books")
    views = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    viewers = orm.relationship("User",
                               secondary=viewers_table,
                               backref="viewed_books")