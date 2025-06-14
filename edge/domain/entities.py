from dataclasses import dataclass

@dataclass
class Crop:
    """Entidad que representa la información del cultivo actual."""
    crop_id: str
    phase: str # Fases: incubation, casing, induction, harvest

@dataclass
class SensorReading:
    """Entidad que representa las lecturas de los sensores."""
    temperature: float
    humidity: float
    co2: int