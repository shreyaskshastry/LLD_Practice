from typing import *

class Vehicle:
    def __init__(self,vehicle_type : str, vehicle_registration : str, vehicle_color : str) -> None:
        self.vehicle_type = vehicle_type
        self.vehicle_registration = vehicle_registration
        self.vehicle_color = vehicle_color
    
    def get_vehicle_registration(self) -> str:
        return self.vehicle_registration
    
    def get_vehicle_color(self) -> str:
        return self.vehicle_color

class ParkingLot:
    def __init__(self,parking_lot_id : int, number_of_floors : int, number_of_slots_per_floor : int) -> None:
        if number_of_slots_per_floor < 4:
            print("Not possible to Construct this floor minimum 4 slots needed")
            return
        self.parking_lot_id = parking_lot_id
        self.number_of_floors = number_of_floors
        self.number_of_slots_per_floor = number_of_slots_per_floor
        self.floors = [self.add_Floor(self.number_of_slots_per_floor) for _ in range(self.number_of_floors)]

        print(f"Created parking lot with {self.number_of_floors} floors and {self.number_of_slots_per_floor} slots per floor")

    def add_Floor(self,number_of_slots : int) -> List:
        slot_map = [None for i in range(number_of_slots)]
        return slot_map
    
    def park_vehicle(self,vehicle_type : str, vehicle_registration : str, vehicle_color : str):
        vehicle = Vehicle(vehicle_type,vehicle_registration,vehicle_color)
        for floor_ind in range(len(self.floors)):
            floor = self.floors[floor_ind]
            if vehicle_type == "TRUCK" and (floor[0] == None):
                ticket = Ticket(self.parking_lot_id,floor_ind + 1, 1)
                self.floors[floor_ind][0] = {'ticket_id' : ticket.get_ticket_id(),'vehicle' : vehicle}
                print(f"Parked vehicle. Ticket ID: {ticket.get_ticket_id()}")
                return
            elif vehicle_type == "BIKE":
                if floor[1] == None: 
                    ticket = Ticket(self.parking_lot_id,floor_ind + 1, 2)
                    self.floors[floor_ind][1] = {'ticket_id' : ticket.get_ticket_id(),'vehicle' : vehicle}
                    print(f"Parked vehicle. Ticket ID: {ticket.get_ticket_id()}")
                    return
                elif floor[2] == None:
                    ticket = Ticket(self.parking_lot_id,floor_ind + 1, 3)
                    self.floors[floor_ind][2] = {'ticket_id' : ticket.get_ticket_id(),'vehicle' : vehicle}
                    print(f"Parked vehicle. Ticket ID: {ticket.get_ticket_id()}")
                    return
            elif vehicle_type == "CAR":
                for slot_no in range(3,len(floor)):
                    if floor[slot_no] == None:
                        ticket = Ticket(self.parking_lot_id,floor_ind + 1, slot_no + 1)
                        self.floors[floor_ind][slot_no] = {'ticket_id' : ticket.get_ticket_id(),'vehicle' : vehicle}
                        print(f"Parked vehicle. Ticket ID: {ticket.get_ticket_id()}")
                        return
            
        print("Parking Lot Full")

    def remove_vehicle(self,ticket_id : str):
        ticket_floor = int(ticket_id[7]) - 1
        ticket_slot = int(ticket_id[9]) - 1

        if ticket_floor >= 0 and ticket_floor < self.number_of_floors and ticket_slot >= 0 and ticket_slot < self.number_of_slots_per_floor:
            if self.floors[ticket_floor][ticket_slot] != None and self.floors[ticket_floor][ticket_slot]["ticket_id"] == ticket_id:
                print(f"Removed vehicle with Registration Number: {self.floors[ticket_floor][ticket_slot]["vehicle"].get_vehicle_registration()} and Color: {self.floors[ticket_floor][ticket_slot]["vehicle"].get_vehicle_color()}")
                self.floors[ticket_floor][ticket_slot] = None
                return
            
        print("Invalid Ticket")
        

    def display_free_count(self, vehicle_type : str):
        print_count = 0
        for floor_ind in range(len(self.floors)):
            floor = self.floors[floor_ind]
            if vehicle_type == "TRUCK" and (floor[0] == None):
                print_count = 1
            elif vehicle_type == "BIKE":
                if floor[1] == None and floor[2] == None:
                    print_count = 2
                elif (floor[1] == None and floor[2] != None) or (floor[1] != None and floor[2] == None):
                    print_count = 1
            elif vehicle_type == "CAR":
                print_count = sum(x == None for x in floor[3:])
            print(f"No. of free slots for {vehicle_type} on Floor {floor_ind + 1}: {print_count}")

    def display_free_slots(self, vehicle_type : str):
        for floor_ind in range(len(self.floors)):
            available_slots = []
            floor = self.floors[floor_ind]
            if vehicle_type == "TRUCK" and (floor[0] == None):
                available_slots.append(1)
            elif vehicle_type == "BIKE":
                if floor[1] == None and floor[2] == None:
                    available_slots.append(2)
                    available_slots.append(3)
                elif floor[1] == None and floor[2] != None:
                    available_slots.append(2)
                elif floor[1] != None and floor[2] == None:
                    available_slots.append(3)
            elif vehicle_type == "CAR":
                available_slots = [index + 4 for index, value in enumerate(floor[3:]) if value == None]
            print(f"Free slots for {vehicle_type} on Floor {floor_ind + 1}: {available_slots}")

    def display_occupied_slots(self, vehicle_type : str):
        for floor_ind in range(len(self.floors)):
            occupied_slots = []
            floor = self.floors[floor_ind]
            if vehicle_type == "TRUCK" and (floor[0] != None):
                occupied_slots.append(1)
            elif vehicle_type == "BIKE":
                if floor[1] != None and floor[2] != None:
                    occupied_slots.append(2)
                    occupied_slots.append(3)
                elif floor[1] == None and floor[2] != None:
                    occupied_slots.append(3)
                elif floor[1] != None and floor[2] == None:
                    occupied_slots.append(2)
            elif vehicle_type == "CAR":
                occupied_slots = [index + 4 for index, value in enumerate(floor[3:]) if value != None]
            print(f"Occupied slots for {vehicle_type} on Floor {floor_ind + 1}: {occupied_slots}")

class Ticket:
    def __init__(self,parking_lot_id : str, floor_no : int, slot_no : int) -> None:
        self.ticket_id = f"{parking_lot_id}_{floor_no}_{slot_no}"
    
    def get_ticket_id(self) -> str:
        return self.ticket_id


if __name__ == "__main__":
    print("Execution Started")
    print()
    parking_lot = ParkingLot("PR1234",2,6)
    print()
    parking_lot.display_free_count("CAR")
    parking_lot.display_free_count("BIKE")
    parking_lot.display_free_count("TRUCK")
    print()
    parking_lot.display_free_slots("CAR")
    parking_lot.display_free_slots("BIKE")
    parking_lot.display_free_slots("TRUCK")
    print()
    parking_lot.display_occupied_slots("CAR")
    parking_lot.display_occupied_slots("BIKE")
    parking_lot.display_occupied_slots("TRUCK")
    print()
    parking_lot.park_vehicle("CAR","KA-01-DB-1234","black")
    parking_lot.park_vehicle("CAR","KA-02-CB-1334","red")
    parking_lot.park_vehicle("CAR","KA-01-DB-1133","black")
    parking_lot.park_vehicle("CAR","KA-05-HJ-8432","white")
    parking_lot.park_vehicle("CAR","WB-45-HO-9032","white")
    parking_lot.park_vehicle("CAR","KA-01-DF-8230","black")
    parking_lot.park_vehicle("CAR","KA-21-HS-2347","red")
    print()
    parking_lot.display_free_count("CAR")
    parking_lot.display_free_count("BIKE")
    parking_lot.display_free_count("TRUCK")
    print()
    parking_lot.remove_vehicle("PR1234_2_5")
    parking_lot.remove_vehicle("PR1234_2_5")
    parking_lot.remove_vehicle("PR1234_2_7")
    print()
    parking_lot.display_free_count("CAR")
    parking_lot.display_free_count("BIKE")
    parking_lot.display_free_count("TRUCK")
    print()
    parking_lot.display_free_slots("CAR")
    parking_lot.display_free_slots("BIKE")
    parking_lot.display_free_slots("TRUCK")
    print()
    parking_lot.display_occupied_slots("CAR")
    parking_lot.display_occupied_slots("BIKE")
    parking_lot.display_occupied_slots("TRUCK")
    print()
    parking_lot.park_vehicle("BIKE","KA-01-DB-1541","black")
    parking_lot.park_vehicle("TRUCK","KA-32-SJ-5289","orange")
    parking_lot.park_vehicle("TRUCK","KL-54-DN-4582","green")
    parking_lot.park_vehicle("TRUCK","KL-12-HF-4542","green")
    print()
    parking_lot.display_free_count("CAR")
    parking_lot.display_free_count("BIKE")
    parking_lot.display_free_count("TRUCK")
    print()
    parking_lot.display_free_slots("CAR")
    parking_lot.display_free_slots("BIKE")
    parking_lot.display_free_slots("TRUCK")
    print()
    parking_lot.display_occupied_slots("CAR")
    parking_lot.display_occupied_slots("BIKE")
    parking_lot.display_occupied_slots("TRUCK")
    print()
    print("Execution Ended")


