from peewee import SqliteDatabase

db = SqliteDatabase("flaccy.db")
db.connect()
