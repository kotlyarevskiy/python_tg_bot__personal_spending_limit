import sqlite3, config

class Transaction:

    def __init__(self):
        self.connection = sqlite3.connect(config.DB_NAME)
        self.cursor = self.connection.cursor()
        
    def add_transaction(self, user_id, transaction_data):
           
        with self.connection:
            return self.cursor.execute("INSERT INTO `transactions` (`user_id`, `transaction_date`, `sum`, `type`, `comment`) VALUES (?, ?, ?, ?, ?)", (user_id, transaction_data['transaction_date'], transaction_data['sum'], transaction_data['type'], transaction_data['comment']))
        
