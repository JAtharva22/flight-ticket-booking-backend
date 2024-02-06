
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    
    bookings = relationship("Booking", back_populates="user")


class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Flight(Base):
    __tablename__ = "flights"
    
    id = Column(Integer, primary_key=True, nullable=False)
    flight_number = Column(String, nullable=False, unique=True)
    departure_airport = Column(String, nullable=False)
    destination_airport = Column(String, nullable=False)
    departure_datetime = Column(DateTime, nullable=False)
    available_seats = Column(Integer, default=60, nullable=False)
    
    bookings = relationship("Booking", back_populates="flight", cascade="all, delete-orphan")


class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    flight_id = Column(Integer, ForeignKey("flights.id", ondelete="CASCADE"), nullable=False)
    seat_number = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    user = relationship("User", back_populates="bookings")
    flight = relationship("Flight", back_populates="bookings")
