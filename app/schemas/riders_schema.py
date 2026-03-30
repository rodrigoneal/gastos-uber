from datetime import datetime
from typing import Annotated

from pydantic import AfterValidator, BaseModel, field_validator
from decimal import Decimal
import re

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
    # "27 de mar. • 19:11"
    parte_data, parte_hora = data_str.split(" • ")

    dia, _, mes_str = parte_data.split(" ")
    mes_str = mes_str.replace(".", "")

    hora, minuto = parte_hora.split(":")

    ano = datetime.now().year  # assume ano atual

    return datetime(
        year=ano,
        month=MESES[mes_str],
        day=int(dia),
        hour=int(hora),
        minute=int(minuto),
    )


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
            match = re.search(r"R\$(\d+,\d+)", v)
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
