from app.db import db
from app import models


def create_tables():
    db.create_tables([models.Library, models.Song])
