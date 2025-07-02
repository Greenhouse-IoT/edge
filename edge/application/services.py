from iam.infrastructure.repositories import DeviceRepository
from ..domain.entities import Crop, SensorReading
from ..domain.services import GreenhouseDomainService
from ..infrastructure.repositories import CropRepository
from ..infrastructure.clients import ExternalBackendClient, ServoControlClient

class CropManagementService:
    """Servicio de aplicación para gestionar la información del cultivo."""
    def __init__(self):
        self.repository = CropRepository()
        self.device_repository = DeviceRepository()

    def update_crop_info(self, crop_id: str, phase: str) -> Crop:
        crop = Crop(crop_id=crop_id, phase=phase)
        return self.repository.save(crop)

class SensorProcessingService:
    """Servicio de aplicación para procesar lecturas de sensores."""
    
    def __init__(self):
        self.crop_repo = CropRepository()
        self.domain_service = GreenhouseDomainService()
        self.backend_client = ExternalBackendClient()
        self.actuator_client = ServoControlClient()
        self.device_repository = DeviceRepository()

    def process_reading(self, device_id: str, api_key: str, reading: SensorReading) -> None:
        """
        Procesa una nueva lectura: valida, la envía al backend, ejecuta la lógica
        de negocio y envía el comando correspondiente al actuador.
        """
        """
        Valida el dispositivo y luego procesa la lectura del sensor.
        """
        if not self.device_repository.find_by_id_and_api_key(device_id, api_key):
            raise ValueError("Device not found")

        current_crop = self.crop_repo.get_current()
        if not current_crop:
            print("WARN: No hay un cultivo activo. Los datos se registrarán sin acciones.")
            return
            
        # 3. Enviar datos al backend externo (si es necesario)
        self.backend_client.post_sensor_reading(current_crop, reading)

        # 4. Ejecutar algoritmo de decisión para obtener acciones por parámetro
        actions = self.domain_service.get_parameter_actions(current_crop.phase, reading)
        
        # 5. Determinar si el servo debe activarse (si alguna acción es '+' o '-)
        should_activate_servo = any(action in ['+', '-'] for action in actions.values())

        # 6. Enviar comando (lecturas + acciones detalladas) al ESP32 del actuador
        self.actuator_client.send_command(reading, actions, should_activate_servo)