from enum import Enum


class TripStatus(str, Enum):
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    UNFULFILLED = "UNFULFILLED"  # não concluída
    UNKNOWN = "UNKNOWN"

    @classmethod
    def from_raw(cls, value: str):
        if not value:
            return cls.UNKNOWN

        try:
            return cls(value)
        except ValueError:
            return cls.UNKNOWN

class VehicleType(str, Enum):
    UBERX = "UberX"
    COMFORT = "Comfort"
    BLACK = "Black"
    POOL = "Pool"
    MOTO = "Moto"
    FLASH = "Flash"
    UNKNOWN = "Unknown"

    @classmethod
    def from_raw(cls, value: str):
        if not value:
            return cls.UNKNOWN

        # normaliza (caso venha zoado)
        value = value.strip()

        for item in cls:
            if item.value.lower() == value.lower():
                return item

        return cls.UNKNOWN