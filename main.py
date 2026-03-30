from time import sleep

import pandas as pd

from app.logging import logger

from app.client.uber_client import UberClient
from app.parsers.dict_parser import trip_to_dict


uber_client = UberClient()

riders = uber_client.get_activities(ano=2026, mes=3)


trips = []

count = 0
for rider in riders:
    logger.info(f"Buscando viagem: {count} de {len(riders)}")
    trip = uber_client.get_trip(trip_id=rider)
    trips.append(trip)
    sleep(1)
    count += 1
df = pd.DataFrame(trip_to_dict(trip) for trip in trips)


df.to_excel("data/uber.xlsx")

df = df[df["status"] == "COMPLETED"]
felipe = df[df["pagamento"].str.contains("Felipe")]

academia = df[df["origem"].str.contains("Irajá") | df["destino"].str.contains("Irajá")]




felipe.to_excel("data/felipe.xlsx")
academia.to_excel("data/academia.xlsx")