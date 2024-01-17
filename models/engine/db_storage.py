#!/usr/bin/python3

"""Defines the DBStorage class engine."""

from os import getenv
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.state import State
from models.place import Place
from models.city import City
from models.review import Review
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session


class DBStorage:
    """ Database storage engine class"""

    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                                      .format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        query on the current database session (self.__session) all objects
        depending of the class name (argument cls)

        if cls=None, query all types of objects
        Return: a dictionary
        """

        if cls is None:
            all_objects = self.__session.query(User).all()
            all_objects.extend(self.__session.query(State).all())
            all_objects.extend(self.__session.query(City).all())
            all_objects.extend(self.__session.query(Place).all())
            all_objects.extend(self.__session.query(Amenity).all())
            all_objects.extend(self.__session.query(Review).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            all_objects = self.__session.query(cls).all()
            return {"{}.{}".format(type(obj).__name__, obj.id): obj
                    for obj in all_objects}

    def new(self, obj):
        """add the object to the current database session """

        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""

        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""

        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
           create all tables in the database (feature of SQLAlchemy)
           (WARNING: all classes who inherit from Base must be imported
           before calling
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
