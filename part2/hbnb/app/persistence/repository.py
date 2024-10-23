from abc import ABC, abstractmethod


class Repository(ABC):
    """
    Abstract base class for a generic repository.

    This class defines the interface for a data repository. Subclasses must implement
    methods to manage data objects, such as adding, retrieving, updating, and deleting.

    Methods:
        add(obj): Add a new object to the repository.
        get(obj_id): Retrieve an object by its ID.
        get_all(): Retrieve all objects from the repository.
        update(obj_id, data): Update an existing object by its ID.
        delete(obj_id): Delete an object by its ID.
        get_by_attribute(attr_name, attr_value): Retrieve an object by a specific attribute.
    """


    @abstractmethod
    def add(self, obj):
        """
        Add a new object to the repository.

        Args:
            obj: The object to be added.
        """
        pass


    @abstractmethod
    def get(self, obj_id):
        """
        Retrieve an object by its ID.

        Args:
            obj_id (str): The ID of the object to retrieve.

        Returns:
            The object associated with the given ID, or None if not found.
        """
        pass


    @abstractmethod
    def get_all(self):
        """
        Retrieve all objects from the repository.

        Returns:
            A list of all objects in the repository.
        """
        pass


    @abstractmethod
    def update(self, obj_id, data):
        """
        Update an existing object by its ID.

        Args:
            obj_id (str): The ID of the object to update.
            data (dict): A dictionary of new values to update the object with.
        """
        pass


    @abstractmethod
    def delete(self, obj_id):
        """
        Delete an object by its ID.

        Args:
            obj_id (str): The ID of the object to delete.
        """
        pass


    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve an object by a specific attribute.

        Args:
            attr_name (str): The name of the attribute to filter by.
            attr_value: The value of the attribute to match.

        Returns:
            The first object that matches the attribute value, or None if not found.
        """
        pass


class InMemoryRepository(Repository):
    """
    In-memory implementation of the Repository interface.

    This class stores objects in a dictionary for quick access and manipulation
    during the application's runtime. Suitable for testing and small-scale applications.

    Attributes:
        _storage (dict): A dictionary that stores objects using their IDs as keys.
    """


    def __init__(self):
        """
        Initialize the in-memory storage dictionary.
        """
        self._storage = {}


    def add(self, obj):
        """
        Add a new object to the repository.

        Args:
            obj: The object to be added.
        """
        self._storage[obj.id] = obj


    def get(self, obj_id):
        """
        Retrieve an object by its ID.

        Args:
            obj_id (str): The ID of the object to retrieve.

        Returns:
            The object associated with the given ID, or None if not found.
        """
        return self._storage.get(obj_id)


    def get_all(self):
        """
        Retrieve all objects from the repository.

        Returns:
            A list of all objects in the repository.
        """
        return list(self._storage.values())


    def update(self, obj_id, data):
        """
        Update an existing object by its ID.

        Args:
            obj_id (str): The ID of the object to update.
            data (dict): A dictionary of new values to update the object with.
        """
        obj = self.get(obj_id)
        if obj:
            obj.update(data)


    def delete(self, obj_id):
        """
        Delete an object by its ID.

        Args:
            obj_id (str): The ID of the object to delete.
        """
        if obj_id in self._storage:
            del self._storage[obj_id]


    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve an object by a specific attribute.

        Args:
            attr_name (str): The name of the attribute to filter by.
            attr_value: The value of the attribute to match.

        Returns:
            The first object that matches the attribute value, or None if not found.
        """
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)