"""
Database initialization for the Smart Band Edge Service.
"""
from peewee import SqliteDatabase

db = SqliteDatabase('greenhouse.db')

def init_db() -> None:
    """
    Initialize the database and create tables.
    """
    db.connect()
    from iam.infrastructure.models import Device
    from edge.infrastructure.models import CropModel 

    # Añadir CropModel a la lista de tablas a crear
    db.create_tables([Device, CropModel], safe=True)
    db.close()