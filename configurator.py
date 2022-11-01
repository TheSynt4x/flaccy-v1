from app import models
from app.db import db


def create_tables():
    db.create_tables([models.Library, models.Song])
