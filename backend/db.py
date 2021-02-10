from databases import Database

from backend.config import settings


def get_database():
    database = Database(settings.DATABASE_URL)
    return database
