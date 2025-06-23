from src.models import MetroCard
from src.repository import Repository

class MetroService:
    def __init__(self):
        self.__repository = Repository()

    def create_balance(self, card_id, balance):
        card = MetroCard(card_id, int(balance))
        self.__repository.save_card(card)

    def check_in(self, card_id, passenger_type, source):
        card = self.__repository.get_card(card_id)
        base_fare = self.__repository.get_rate(passenger_type)
        
        is_return_trip = self.__is_return_trip(card, source)
        fare = self.__calculate_fare(base_fare, is_return_trip)
        
        if card.balance < fare:
            recharge_amount = fare - card.balance
            self.__recharge_card(card, recharge_amount, source)
        
        card.add_balance(-fare)
        
        station = self.__repository.get_station(source)
        station.add_amount(fare)
        station.add_passenger(passenger_type)
        
        if is_return_trip:
            discount_amount = base_fare - fare
            station.add_discount(discount_amount)
            card.update_src(None)
        else:
            card.update_src(source)

    def __is_return_trip(self, card, source):
        if card.src is None:
            return False
        return ((card.src == "AIRPORT" and source == "CENTRAL") or 
                (card.src == "CENTRAL" and source == "AIRPORT"))

    def __calculate_fare(self, base_fare, is_return_trip):
        if is_return_trip:
            return base_fare // 2
        return base_fare

    def __recharge_card(self, card, amount, source):
        card.add_balance(amount)
        station = self.__repository.get_station(source)
        service_fee = (amount * 2) // 100
        station.add_amount(service_fee)

    def generate_summary(self):
        all_stations = self.__repository.get_all_stations()
        
        for station_name in ['CENTRAL', 'AIRPORT']:
            station = all_stations[station_name]
            print(f"TOTAL_COLLECTION {station_name} {int(station.total_amount)} {int(station.discount)}")
            print("PASSENGER_TYPE_SUMMARY")
            
            for passenger_type, count in sorted(station.passenger_history.items()):
                print(f"{passenger_type} {count}")
