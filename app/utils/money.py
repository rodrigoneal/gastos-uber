from decimal import Decimal


def parse_money(value: str) -> Decimal:
    value = value.replace("\xa0", "").replace("R$", "").strip()
    value = value.replace(".", "").replace(",", ".")
    return Decimal(value)