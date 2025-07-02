from .entities import SensorReading
from typing import Dict

class GreenhouseDomainService:
    """
    Contiene la lógica de negocio principal para el invernadero, evaluando las
    lecturas de los sensores contra los umbrales definidos para cada fase del cultivo.
    """

    # Umbrales para cada fase del cultivo, con valores mínimos y máximos.
    THRESHOLDS = {
        "incubation": {
            "temp_min": 21, "temp_max": 27,
            "humidity_min": 80, "humidity_max": 95,
            "co2_min": 5000, "co2_max": 10000
        },
        "casing": {
            "temp_min": 21, "temp_max": 27,
            "humidity_min": 80, "humidity_max": 95,
            "co2_min": 5000, "co2_max": 10000
        },
        "induction": {
            "temp_min": 15, "temp_max": 21,
            "humidity_min": 80, "humidity_max": 95,
            "co2_min": 800, "co2_max": 1200
        },
        "harvest": {
            "temp_min": 16, "temp_max": 22,
            "humidity_min": 80, "humidity_max": 95,
            "co2_min": 800, "co2_max": 1100
        }
    }

    def get_parameter_actions(self, phase: str, reading: SensorReading) -> Dict[str, str]:
        """
        Evalúa cada parámetro contra los umbrales de la fase actual y devuelve
        un diccionario con la acción correspondiente para cada uno.
        
        Args:
            phase (str): La fase actual del cultivo (ej. "incubation").
            reading (SensorReading): El objeto con las lecturas actuales de los sensores.

        Returns:
            dict: Un diccionario con la acción ('+', '-', o '=') para cada parámetro.
                  '+' = por debajo del mínimo, '-' = por encima del máximo, '=' = dentro del rango
                  Ej: {"temperature": "+", "humidity": "=", "co2": "-"}
        """
        actions = {
            "temperature": "=",
            "humidity": "=",
            "co2": "="
        }
        reasons = []

        # Obtener los umbrales para la fase actual del diccionario.
        # El valor de 'phase' viene del objeto Crop, que es un string.
        current_thresholds = self.THRESHOLDS.get(phase)

        # Si la fase no tiene umbrales definidos, no se hace nada.
        if not current_thresholds:
            print(f"WARN: No se encontraron umbrales para la fase '{phase}'. No se tomará ninguna acción.")
            return actions

        # Evaluar temperatura
        if reading.temperature < current_thresholds["temp_min"]:
            actions["temperature"] = "+"
            reasons.append(f"Temperatura ({reading.temperature}°C) < {current_thresholds['temp_min']}°C (mínimo)")
        elif reading.temperature > current_thresholds["temp_max"]:
            actions["temperature"] = "-"
            reasons.append(f"Temperatura ({reading.temperature}°C) > {current_thresholds['temp_max']}°C (máximo)")
        else:
            reasons.append(f"Temperatura ({reading.temperature}°C) dentro del rango [{current_thresholds['temp_min']}-{current_thresholds['temp_max']}°C]")

        # Evaluar humedad
        if reading.humidity < current_thresholds["humidity_min"]:
            actions["humidity"] = "+"
            reasons.append(f"Humedad ({reading.humidity}%) < {current_thresholds['humidity_min']}% (mínimo)")
        elif reading.humidity > current_thresholds["humidity_max"]:
            actions["humidity"] = "-"
            reasons.append(f"Humedad ({reading.humidity}%) > {current_thresholds['humidity_max']}% (máximo)")
        else:
            reasons.append(f"Humedad ({reading.humidity}%) dentro del rango [{current_thresholds['humidity_min']}-{current_thresholds['humidity_max']}%]")

        # Evaluar CO2
        if reading.co2 < current_thresholds["co2_min"]:
            actions["co2"] = "+"
            reasons.append(f"CO2 ({reading.co2} ppm) < {current_thresholds['co2_min']} ppm (mínimo)")
        elif reading.co2 > current_thresholds["co2_max"]:
            actions["co2"] = "-"
            reasons.append(f"CO2 ({reading.co2} ppm) > {current_thresholds['co2_max']} ppm (máximo)")
        else:
            reasons.append(f"CO2 ({reading.co2} ppm) dentro del rango [{current_thresholds['co2_min']}-{current_thresholds['co2_max']} ppm]")

        # Log informativo con todas las evaluaciones
        print(f"INFO: Evaluación para la fase '{phase}': {', '.join(reasons)}")
            
        return actions