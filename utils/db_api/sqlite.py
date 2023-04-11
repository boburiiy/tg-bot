import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def craete_table_cats(self):
        sql = '''
            CREATE TABLE cats(
                id INTEGER NOT NULL,
                name TEXT NOT NULL
            );'''
        self.execute(sql, commit=True)

    def craete_table_products(self):
        sql = '''
            CREATE TABLE products(
                id INTEGER NOT NULL,
                name TEXT NOT NULL,
                img TEXT NOT NULL,
                price INTEGER NOT NULL,
                cat_id INTEGER NOT NULL
            );'''
        self.execute(sql, commit=True)

    def create_table_cart(self):
        sql = '''CREATE TABLE cart(
            user INTEGER NOT NULL,
            item TEXT NIT NULL,
            total_amount INTEGER NOT NULL,
            count INTEGER NOT NULL,
            price INTEGER NOT NULL);
        '''
        self.execute(sql, commit=True)

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int NOT NULL,
            Name varchar(255) NOT NULL,
            email varchar(255),
            language varchar(3),
            PRIMARY KEY (id)
            );"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, name: str, email: str = None, language: str = 'uz'):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Users(id, Name, email, language) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, email, language), commit=True)

    def add_to_cart(self, user, item, total_amount, count, price):
        sql = '''INSERT INTO cart(user,item,total_amount,count,price) VALUES(?,?,?,?,?)'''
        self.execute(sql, parameters=(
            user, item, total_amount, count, price), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_cat(self, text):
        sql = '''SELECT id FROM Category WHERE text=?'''
        return self.execute(sql, parameters=(text,), fetchone=True)

    def select_prod(self, **kwargs):
        sql = '''SELECT * FROM products WHERE '''
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_all_from_cart(self, user):
        sql = 'SELECT * FROM cart WHERE user = ?'
        return self.execute(sql, parameters=(user,), fetchall=True)

    def update_cart(self, amount, count, user, item):
        sql = 'UPDATE cart set total_amount=?,count=? WHERE user = ? AND item=?'
        self.execute(sql, parameters=(amount, count, user, item), commit=True)

    def delete_pro(self, user, item):
        sql = 'DELETE FROM cart WHERE user=? AND item=?'
        self.execute(sql, parameters=(user, item), commit=True)

    def delete_all(self, user):
        sql = 'DELETE FROM cart WHERE user=?'
        self.execute(sql, parameters=(user,), commit=True)

    def selected_select(self, item, user):
        sql = 'SELECT * FROM cart WHERE item = ? AND user=?'
        return self.execute(sql, parameters=(item, user), fetchone=True)

    def all_select(self):
        sql = 'SELECT * FROM products'
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_email(self, email, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET email=? WHERE id=?
        """
        return self.execute(sql, parameters=(email, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)


def logger(statement):
    print(f"""
_____________________________________________________
Executing:
{statement}
_____________________________________________________
""")
