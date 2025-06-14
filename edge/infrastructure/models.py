from peewee import Model, CharField, AutoField
from shared.infrastructure.database import db

class CropModel(Model):
    """Modelo Peewee para persistir la información del cultivo."""
    id = AutoField() # Usamos un ID simple ya que solo guardaremos el último.
    crop_id = CharField()
    phase = CharField()

    class Meta:
        database = db
        table_name = 'current_crop'