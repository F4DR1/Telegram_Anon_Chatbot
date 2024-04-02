# Подключаем библиотеку
import sqlite3
from config import DATABASE

class Users:
    # Функция для соединения с БД
    def create_connect(self):
        self.connect = sqlite3.connect(DATABASE)
        self.cursor = self.connect.cursor()

    # Закрываем соединение с БД
    def close_connect(self):
        if self.connect:
            self.connect.close()



    # Добавляем нового пользователя
    def put(self, user_id, gender, age):
        self.create_connect()
        self.cursor.execute(f"INSERT INTO users(id, gender, age) VALUES({user_id}, {gender}, {age})")
        self.connect.commit()
        self.close_connect()

    # Меняем значение поля
    def post(self, user_id, field, value):
        self.create_connect()
        self.cursor.execute(f"UPDATE users SET {field}={value} WHERE id={user_id}")
        self.connect.commit()
        self.close_connect()

    # Получаем заданное поле по пользователю
    def get(self, user_id, field = "id"):
        self.create_connect()
        txt = ""
        if user_id is not None:
            txt = f" WHERE id={user_id}"
        result = self.cursor.execute(f"SELECT {field} FROM users{txt}")
        self.close_connect()
        return result


class Chats:
    # Функция для соединения с БД
    def create_connect(self):
        self.connect = sqlite3.connect(DATABASE)
        self.cursor = self.connect.cursor()

    # Закрываем соединение с БД
    def close_connect(self):
        if self.connect:
            self.connect.close()



    # Добавляем новый чат в базу
    def put(self, user_id, partner_user_id):
        self.create_connect()
        self.cursor.execute(f"INSERT INTO chats(user_id, partner_user_id) VALUES({user_id}, {partner_user_id})")
        self.connect.commit()
        self.close_connect()

    # Получаем заданное поле по пользователю
    def get(self, user_id, field):
        self.create_connect()
        result = self.cursor.execute(f"SELECT {field} FROM chats WHERE id={user_id}")
        self.close_connect()
        return result
    
    # Удаляем чат из базы
    def delete(self, user_id):
        self.create_connect
        self.cursor.execute(f"DELETE FROM chats WHERE user_id={user_id}")
        self.close_connect
