"""This module is used to perform CRUD operations on the database"""

from typing import Any, List, Optional

from bson import ObjectId
from bson import errors as bsonErrors
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError


class UserModel(BaseModel):
    """
    BaseModel class for the User class
    """

    name: str
    email: str
    password: str


class Connection:
    """This class is used to connect to the database and perform operations on it"""

    def __init__(self, host: str) -> None:
        """This constructor is used to connect to the database and get the collection"""
        try:
            self.my_collection: Collection[Any] = MongoClient(host=host).get_default_database().get_collection("identity")
            self.is_connected = True
        except PyMongoError:
            self.is_connected = False

    def get_all_document(self) -> List[UserModel]:
        """Gets all the documents from the collection

        Returns:
            list: A list of all the documents
        """
        return list(self.my_collection.find())

    def get_one_document(self, doc_id: str) -> Optional[UserModel]:
        """Returns a document from the collection

        Args:
            doc_id (str): The doc_id of the document to be returned

        Returns:
            dict: The document
        """

        try:
            return self.my_collection.find_one({"_id": ObjectId(doc_id)})
        except bsonErrors.InvalidId:
            return None

    def insert_in_collection(self, document: UserModel) -> bool:
        """Inserts a document in the collection

        Args:
            document (dict): A dictionary containing the document to be inserted

        Returns:
            bool: Returns True if the document is inserted successfully, else False
        """

        return self.my_collection.insert_one({"name": document.name, "email": document.email, "password": document.password}).acknowledged

    def delete_one_document(self, doc_id: str) -> bool:
        """Deletes a document from the collection

        Args:
            doc_id (str): The doc_id of the document to be deleted

        Returns:
            bool: Returns True if the document is deleted successfully, else False
        """
        try:
            return self.my_collection.delete_one({"_id": ObjectId(doc_id)}).acknowledged

        except bsonErrors.InvalidId:
            return False

    def update_one_document(self, doc_id: str, document: UserModel) -> bool:
        """Updates a document in the collection

        Args:
            doc_id (str): The doc_id of the document to be updated
            document (dict): A dictionary containing the updated document

        Returns:
            bool: Returns True if the document is updated successfully, else False
        """
        try:
            return self.my_collection.update_one({"_id": ObjectId(doc_id)}, {"$set": document}).acknowledged

        except bsonErrors.InvalidId:
            return False
