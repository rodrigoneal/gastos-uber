def safe_float_zero(value):
    return float(value) if value is not None else 0.0


def trip_to_dict(trip):
    receipt = trip.receipt_detail

    return {
        "id": trip.id,
        "status": trip.status.value,
        "inicio": trip.inicio,
        "fim": trip.fim,
        "motorista": trip.motorista,
        "valor": float(trip.valor),
        "origem": trip.origem,
        "destino": trip.destino,
        "distancia_km": safe_float_zero(trip.distancia_km),
        "duracao_min": trip.duracao_min,
        "tipo_veiculo": trip.tipo_veiculo.value if trip.tipo_veiculo else None,
        # receipt seguro
        "total": safe_float_zero(receipt.total) if receipt else None,
        "preco_viagem": safe_float_zero(receipt.preco_viagem) if receipt else None,
        "taxa_intermediacao": safe_float_zero(receipt.taxa_intermediacao)
        if receipt
        else None,
        "custo_fixo": safe_float_zero(receipt.custo_fixo) if receipt else None,
        "tempo_espera": safe_float_zero(receipt.tempo_espera) if receipt else None,
        # aqui já resolve também
        "creditos_uber_one": safe_float_zero(receipt.creditos_uber_one) if receipt else 0,
        "pagamento": receipt.pagamento if receipt else None,
    }