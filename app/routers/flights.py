from typing import Optional, List
from sqlalchemy.exc import SQLAlchemyError
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from datetime import datetime, time, timedelta

from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/flight",
    tags=['Flight']
)


# for users
# to search for flights using query parameters
@router.get("/", response_model=List[schemas.FlightResponse])
def get_flights(
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.get_current_user),
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    departure_airport: Optional[str] = None,
    destination_airport: Optional[str] = None
):
    try:
        query = db.query(models.Flight)

        if start_time and end_time:
            query = query.filter(models.Flight.departure_datetime.between(start_time, end_time))

        if departure_airport:
            query = query.filter(models.Flight.departure_airport == departure_airport)

        if destination_airport:
            query = query.filter(models.Flight.destination_airport == destination_airport)

        flights = query.all()
        return flights
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching flights: {str(e)}"
        )



#  for admin
@router.get("/getall", response_model=List[schemas.FlightResponse])
def get_all_flights(
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_admin),
):
    try:
        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized to create. Login with admin."
            )
        flights = db.query(models.Flight).all()
        return flights
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching all flights: {str(e)}"
        )

@router.get("/{id}") #, response_model=schemas.FlightResponse)
def get_flight(
    id: str,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_admin)
):
    try:
        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized to create. Login, flight with admin."
            )
        flight = db.query(models.Flight).filter(models.Flight.flight_number == id).first()

        print(current_user.id, flight)
        if not flight:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Flight with id: {id} was not found"
            )

        return flight
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching flight: {str(e)}"
        )


# to add flights
@router.post("/", response_model=schemas.FlightResponse, status_code=status.HTTP_201_CREATED)
def create_flight(
    flight_data: schemas.FlightCreate,
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.get_current_admin)
):
    try:
        print("hello1", current_user.id)
        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized to create. Login with admin."
            )

        new_flight = models.Flight(**flight_data.dict())
        
        db.add(new_flight)
        db.commit()
        db.refresh(new_flight)

        return new_flight    
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching flights: {str(e)}"
        )


# def to delete flight and respective booking along it
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_flight(
    id: str, 
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_admin)
):
    try:
        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized to delete. Login with admin."
            )

        flight = db.query(models.Flight).filter(models.Flight.flight_number == id).first()

        if flight is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Flight with id: {id} does not exist."
            )
        db.delete(flight)
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during flight deletion: {str(e)}"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
