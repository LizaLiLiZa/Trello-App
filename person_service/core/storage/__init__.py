"""
Register our storages
"""
from database import Session
from .person.person_storage import PersonStorage
from .base import BaseStorage

base_storage = BaseStorage(Session)
person_storage = PersonStorage(Session)