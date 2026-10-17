from typing import Annotated

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, StringConstraints, model_validator, AwareDatetime
app = FastAPI()

flights = []

airportcode = Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=3, to_upper=True)]

class flight_info(BaseModel):
    flight_num : int
    origin : airportcode
    destination : airportcode
    capacity : int = Field(gt=0)
    departure_time : AwareDatetime
    arrival_time : AwareDatetime

    @model_validator(mode="after")
    def validate_time(self):
        if self.arrival_time <= self.departure_time:
            raise ValueError("arrival time must be later than departure time")
        return self

@app.get("/flights/{id}")
def get_flights(id : int):
    for flight in flights:
        if flight["id"] == id:
            return flight
    raise HTTPException(status_code=404,detail="flight not found")
        
    

@app.post("/flights", status_code=201)
def upload_flight(flight: flight_info ): 
    nxt_id = len(flights) + 1
    flight_dict = flight.model_dump()
    flight_dict["id"] = nxt_id
    flights.append(flight_dict)
    return flight_dict

