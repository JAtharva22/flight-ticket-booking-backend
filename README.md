# Backend of Flight Ticket Booking System
video :-
https://www.youtube.com/watch?v=gMlcA1oTVV4

###![er](https://github.com/JAtharva22/flight-ticket-booking-backend/assets/93152317/932479ec-f6f4-4b77-a1c8-ba77758f600f)


#### This API  has 4 routes

## 1) flight route

#### This route is reponsible for creating flights(admin), deleting flight(admin), viewing all flights(admin), searching for flights(user)

## 2) Users route

#### This route is about creating users and searching user by id

## 3) Auth route

#### This route is about login system

## 4) bookings route

 #### This route is about creating booking of flight(user), user can view their own bookings(user), admin can view all the bookings(admin)

# how to run locally

````

uvicorn main:app --reload

````

Then you can use following link to use the  API

````

http://127.0.0.1:8000/docs 

````

## After run this API you need a database in postgres 
Create a database in postgres then create a file name .env and write the following things in you file 

````
DATABASE_HOSTNAME = localhost
DATABASE_PORT = 5432
DATABASE_PASSWORD = passward_that_you_set
DATABASE_NAME = name_of_database
DATABASE_USERNAME = User_name
SECRET_KEY = 09d25e094faa2556c818166b7a99f6f0f4c3b88e8d3e7 
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60(base)

````
### Note: SECRET_KEY in this exmple is just a psudo key.
