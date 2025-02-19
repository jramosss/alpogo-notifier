from peewee import SqliteDatabase


db = SqliteDatabase('test.db')


def setup_database():
    db.connect()
    yield db
    db.close()