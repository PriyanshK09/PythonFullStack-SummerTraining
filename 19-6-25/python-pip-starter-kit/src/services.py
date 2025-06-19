from  .repository import *
from  .modals import MetroCard

def balance(mid  ,  balance ):
    metroCard[mid] = MetroCard(mid  ,int(balance) )



def rechargeCard(card  , ammount , src) :
    card.add_balance(ammount)
    station  = stations[src]
    x =  ammount*2/100
    station.add_ammount(x)


def check_in(mid  ,  type  ,  src) :
    card = metroCard[mid]
    fare =  rates[type]
    station = stations[src]
    round_trip  =  False
    if (card.src == "AIRPORT" and src == "CENTRAL") or (card.src == "CENTRAL" and src == "AIRPORT") :
        fare =  fare/2
        station.add_discount(fare)
        round_trip =  True

    if card.balance <  fare  :
        rechargeCard(card , fare - card.balance , src)

    card.add_balance(-1*fare)
    if round_trip :
        card.update_src(None)
    else  :
        card.update_src(src)


    station.add_ammount(fare)
    station.add_passenger(type)


def summary():
    for station_name in ['CENTRAL', 'AIRPORT']:
        station = stations[station_name]

        print(f"TOTAL_COLLECTION {station_name} {int(station.total_ammount)}  {int(station.discount)}")
        print("PASSENGER_TYPE_SUMMARY")


        for passenger_type, count in sorted(station.passengerHistory.items()):
            print(f"{passenger_type} {count}")


