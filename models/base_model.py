#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
import models
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Column

Base = declarative_base()
date_form = "%Y-%m-%dT%H:%M:%S.%f"

class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """initializes instance of a class"""

        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at
        self.id= str(uuid.uuid4())

        if kwargs:
            for key, value in kwargs.items():
                if (key != "__class__"):
                    if (key == "updated_at" or key == "created_at"):
                        value = datetime.strptime(value, date_form)

                    setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        filtered_dict = {key: value for key, value in self.__dict__.items()
                         if key != "_sa_instance_state"}
        return '[{}] ({}) {}'.format(self.__class__.__name__,
                                     self.id, filtered_dict)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dict_copy = self.__dict__.copy()
        dict_copy['__class__'] = self.__class__.__name__
        dict_copy["created_at"] = dict_copy["created_at"].strftime(date_form)
        dict_copy["updated_at"] = dict_copy["updated_at"].strftime(date_form)
        if "_sa_instance_state" in dict_copy:
            dict_copy.pop("_sa_instance_state", None)

        return dict_copy

    def delete(self):
        """delete the current instance from the storage """
        models.storage.delete(self)
