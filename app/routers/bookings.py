# routers/booking.py

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, aliased

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/booking",
    tags=['Booking']
)

# user
@router.post("/book/{flight_id}", response_model=schemas.BookingResponse)
def book_flight(
    flight_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.get_current_user)
):
    try:
        # Check if the flight has available seats
        flight = db.query(models.Flight).filter(models.Flight.id == flight_id).first()
        if not flight or flight.available_seats <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No available seats on this flight."
            )

        seats = flight.available_seats
        seat_number = seats - 1

        new_booking = models.Booking(
            user_id=current_user.id,
            flight_id=flight_id,
            seat_number=seat_number
        )

        flight.available_seats -= 1

        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)

        return new_booking

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while booking the flight: {str(e)}"
        )


# ==========================================================

# user
@router.get("/", response_model=List[schemas.BookingWithFlightResponse])
def get_user_bookings(
    db: Session = Depends(get_db),
    current_user= Depends(oauth2.get_current_user)
):
    try:
        flight_alias = aliased(models.Flight)
        # Use join and add_columns for a outer join
        bookings = db.query(models.Booking, flight_alias).outerjoin(
            flight_alias, models.Booking.flight_id == flight_alias.id).filter(
                models.Booking.user_id == current_user.id).all()
        result_list = []
        for booking, flight in bookings:
            result_dict = {
                    "id": booking.id,
                    "seat_number": booking.seat_number,
                    "user_id": booking.user_id,
                    "created_at": booking.created_at,
                    "flight_id": booking.flight_id,
                    "available_seats": flight.available_seats,
                    "destination_airport": flight.destination_airport,
                    "flight_number": flight.flight_number,
                    "departure_datetime": flight.departure_datetime,
                    "departure_airport": flight.departure_airport,
                }
            result_list.append(result_dict)

        return result_list

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching user bookings: {str(e)}"
        )


# ==========================================================

# admin
@router.get("/allbookings", response_model=List[schemas.BookingResponse])
def get_all_bookings(
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.get_current_admin)
):
    try:
        bookings = db.query(models.Booking).all()
        return bookings

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching all bookings: {str(e)}"
        )
