import unittest
from src.models import MetroCard, Station

class TestMetroCard(unittest.TestCase):
    
    def test_metro_card_initialization(self):
        card = MetroCard("MC001", 100)
        self.assertEqual(card.id, "MC001")
        self.assertEqual(card.balance, 100)
        self.assertIsNone(card.src)
    
    def test_add_positive_balance(self):
        card = MetroCard("MC001", 100)
        card.add_balance(50)
        self.assertEqual(card.balance, 150)
    
    def test_add_negative_balance(self):
        card = MetroCard("MC001", 100)
        card.add_balance(-30)
        self.assertEqual(card.balance, 70)
    
    def test_add_zero_balance(self):
        card = MetroCard("MC001", 100)
        card.add_balance(0)
        self.assertEqual(card.balance, 100)
    
    def test_update_src_to_station(self):
        card = MetroCard("MC001", 100)
        card.update_src("CENTRAL")
        self.assertEqual(card.src, "CENTRAL")
    
    def test_update_src_to_none(self):
        card = MetroCard("MC001", 100)
        card.update_src("CENTRAL")
        card.update_src(None)
        self.assertIsNone(card.src)

class TestStation(unittest.TestCase):
    
    def test_station_initialization(self):
        station = Station("CENTRAL")
        self.assertEqual(station.name, "CENTRAL")
        self.assertEqual(station.total_amount, 0)
        self.assertEqual(station.discount, 0)
        self.assertEqual(len(station.passenger_history), 0)
    
    def test_add_amount(self):
        station = Station("CENTRAL")
        station.add_amount(100)
        self.assertEqual(station.total_amount, 100)
    
    def test_add_multiple_amounts(self):
        station = Station("CENTRAL")
        station.add_amount(100)
        station.add_amount(50)
        self.assertEqual(station.total_amount, 150)
    
    def test_add_discount(self):
        station = Station("CENTRAL")
        station.add_discount(25)
        self.assertEqual(station.discount, 25)
    
    def test_add_multiple_discounts(self):
        station = Station("CENTRAL")
        station.add_discount(25)
        station.add_discount(10)
        self.assertEqual(station.discount, 35)
    
    def test_add_passenger_single_type(self):
        station = Station("CENTRAL")
        station.add_passenger("ADULT")
        self.assertEqual(station.passenger_history["ADULT"], 1)
    
    def test_add_passenger_multiple_same_type(self):
        station = Station("CENTRAL")
        station.add_passenger("ADULT")
        station.add_passenger("ADULT")
        self.assertEqual(station.passenger_history["ADULT"], 2)
    
    def test_add_passenger_different_types(self):
        station = Station("CENTRAL")
        station.add_passenger("ADULT")
        station.add_passenger("KID")
        station.add_passenger("SENIOR_CITIZEN")
        self.assertEqual(station.passenger_history["ADULT"], 1)
        self.assertEqual(station.passenger_history["KID"], 1)
        self.assertEqual(station.passenger_history["SENIOR_CITIZEN"], 1)
    
    def test_passenger_history_default_value(self):
        station = Station("CENTRAL")
        self.assertEqual(station.passenger_history["NONEXISTENT"], 0)

if __name__ == '__main__':
    unittest.main()