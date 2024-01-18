#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel
from models.review import Review
from models.user import User
from models.amenity import Amenity
from os import getenv
import models
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy import MetaData

metadata = MetaData()

place_amenity = Table('place_amenity', metadata,
                     Column('place_id', String(60),
                            ForeignKey('places.id'),
                            primary_key=True,
                            nullable=False),
                     Column('amenity_id', String(60),
                            ForeignKey('amenities.id'),
                            primary_key=True,
                            nullable=False)
                     )


class Place(BaseModel):
    """ A place to stay """

    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "places"
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0

        reviews = relationship("Review", backref="place", cascade="all, delete-orphan")

        amenities = relationship("Amenity", secondary="place_amenity", viewonly=False)

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        reviews = []
        amenity_ids = []

        @property
        def amenities(self):
            """Getter attribute that returns the list of Amenity instances based on
               the attribute amenity_ids."""
            all_amenities = models.storage.all(Amenity)
            place_amenities = [amenity for amenity in all_amenities.values() if
                               amenity.id in self.amenity_ids]
            return place_amenities

        @amenities.setter
        def amenities(self, amenity):
            """Setter attribute that handles append method for adding an Amenity.id to
               the attribute amenity_ids. Accepts only Amenity object."""
            if isinstance(amenity, Amenity):
                self.amenity_ids.append(amenity.id)

