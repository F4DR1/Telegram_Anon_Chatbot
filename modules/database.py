# Подключаем библиотеку
import sqlite3
from config import DATABASE

# Пользователи
class Users:
    # Функция для соединения с БД
    def create_connect(self):
        self.database = "users"
        self.connect = sqlite3.connect(DATABASE)
        self.cursor = self.connect.cursor()



    # Добавляем нового пользователя
    def put(self, user_id, gender, age, language):
        self.create_connect()
        self.cursor.execute(f"INSERT INTO {self.database}(id, gender, age, language) VALUES({user_id}, '{gender}', '{age}', '{language}')")
        self.connect.commit()

    # Меняем значение поля
    def post(self, user_id, field, value):
        self.create_connect()
        self.cursor.execute(f"UPDATE {self.database} SET {field}='{value}' WHERE id={user_id}")
        self.connect.commit()

    # Получаем заданное поле по пользователю
    def get(self, user_id, field = "id"):
        self.create_connect()
        txt = ""
        if user_id is not None:
            txt = f" WHERE id={user_id}"
        result = self.cursor.execute(f"SELECT {field} FROM {self.database}{txt}")
        return result



# Поиск
class Searches:
    # Функция для соединения с БД
    def create_connect(self):
        self.database = "searches"
        self.connect = sqlite3.connect(DATABASE)
        self.cursor = self.connect.cursor()



    # Добавляем нового пользователя
    def put(self, user_id, language):
        self.create_connect()
        self.cursor.execute(f"INSERT INTO {self.database}(user_id, language) VALUES({user_id}, '{language}')")
        self.connect.commit()

    # Меняем значение поля
    def post(self, user_id, field, value):
        self.create_connect()
        self.cursor.execute(f"UPDATE {self.database} SET {field}='{value}' WHERE user_id={user_id}")
        self.connect.commit()

    # Получаем заданное поле по пользователю
    def get(self, user_id, field = "user_id"):
        self.create_connect()
        txt = ""
        if user_id is not None:
            txt = f" WHERE user_id={user_id}"
        result = self.cursor.execute(f"SELECT {field} FROM {self.database}{txt}")
        return result



# Чаты
class Chats:
    # Функция для соединения с БД
    def create_connect(self):
        self.database = "chats"
        self.connect = sqlite3.connect(DATABASE)
        self.cursor = self.connect.cursor()



    # Добавляем новый чат в базу
    def put(self, user_id, partner_user_id):
        self.create_connect()
        self.cursor.execute(f"INSERT INTO {self.database}(user_id, partner_user_id) VALUES({user_id}, {partner_user_id})")
        self.connect.commit()

    # Получаем заданное поле по пользователю
    def get(self, user_id, field):
        self.create_connect()
        result = self.cursor.execute(f"SELECT {field} FROM {self.database} WHERE user_id={user_id}")
        return result
    
    # Удаляем чат из базы
    def delete(self, user_id):
        self.create_connect()
        self.cursor.execute(f"DELETE FROM {self.database} WHERE user_id={user_id}")
        self.connect.commit()



# Все премиумы
class Premiums:
    # Функция для соединения с БД
    def create_connect(self):
        self.database = "premiums"
        self.connect = sqlite3.connect(DATABASE)
        self.cursor = self.connect.cursor()



    # Добавляем новую запись
    def put(self, user_id, type, date, duration):
        self.create_connect()
        self.cursor.execute(f"INSERT INTO {self.database}(user_id, type, date, duration) VALUES({user_id}, '{type}', '{date}', '{duration}')")
        self.connect.commit()

    # Меняем значение поля записи
    def post(self, user_id, field, value):
        self.create_connect()
        self.cursor.execute(f"UPDATE {self.database} SET {field}='{value}' WHERE user_id={user_id}")
        self.connect.commit()

    # Получаем заданное поле по пользователю
    def get(self, user_id, field = "user_id"):
        self.create_connect()
        txt = ""
        if user_id is not None:
            txt = f" WHERE user_id={user_id}"
        result = self.cursor.execute(f"SELECT {field} FROM {self.database}{txt}")
        return result
    
    # Удаляем запись из базы
    def delete(self, user_id):
        self.create_connect()
        self.cursor.execute(f"DELETE FROM {self.database} WHERE user_id={user_id}")
        self.connect.commit()
