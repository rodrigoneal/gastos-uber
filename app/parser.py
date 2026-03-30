from app.schemas.riders_schema import UberTrip





def parse_to_schema(data: dict) -> list[UberTrip]:
    activities = data["data"]["activities"]["past"]["activities"]

    trips = []

    for act in activities:
        trip = UberTrip(
            id=act["uuid"],
            data=act["subtitle"],
            valor=act["description"],  # deixa o validator resolver
            status=act["description"], # mesma coisa
            endereco=act["title"],
            url=act["cardURL"],
        )
        trips.append(trip)

    return trips