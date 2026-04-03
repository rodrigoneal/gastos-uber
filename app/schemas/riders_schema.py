from datetime import datetime
from typing import Annotated

from pydantic import AfterValidator, BaseModel, field_validator
from decimal import Decimal
import re

from dateutil.parser import parse as parse_date

from app.enum.rider import RiderStatus


MESES = {
    "jan": 1,
    "fev": 2,
    "mar": 3,
    "abr": 4,
    "mai": 5,
    "jun": 6,
    "jul": 7,
    "ago": 8,
    "set": 9,
    "out": 10,
    "nov": 11,
    "dez": 12,
}


def parse_data_uber(data_str: str) -> datetime:
    data_str = data_str.replace("•", "").strip()
    return parse_date(data_str)


class UberTrip(BaseModel):
    id: str
    data: datetime
    valor: Decimal
    status: str
    endereco: str
    url: str

    @field_validator("valor", mode="before")
    @classmethod
    def parse_valor(cls, v):
        if isinstance(v, str):
            match = re.search(r"R\$(\d+.\d+)", v)
            if match:
                return Decimal(match.group(1).replace(",", "."))
        return v

    @field_validator("data", mode="before")
    @classmethod
    def parse_data(cls, v):
        if isinstance(v, str):
            return parse_data_uber(v)
        return v

    @field_validator("status", mode="before")
    @classmethod
    def parse_status(cls, v, values):
        description = values.data.get("valor") or values.data.get("description")

        if isinstance(description, str):
            if "Cancelada" in description:
                return RiderStatus.CANCELADA
            elif "Não concluído" in description:
                return RiderStatus.NAO_CONCLUIDO

        return RiderStatus.CONCLUIDO
