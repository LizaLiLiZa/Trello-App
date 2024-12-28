"""
Register our storages
"""
from database import Session
from .project_storage import ProjectStorage
from .board_storage import BoardStorage
from .state_storage import StateStorage
from .task_categories_storage import TaskCategoriesStorage
from .task_mean_storage import TaskMeanStorage
from .task_storage import TaskStorage
from .delete_storage import DeleteStorage
from .base import BaseStorage

base_storage = BaseStorage(Session)
project_storage = ProjectStorage(Session)
board_storage = BoardStorage(Session)
state_storage = StateStorage(Session)
task_categories_storage = TaskCategoriesStorage(Session)
task_mean_storage = TaskMeanStorage(Session)
task_storage = TaskStorage(Session)
delete_storage = DeleteStorage(Session)
