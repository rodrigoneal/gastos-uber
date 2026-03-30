from bs4 import BeautifulSoup

from app.schemas.trip_schema import parse_money





def extrair_receipt(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    result = {
        "total": None,
        "preco_viagem": None,
        "taxa_intermediacao": None,
        "custo_fixo": None,
        "tempo_espera": None,
        "creditos_uber_one": None,
        "pagamento": None,
    }

    # -------------------------
    # TOTAL
    # -------------------------
    total = soup.select_one('[data-testid="total_fare_amount"]')
    if total:
        result["total"] = parse_money(total.text)

    # -------------------------
    # ITENS DO FARE
    # -------------------------
    items = soup.select(".fare-breakdown-item")

    for item in items:
        label_el = item.select_one(".fare-breakdown-name")
        value_el = item.select_one(".fare-breakdown-amount")

        if not label_el or not value_el:
            continue

        label = label_el.text.strip().lower()
        value = value_el.text.strip()

        money = parse_money(value.replace("-", ""))

        if "preço da viagem" in label:
            result["preco_viagem"] = money

        elif "taxa de intermediação" in label:
            result["taxa_intermediacao"] = money

        elif "custo fixo" in label:
            result["custo_fixo"] = money

        elif "tempo de espera" in label:
            result["tempo_espera"] = money

        elif "uber one" in label:
            # pode ser negativo
            if "-" in value:
                money = -money
            result["creditos_uber_one"] = money

    # -------------------------
    # PAGAMENTO
    # -------------------------
    payment = soup.select_one(".payment-card-title")
    if payment:
        
        result["pagamento"] = payment.text.strip().replace(" ••••", " ").strip()

    return result