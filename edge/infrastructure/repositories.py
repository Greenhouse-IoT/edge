from typing import Optional
from ..domain.entities import Crop
from .models import CropModel

class CropRepository:
    """Repositorio para gestionar la persistencia de la info del cultivo."""

    def save(self, crop: Crop) -> Crop:
        """
        Guarda o actualiza la información del cultivo.
        Siempre habrá una única fila en la tabla.
        """
        # Elimina el registro anterior para guardar solo el más reciente.
        CropModel.delete().execute()
        model = CropModel.create(crop_id=crop.crop_id, phase=crop.phase)
        return Crop(crop_id=model.crop_id, phase=model.phase)

    def get_current(self) -> Optional[Crop]:
        """Obtiene la información del cultivo actual."""
        try:
            model = CropModel.select().order_by(CropModel.id.desc()).get()
            return Crop(crop_id=model.crop_id, phase=model.phase)
        except CropModel.DoesNotExist:
            return None