from .entities import SensorReading
from typing import Dict

class GreenhouseDomainService:
    """
    Contiene la lógica de negocio principal para el invernadero, evaluando las
    lecturas de los sensores contra los umbrales definidos para cada fase del cultivo.
    """

    # Umbrales para cada fase del cultivo, según lo especificado.
    THRESHOLDS = {
        "incubation": {"temp_max": 25, "humidity_max": 85, "co2_max": 800},
        "casing": {"temp_max": 23, "humidity_max": 90, "co2_max": 1000},
        "induction": {"temp_max": 21, "humidity_max": 95, "co2_max": 1200},
        "harvest": {"temp_max": 22, "humidity_max": 80, "co2_max": 1000}
    }

    def get_parameter_actions(self, phase: str, reading: SensorReading) -> Dict[str, str]:
        """
        Evalúa cada parámetro contra los umbrales de la fase actual y devuelve
        un diccionario con la acción correspondiente para cada uno.
        
        Args:
            phase (str): La fase actual del cultivo (ej. "incubation").
            reading (SensorReading): El objeto con las lecturas actuales de los sensores.

        Returns:
            dict: Un diccionario con la acción ('+' o '-') para cada parámetro.
                  Ej: {"temperature": "+", "humidity": "-", "co2": "-"}
        """
        actions = {
            "temperature": "-",
            "humidity": "-",
            "co2": "-"
        }
        reasons = []

        # Obtener los umbrales para la fase actual del diccionario.
        # El valor de 'phase' viene del objeto Crop, que es un string.
        current_thresholds = self.THRESHOLDS.get(phase)

        # Si la fase no tiene umbrales definidos, no se hace nada.
        if not current_thresholds:
            print(f"WARN: No se encontraron umbrales para la fase '{phase}'. No se tomará ninguna acción.")
            return actions

        # Comprobar cada parámetro contra su umbral máximo.
        if reading.temperature > current_thresholds["temp_max"]:
            actions["temperature"] = "+"
            reasons.append(f"Temperatura ({reading.temperature}°C) > {current_thresholds['temp_max']}°C")
        
        if reading.humidity > current_thresholds["humidity_max"]:
            actions["humidity"] = "+"
            reasons.append(f"Humedad ({reading.humidity}%) > {current_thresholds['humidity_max']}%")

        if reading.co2 > current_thresholds["co2_max"]:
            actions["co2"] = "+"
            reasons.append(f"CO2 ({reading.co2} ppm) > {current_thresholds['co2_max']} ppm")

        # Si hubo alguna razón para activar, se imprime un log informativo.
        if reasons:
            print(f"INFO: Razones para la activación en fase '{phase}': {', '.join(reasons)}")
            
        return actions