from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from app.enum.trip import TripStatus, VehicleType
from app.schemas.receipt import ReceiptBreakdown


# -------------------------
# Helpers
# -------------------------


def parse_datetime_uber(dt: str) -> datetime:
    # "Fri Mar 27 2026 22:21:17 GMT+0000 (Coordinated Universal Time)"
    return datetime.strptime(dt.split(" GMT")[0], "%a %b %d %Y %H:%M:%S")


def parse_money(value: str) -> Decimal:
    # "R$ 20,00"
    value = value.replace("\xa0", "").replace("R$", "").strip()
    return Decimal(value.replace(",", "."))


# -------------------------
# Sub-models
# -------------------------


class Receipt(BaseModel):
    distance_km: Decimal | None
    duration_minutes: int | None
    vehicle_type: str | None

    @classmethod
    def from_raw(cls, data: dict):
        return cls(
                distance_km=Decimal(data["distance"]) if data["distance"] else None,
                duration_minutes=int(data["duration"].split()[0]) if data["duration"] else None,
                vehicle_type=data["vehicleType"] if data["vehicleType"] else None,
            )


class Trip(BaseModel):
    id: str
    status: TripStatus

    inicio: datetime 
    fim: datetime | None

    motorista: str | None
    valor: Decimal | None

    origem: str
    destino: str

    distancia_km: Optional[Decimal] = None
    duracao_min: Optional[int] = None
    tipo_veiculo: Optional[VehicleType] = None
    receipt_detail: Optional[ReceiptBreakdown] = None

    @classmethod
    def from_raw(cls, data: dict, receipt_detail: ReceiptBreakdown | None = None):
        trip = data["data"]["getTrip"]["trip"]
        receipt = data["data"]["getTrip"].get("receipt")

        receipt_parsed = Receipt.from_raw(receipt) if receipt else None
        try:
            return cls(
                id=trip["uuid"],
                status=TripStatus.from_raw(trip["status"]),
                inicio=parse_datetime_uber(trip["beginTripTime"]),
                fim=parse_datetime_uber(trip["dropoffTime"]) if trip["dropoffTime"] else None,
                motorista=trip["driver"] if trip["driver"] else None,
                valor=parse_money(trip["fare"]) if trip["fare"] else None,
                origem=trip["waypoints"][0],
                destino=trip["waypoints"][-1],
                distancia_km=receipt_parsed.distance_km if receipt_parsed else None,
                duracao_min=receipt_parsed.duration_minutes if receipt_parsed else None,
                tipo_veiculo=VehicleType.from_raw(
                    receipt_parsed.vehicle_type if receipt_parsed else None
                ),
                receipt_detail=receipt_detail,
            )
        except ValueError:
            breakpoint()
