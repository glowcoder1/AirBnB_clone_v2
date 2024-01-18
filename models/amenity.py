import json

class FileStorage:
    """A class for managing file-based storage of objects."""

    # Class variable to store the file path
    __file_path = "your_file_path.json"

    # Class variable to store the objects
    __objects = {}

    def save(self):
        """
        Save the storage dictionary to a JSON file.

        This method serializes the stored objects to dictionaries,
        updates a temporary dictionary, and writes the data to a JSON file.

        Args:
            None

        Returns:
            None
        """
        # Create a copy of the storage dictionary
        serialized_objects = {key: value.to_dict() for key, value in self.__objects.items()}

        # Write the serialized objects to the JSON file
        with open(self.__file_path, "w") as file:
            json.dump(serialized_objects, file)

