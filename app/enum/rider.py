from enum import StrEnum


class RiderStatus(StrEnum):
    CANCELADA = "cancelada"
    NAO_CONCLUIDO = "nao_concluido"
    CONCLUIDO = "concluido"