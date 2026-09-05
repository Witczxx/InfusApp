from dataclasses import dataclass
from datetime import datetime

@dataclass
class Nurse:
    nurse_id: int
    nurse_name: str


@dataclass
class Patient:
    patient_id: int
    patient_name: str


@dataclass
class Medi:
    ingredient: str
    strength: str
    unit: int | float
    dosage_form: str
    carrier_fluid: str | None
    total_volume: int
    drops_per_min: int
    ml_per_hour: int
    start_time: datetime
    stop_time: datetime
