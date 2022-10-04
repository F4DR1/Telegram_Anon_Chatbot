# Подключаем библиотеку
import sqlite3

class Users:
    # Функция для соединения с БД
    def connect_to_db(self):
        self.connect = sqlite3.connect('db_telegram_bot.db')
        self.cursor = self.connect.cursor()

    # Закрываем соединение с БД
    def close(self):
        if self.connect:
            self.connect.close()



    # Получаем id всех пользователей, позже будем проверять наличие пользователя в этом списке
    def get_all_id(self):
        self.connect_to_db()
        request = "SELECT user_id FROM users"
        result = self.cursor.execute(request).fetchall()
        self.close()

        return [i[0] for i in result]

    # Добавляем нового пользователя
    def add_id_to_db(self, user_id, sex, age):
        self.connect_to_db()
        request = "INSERT INTO users(user_id, sex, age) VALUES(?, ?, ?)"
        self.cursor.execute(request, (user_id, sex, age))
        self.connect.commit()
        self.close()
    


    # Получаем заданное поле по пользователю
    def get_field(self, user_id, field):
        self.connect_to_db()
        request = f"SELECT {field} FROM users WHERE user_id=?"
        result = self.cursor.execute(request, (user_id,)).fetchone()
        self.close()
        return result[0]

    # Меняем значение поля
    def set_field(self, user_id, field, value):
        self.connect_to_db()
        request = f"UPDATE users SET {field}=? WHERE user_id=?"
        self.cursor.execute(request, (value, user_id))
        self.connect.commit()
        self.close()