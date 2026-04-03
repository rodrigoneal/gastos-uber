from datetime import datetime
import json
from time import sleep

from app.logging import logger

import httpx

from app.parser import parse_to_schema
from app.parsers.receipt_parser import extrair_receipt
from app.schemas.receipt import ReceiptBreakdown
from app.schemas.riders_schema import UberTrip
from app.schemas.trip_schema import Trip


QUERY = "query Activities($cityID: Int, $endTimeMs: Float, $includePast: Boolean = true, $includeUpcoming: Boolean = true, $limit: Int = 5, $nextPageToken: String, $orderTypes: [RVWebCommonActivityOrderType!] = [RIDES, TRAVEL], $profileType: RVWebCommonActivityProfileType = PERSONAL, $startTimeMs: Float) {\n  activities(cityID: $cityID) {\n    cityID\n    past(\n      endTimeMs: $endTimeMs\n      limit: $limit\n      nextPageToken: $nextPageToken\n      orderTypes: $orderTypes\n      profileType: $profileType\n      startTimeMs: $startTimeMs\n    ) @include(if: $includePast) {\n      activities {\n        ...RVWebCommonActivityFragment\n        __typename\n      }\n      nextPageToken\n      __typename\n    }\n    upcoming @include(if: $includeUpcoming) {\n      activities {\n        ...RVWebCommonActivityFragment\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment RVWebCommonActivityFragment on RVWebCommonActivity {\n  buttons {\n    isDefault\n    startEnhancerIcon\n    text\n    url\n    __typename\n  }\n  cardURL\n  description\n  imageURL {\n    light\n    dark\n    __typename\n  }\n  subtitle\n  title\n  uuid\n  __typename\n}\n"

TRIP_QUERY = "query GetTrip($tripUUID: String!) {\n  getTrip(tripUUID: $tripUUID) {\n    trip {\n      beginTripTime\n      cityID\n      countryID\n      disableCanceling\n      disableRating\n      disableResendReceipt\n      driver\n      dropoffTime\n      fare\n      guest\n      isRidepoolTrip\n      isScheduledRide\n      isSurgeTrip\n      isUberReserve\n      jobUUID\n      marketplace\n      paymentProfileUUID\n      showRating\n      status\n      uuid\n      vehicleDisplayName\n      vehicleViewID\n      waypoints\n      __typename\n    }\n    mapURL\n    polandTaxiLicense\n    rating\n    reviewer\n    receipt {\n      carYear\n      distance\n      distanceLabel\n      duration\n      vehicleType\n      __typename\n    }\n    concierge {\n      sourceType\n      __typename\n    }\n    organization {\n      name\n      __typename\n    }\n    __typename\n  }\n}\n"


RECEPT_QUERY = "query GetReceipt($tripUUID: String!, $timestamp: String) {\n  getReceipt(tripUUID: $tripUUID, timestamp: $timestamp) {\n    actionList {\n      type\n      helpNodeUUID\n      __typename\n    }\n    receiptData\n    receiptsForJob {\n      timestamp\n      type\n      eventUUID\n      __typename\n    }\n    __typename\n  }\n}\n"


class UberClient:
    def __init__(self):
        with open("data/session.json", "r") as f:
            self.session = json.load(f)
        self.client = httpx.Client(
            headers=self.session["headers"],
            cookies=self.session["cookies"],
        )
        self.url = "https://riders.uber.com/graphql"
        self.next_token = None

    def build_variables_trip(self, trip_id=str):
        return {
            "tripUUID": trip_id,
        }

    def build_variables_activities(
        self,
        limit=10,
        next_token=None,
        mes: int = None,
        ano: int = None,
        include_upcoming=True,
    ):
        variables = {
            "includePast": True,
            "includeUpcoming": include_upcoming,
            "limit": limit,
            "orderTypes": ["RIDES", "TRAVEL"],
            "profileType": "PERSONAL",
        }
        variables["limit"] = limit
        if mes and ano:
            start, end = self.__mes_para_range(ano, mes)
            variables["startTimeMs"] = start
            variables["endTimeMs"] = end
            variables["limit"] = 1000
        if next_token:
            variables["nextPageToken"] = next_token
        variables["includeUpcoming"] = include_upcoming
        return variables

    def _get_next_token(self, data: dict) -> str | None:
        return data["data"]["activities"]["past"]["nextPageToken"]

    def __mes_para_range(self, ano: int, mes: int):
        inicio = datetime(ano, mes, 1)

        if mes == 12:
            fim = datetime(ano + 1, 1, 1)
        else:
            fim = datetime(ano, mes + 1, 1)

        return (
            int(inicio.timestamp() * 1000),
            int(fim.timestamp() * 1000) - 1,
        )

    def get_activities(self, limit=10, mes: int = None, ano: int = None):
        logger.info("Buscando atividades")
        variables = self.build_variables_activities(
            limit=limit, include_upcoming=True, mes=mes, ano=ano
        )
        payload = {"variables": variables}
        payload["query"] = QUERY
        payload["operationName"] = "Activities"
        response = self.client.post(self.url, json=payload)
        response.raise_for_status()
        data = response.json()
        self.next_token = self._get_next_token(data)
        return parse_to_schema(data)

    def get_trip(self, trip_id: str | UberTrip, receipt_detail=True):
        if isinstance(trip_id, UberTrip):
            trip_id = trip_id.id
        logger.info(f"Buscando viagem {trip_id}")
        payload = {
            "operationName": "GetTrip",
            "query": TRIP_QUERY,
            "variables": {"tripUUID": trip_id},
        }
        response = self.client.post(self.url, json=payload)
        response.raise_for_status()
        receipt = None
        if receipt_detail:
            sleep(.5)
            receipt = self.get_receipt(trip_id)
        data = response.json()
        return Trip.from_raw(data, receipt_detail=receipt)

    def get_receipt(self, trip_id: str | UberTrip):
        if isinstance(trip_id, UberTrip):
            trip_id = trip_id.id
        logger.info(f"Buscando recibo {trip_id}")
        payload = {
            "operationName": "GetReceipt",
            "query": RECEPT_QUERY,
            "variables": {"tripUUID": trip_id, "timestamp": ""},
        }
        response = self.client.post(self.url, json=payload)
        response.raise_for_status()
        data = response.json()
        try:
            raw = extrair_receipt(html=data["data"]["getReceipt"]["receiptData"])
        except TypeError:
            return None
        return ReceiptBreakdown(**raw)

