from fastapi.testclient import TestClient
from main import app, flights

client = TestClient(app)

def test_zero_capacity():
    flight = {
        "flight_num": 430,
        "origin": "HYD",
        "destination": "DEL",
        "capacity": 0,
        "departure_time": "2026-10-18T10:00:00+05:30",
        "arrival_time": "2026-10-18T12:00:00+05:30"
    }

    count_before = len(flights)
    response = client.post("/flights",json=flight)
    assert response.status_code == 422
    assert len(flights) == count_before

def test_missing_route_info():
    flight = {
        "flight_num": 430,
        "destination": "DEL",
        "capacity": 233,
        "departure_time": "2026-10-18T10:00:00+05:30",
        "arrival_time": "2026-10-18T12:00:00+05:30"
    }

    count_before = len(flights)

    response = client.post("/flights",json=flight)
    assert response.status_code == 422
    assert len(flights) == count_before

def test_timing_mismatch():
    flight = {
        "flight_num": 430,
        "origin": "HYD",
        "destination": "DEL",
        "capacity": 180,
        "departure_time": "2026-10-18T13:00:00+05:30",
        "arrival_time": "2026-10-18T12:00:00+05:30"
    }

    count_before = len(flights)
     
    response = client.post("/flights",json=flight)
    assert response.status_code == 422
    assert len(flights) == count_before

def test_retriving_valid_flight():
    flight = {
        "flight_num": 430,
        "origin": "HYD",
        "destination": "DEL",
        "capacity": 180,
        "departure_time": "2026-10-18T12:00:00+05:30",
        "arrival_time": "2026-10-18T13:00:00+05:30"
    }

    response = client.post("/flights",json=flight)
    assert response.status_code == 201
    id = response.json()["id"]
    response1 = client.get(f"/flights/{id}")
    assert response1.status_code == 200
    
    assert response.json() == response1.json()
    

