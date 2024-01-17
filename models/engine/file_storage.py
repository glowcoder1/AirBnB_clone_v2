#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None) -> dict:
        """Returns a dictionary of models of specified class
        currently in storage
        """
        from models.base_model import Base
        from models.amenity import Amenity
        from models.city import City
        from models.place import Place
        from models.review import Review
        from models.state import State
        from models.user import User

        if cls:
            cls_dict = {}
            if isinstance(cls, str):
                cls = eval(cls)
            cls_name = cls.__name__
            all_objs = FileStorage.__objects
            for key, val in all_objs.items():
                if key.split(".")[0] == cls_name:
                    cls_dict.update({key: val})
            return cls_dict
        return FileStorage.__objects

    def delete(self, obj=None):
        """Deletes obj instance from local storage FileStorage.__objects"""
        if obj is None:
            return
        obj_key = "{}.{}".format(type(obj).__name__, obj.id)
        del FileStorage.__objects[obj_key]
        self.save()

    def new(self, obj):
        """Adds new obj to storage dictionary"""
        self.all().update({obj.to_dict()["__class__"] + "." + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, "w") as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "Place": Place,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Review": Review,
        }
        try:
            temp = {}
            with open(FileStorage.__file_path, "r") as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val["__class__"]](**val)
        except FileNotFoundError:
            pass
