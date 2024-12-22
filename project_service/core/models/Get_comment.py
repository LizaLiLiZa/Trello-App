from pydantic import BaseModel


"""
    Модель для создания новой записи в бд всех записей
"""
class Get_Comment(BaseModel):
    ID_reviewer: int
    ID_under_review: int
    review: str