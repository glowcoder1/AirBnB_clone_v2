#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


"""
Table defining the relationship between
places and amenities
"""
place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column(
        "place_id",
        String(60),
        ForeignKey("places.id"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "amenity_id",
        String(60),
        ForeignKey("amenities.id"),
        primary_key=True,
        nullable=False,
    ),
)

class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    reviews = relationship("Review", backref="place", cascade="delete")


    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship(
            "Review", cascade="all, delete, delete-orphan", backref="place"
        )

        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            viewonly=False,
            back_populates="place_amenities",
        )

    else:

        @property
        def reviews(self) -> list:
            """Returns a list of Review instances that match self.id"""
            from models import storage

            all_objs = storage.all()
            reviews_list = []
            for key in all_objs.keys():
                review = key.replace(".", " ")
                review = shlex.split(review)
                if review[0] == "Review":
                    if all_objs[key].__dict__["place_id"] == self.id:
                        reviews_list.append(all_objs[key])
            return reviews_list

        @property
        def amenities(self) -> list:
            """
            Validates the object obj class and returns a list
            of Amenity.id linked to Place
            """
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj=None):
            from models.amenity import Amenity

            if obj:
                if type(obj) is Amenity and obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)
