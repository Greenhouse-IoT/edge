import requests
import os # Importar el módulo os para acceder a variables de entorno
from typing import Dict
from ..domain.entities import Crop, SensorReading

class ExternalBackendClient:
    """Cliente para comunicarse con el backend de Greenhouse."""

    # Se obtienen las variables de entorno para API_URL y STATIC_JWT_TOKEN
    # Si las variables no están definidas, se usará un valor predeterminado (o None si no se especifica)
    # En un entorno de producción, se recomienda que estas variables sean obligatorias.
    API_URL = os.environ.get("API_URL")
    STATIC_JWT_TOKEN = os.environ.get(
        "STATIC_JWT_TOKEN"
    )

    def post_sensor_reading(self, crop: Crop, reading: SensorReading):
        headers = {
            "Authorization": f"Bearer {self.STATIC_JWT_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "author": "esp32-edge-service",
            "phase": crop.phase,
            "payload": {
                "data": [
                    {"name": "Air Temperature", "value": str(reading.temperature)},
                    {"name": "Air Humidity", "value": str(reading.humidity)},
                    {"name": "Carbon Dioxide", "value": str(reading.co2)}
                ]
            },
            "cropId": crop.crop_id
        }
        try:
            print(f"INFO: Enviando datos al backend externo: {payload}")
            response = requests.post(self.API_URL, headers=headers, json=payload, timeout=10)
            response.raise_for_status() # Lanza una excepción para errores HTTP 4xx/5xx
            print(f"INFO: Datos enviados al backend externo con éxito. Status: {response.status_code}")
        except requests.RequestException as e:
            print(f"ERROR: No se pudo enviar la información al backend externo. Error: {e}")

## Clientes de Actuadores y Servo

class ServoControlClient:
    """Cliente para controlar el ESP32 del actuador (servo y LCD)."""

    # Se obtiene la variable de entorno para SERVO_ESP32_IP
    SERVO_ESP32_URL = os.environ.get("SERVO_ESP32_IP")

    def send_command(self, reading: SensorReading, actions: Dict[str, str], activate_servo: bool):
        """
        Construye el payload JSON y lo envía al ESP32 del actuador.

        Args:
            reading (SensorReading): Objeto con las lecturas actuales.
            actions (dict): Diccionario con la acción para cada parámetro.
            activate_servo (bool): Indicador general para mover el servo.
        """

        # El payload contiene una acción general para el servo y acciones
        # específicas para cada parámetro que se mostrarán en el LCD.
        payload = {
            "servo_action": "+" if activate_servo else "-",
            "temperature": reading.temperature,
            "temp_action": actions.get("temperature", "-"),
            "humidity": reading.humidity,
            "hum_action": actions.get("humidity", "-"),
            "co2": reading.co2,
            "co2_action": actions.get("co2", "-")
        }

        try:
            response = requests.post(self.SERVO_ESP32_URL, json=payload, timeout=5)
            if response.status_code == 200:
                print(f"INFO: Comando enviado al actuador ESP32 con éxito. Payload: {payload}")
            else:
                print(f"WARN: El actuador ESP32 respondió con status: {response.status_code}, Body: {response.text}")
        except requests.RequestException as e:
            print(f"ERROR: No se pudo comunicar con el ESP32 del actuador en {self.SERVO_ESP32_URL}. Error: {e}")

# Si este es un cliente para un SEGUNDO servo ESP32 y no el mismo que ServoControlClient,
# entonces la clase es relevante. Si es el mismo, puedes eliminarla para evitar duplicados.
class SecondServoControlClient: # He renombrado la clase para mayor claridad si son dos ESP32 distintos
    """Cliente para controlar el servo en el segundo ESP32."""
    # La IP debe ser estática o descubrible (ej. mDNS)
    SERVO_ESP32_URL = os.environ.get("SERVO_ESP32_IP") # También usar variable de entorno aquí

    def activate(self):
        """Envía una señal para activar el servo."""
        try:
            response = requests.post(self.SERVO_ESP32_URL, timeout=5)
            if response.status_code == 200:
                print("INFO: Señal de activación enviada al servo ESP32 con éxito.")
            else:
                print(f"WARN: El servo ESP32 respondió con status: {response.status_code}")
        except requests.RequestException as e:
            print(f"ERROR: No se pudo comunicar con el ESP32 del servo. Error: {e}")