from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

# ====================================

class FlightBase(BaseModel):
    flight_number: str
    departure_airport: str
    destination_airport: str
    departure_datetime: datetime
    available_seats: Optional[int] = 60 

class FlightCreate(FlightBase):
    pass

class FlightResponse(BaseModel):
    id: int
    available_seats: int
    destination_airport: str
    flight_number: str
    departure_datetime: datetime
    departure_airport: str

    class Config:
        orm_mode = True
# ====================================

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class AdminCreate(BaseModel):
    username: str
    password: str

class AdminOut(BaseModel):
    id: int
    username: str
    class Config:
        orm_mode = True
        
class AdminLogin(BaseModel):
    role: str
    password: str


# ==============================================

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class UserToken(Token):
    user_id: int


class TokenData(BaseModel):
    id: Optional[str] = None


# =================================================
class BookingResponse(BaseModel):
    id: int
    user_id: int
    flight_id: int
    seat_number: int
    created_at: datetime
    
    class Config:
        orm_mode = True
    
class BookingWithFlightResponse(BookingResponse):
    flight_number: Optional[str]
    departure_airport: Optional[str]
    destination_airport: Optional[str]
    departure_datetime: Optional[datetime]
    available_seats: Optional[int]

    
