from peewee import Model
from app.db import db


class Base(Model):
    class Meta:
        database = db
