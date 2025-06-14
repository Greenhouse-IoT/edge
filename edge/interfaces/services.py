from flask import Blueprint, request, jsonify
from ..application.services import CropManagementService, SensorProcessingService
from ..domain.entities import SensorReading
from iam.interfaces.services import authenticate_request

greenhouse_api = Blueprint("greenhouse_api", __name__)

# Inicializar servicios de aplicación
crop_service = CropManagementService()
processing_service = SensorProcessingService()

@greenhouse_api.route("/api/v1/greenhouse/crop-info", methods=["POST"])
def set_crop_info():
    """
    Endpoint para recibir y persistir el cropId y la phase.
    """
    data = request.json
    try:
        crop_id = data["cropId"]
        phase = data["phase"]
        crop = crop_service.update_crop_info(crop_id, phase)
        return jsonify({"message": "Crop info updated", "cropId": crop.crop_id, "phase": crop.phase}), 200
    except KeyError:
        return jsonify({"error": "Faltan los campos 'cropId' o 'phase'"}), 400

@greenhouse_api.route("/api/v1/greenhouse/sensor-readings", methods=["POST"])
def receive_sensor_readings():
    """
    Endpoint para recibir datos de los sensores del ESP32, previa autenticación.
    """
    auth_result = authenticate_request()
    if auth_result:
        return auth_result

    data = request.json
    try:
        device_id = data["device_id"]
        api_key = request.headers.get("X-API-Key")
        
        reading = SensorReading(
            temperature=float(data["temperature"]),
            humidity=float(data["humidity"]),
            co2=int(data["co2"])
        )
        
        processing_service.process_reading(device_id, api_key, reading)
        return jsonify({"message": "Lectura procesada con éxito"}), 200
    except KeyError:
        return jsonify({"error": "Faltan datos: 'device_id', 'temperature', 'humidity', o 'co2'"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500
