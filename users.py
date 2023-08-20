import sqlite3, config

class User:

    message_for_blocked_user = "Шановний, %s, ви заблоковані!!!"
    message_if_not_admin = "Шановний, %s, ця команда тільки для адміністраторів!!!"

    def __init__(self):
        self.connection = sqlite3.connect(config.DB_NAME)
        self.cursor = self.connection.cursor()

    def result_to_dict(self, result, cursor) -> dict:           
        columns = [column[0] for column in cursor.description]            
        return dict(zip(columns, result))

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id`= ?", (user_id,)).fetchall()
            return bool(len(result))

    def set_nickname(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `nickname` = ? WHERE `user_id`= ?", (nickname, user_id,))

    def get_user_info(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id`= ?", (user_id,)).fetchone()
            return self.result_to_dict(result, self.cursor)
        
    def get_user_list(self):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id`= ?", (user_id,)).fetchall()
            return result

    def set_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `signup` = ? WHERE `user_id`= ?", (signup, user_id,))

    def set_block(self, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `blocked` = ? WHERE `user_id`= ?", (True, user_id,))
    
    def set_unblok(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `blocked` = ? WHERE `user_id`= ?", (False, user_id,))
        