from  .repository import *
from  .modals import MetroCard
import math

def balance(mid  ,  balance ):
    metroCard[mid] = MetroCard(mid  ,int(balance) )



def rechargeCard(card  , ammount , src) :
    card.add_balance(ammount)
    station  = stations[src]
    x =  math.ceil(ammount*2/100)
    station.add_ammount(x)


def check_in(mid  ,  type  ,  src) :
    card = metroCard[mid]
    fare =  rates[type]
    station = stations[src]

    if (card.src == "AIRPORT" and src == "CENTRAL") or (card.src == "CENTRAL" and src == "AIRPORT") :
        fare =  fare/2
        station.add_discount(fare)

    if card.balance <  fare  :
        rechargeCard(card , fare - card.balance , src)

    card.add_balance(-1*fare)
    card.update_src(src)


    station.add_ammount(fare)
    station.add_passenger(type)


def summary():
    central = stations['CENTRAL']
    print(f"TOTAL_COLLECTION CENTRAL {int(central.total_ammount)} {int(central.discount)}")
    
    if central.passengerHistory:
        print("PASSENGER_TYPE_SUMMARY")
        for passenger_type in sorted(central.passengerHistory.keys()):
            count = central.passengerHistory[passenger_type]
            print(f"{passenger_type} {count}")
    
    airport = stations['AIRPORT']
    print(f"TOTAL_COLLECTION AIRPORT {int(airport.total_ammount)} {int(airport.discount)}")
    
    if airport.passengerHistory:
        print("PASSENGER_TYPE_SUMMARY")
        for passenger_type in sorted(airport.passengerHistory.keys()):
            count = airport.passengerHistory[passenger_type]
            print(f"{passenger_type} {count}")
