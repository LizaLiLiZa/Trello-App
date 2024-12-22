import datetime
import json
import os


def Delete_old_reviews(last_year):
    """
    Удаляет отзывы, которые были добавлены позже какой-то даты
    """
    if not os.path.exists("./core/db/all_comments.json"):
        print("Отзывов нету.")
        return
    with open("./core/db/all_comments.json", "r+", encoding="utf-8") as f:
        data = json.load(f)
        updated_data = []
        for review in data:
            review_date = datetime.datetime.strptime(review["date"], "%m/%d/%Y")
            if review_date.year >= last_year:
                updated_data.append(review)
        f.seek(0)  # Перемещаем указатель в начало файла
        json.dump(updated_data, f, indent=4, ensure_ascii=False)
        f.truncate()  # Обрезаем файл, чтобы удалить старые данные

    print(f"Отзывы до {last_year} года были удалены.")

