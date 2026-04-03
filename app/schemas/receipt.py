from decimal import Decimal

from pydantic import BaseModel


class ReceiptBreakdown(BaseModel):
    total: Decimal | None
    preco_viagem: Decimal | None
    taxa_intermediacao: Decimal | None
    custo_fixo: Decimal | None
    tempo_espera: Decimal | None
    creditos_uber_one: Decimal | None
    pagamento: str | None