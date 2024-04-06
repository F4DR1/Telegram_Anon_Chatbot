# Подключаем библиотеку
import sqlite3
from config import DATABASE

class Users:
    # Функция для соединения с БД
    def create_connect(self):
        self.connect = sqlite3.connect(DATABASE)
        self.cursor = self.connect.cursor()



    # Добавляем нового пользователя
    def put(self, user_id, gender, age):
        self.create_connect()
        self.cursor.execute(f"INSERT INTO users(id, gender, age) VALUES({user_id}, '{gender}', '{age}')")
        self.connect.commit()

    # Меняем значение поля
    def post(self, user_id, field, value):
        self.create_connect()
        self.cursor.execute(f"UPDATE users SET {field}='{value}' WHERE id={user_id}")
        self.connect.commit()

    # Получаем заданное поле по пользователю
    def get(self, user_id, field = "id"):
        self.create_connect()
        txt = ""
        if user_id is not None:
            txt = f" WHERE id={user_id}"
        result = self.cursor.execute(f"SELECT {field} FROM users{txt}")
        return result



class Searches:
    # Функция для соединения с БД
    def create_connect(self):
        self.connect = sqlite3.connect(DATABASE)
        self.cursor = self.connect.cursor()



    # Добавляем нового пользователя
    def put(self, user_id, language):
        self.create_connect()
        self.cursor.execute(f"INSERT INTO searches(user_id, language) VALUES({user_id}, '{language}')")
        self.connect.commit()

    # Меняем значение поля
    def post(self, user_id, field, value):
        self.create_connect()
        self.cursor.execute(f"UPDATE searches SET {field}='{value}' WHERE user_id={user_id}")
        self.connect.commit()

    # Получаем заданное поле по пользователю
    def get(self, user_id, field = "user_id"):
        self.create_connect()
        txt = ""
        if user_id is not None:
            txt = f" WHERE user_id={user_id}"
        result = self.cursor.execute(f"SELECT {field} FROM searches{txt}")
        return result



class Chats:
    # Функция для соединения с БД
    def create_connect(self):
        self.connect = sqlite3.connect(DATABASE)
        self.cursor = self.connect.cursor()



    # Добавляем новый чат в базу
    def put(self, user_id, partner_user_id):
        self.create_connect()
        self.cursor.execute(f"INSERT INTO chats(user_id, partner_user_id) VALUES({user_id}, {partner_user_id})")
        self.connect.commit()

    # Получаем заданное поле по пользователю
    def get(self, user_id, field):
        self.create_connect()
        result = self.cursor.execute(f"SELECT {field} FROM chats WHERE user_id={user_id}")
        return result
    
    # Удаляем чат из базы
    def delete(self, user_id):
        self.create_connect()
        self.cursor.execute(f"DELETE FROM chats WHERE user_id={user_id}")
        self.connect.commit()



class Premiums:
    # Функция для соединения с БД
    def create_connect(self):
        self.connect = sqlite3.connect(DATABASE)
        self.cursor = self.connect.cursor()



    # Добавляем новую запись
    def put(self, user_id, type, date, duration):
        self.create_connect()
        self.cursor.execute(f"INSERT INTO premiums(user_id, type, date, duration) VALUES({user_id}, '{type}', '{date}', '{duration}')")
        self.connect.commit()

    # Меняем значение поля записи
    def post(self, user_id, field, value):
        self.create_connect()
        self.cursor.execute(f"UPDATE premiums SET {field}='{value}' WHERE id={user_id}")
        self.connect.commit()

    # Получаем заданное поле по пользователю
    def get(self, user_id, field = "id"):
        self.create_connect()
        txt = ""
        if user_id is not None:
            txt = f" WHERE user_id={user_id}"
        result = self.cursor.execute(f"SELECT {field} FROM premiums{txt}")
        return result
    
    # Удаляем запись из базы
    def delete(self, user_id):
        self.create_connect()
        self.cursor.execute(f"DELETE FROM premiums WHERE user_id={user_id}")
        self.connect.commit()
