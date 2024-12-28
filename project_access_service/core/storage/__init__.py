"""
Register our storages
"""
from database import Session
from .base import BaseStorage
from .access_right_storage import AccessRightStorage
from .role_storage import RoleStorage
from .person_project_role_storage import PersonProjectRoleStorage
from .person_project_storage import PersonProjectStorage

base_storage = BaseStorage(Session)
access_right_storage = AccessRightStorage(Session)
role_storage = RoleStorage(Session)
person_project_role_storage = PersonProjectRoleStorage(Session)
person_project_storage = PersonProjectStorage(Session)
