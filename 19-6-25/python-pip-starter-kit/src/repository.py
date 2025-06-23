from src.models import Station

class Repository:
    def __init__(self):
        self.__metro_cards = {}
        self.__rates = {
            "ADULT": 200,
            "SENIOR_CITIZEN": 100,
            "KID": 50
        }
        self.__stations = {
            "CENTRAL": Station("CENTRAL"),
            "AIRPORT": Station("AIRPORT")
        }

    def get_card(self, card_id):
        return self.__metro_cards.get(card_id)

    def save_card(self, card):
        self.__metro_cards[card.id] = card

    def get_station(self, station_name):
        return self.__stations.get(station_name)

    def get_rate(self, passenger_type):
        return self.__rates.get(passenger_type)

    def get_all_stations(self):
        return self.__stations