-- BRMSFinal1 Database Setup Script
-- 2️ Create database
CREATE DATABASE BRMSFinal1;
GO

USE BRMSFinal1;
GO
-- 4️ Create Tables with Foreign Keys

-- Route Table
CREATE TABLE Route (
    RouteID INT PRIMARY KEY,
    Source VARCHAR(50),
    Destination VARCHAR(50),
    Distance INT
);
GO

-- Bus Table (FK → Route)
CREATE TABLE Bus (
    BusID INT PRIMARY KEY,
    BusName VARCHAR(50),
    Capacity INT,
    RouteID INT,
    CONSTRAINT FK_Bus_Route FOREIGN KEY (RouteID) REFERENCES Route(RouteID)
);
GO

-- Passenger Table
CREATE TABLE Passenger (
    PassengerID INT PRIMARY KEY,
    Name VARCHAR(50),
    Age INT,
    Gender VARCHAR(10),
    Contact VARCHAR(20)
);
GO

-- Reservation Table (FK → Passenger, Bus)
CREATE TABLE Reservation (
    ReservationID INT PRIMARY KEY,
    PassengerID INT,
    BusID INT,
    SeatNo INT,
    NoOfSeats INT,
    Date DATE,
    CONSTRAINT FK_Reservation_Passenger FOREIGN KEY (PassengerID) REFERENCES Passenger(PassengerID),
    CONSTRAINT FK_Reservation_Bus FOREIGN KEY (BusID) REFERENCES Bus(BusID)
);
GO

-- Payment Table (FK → Reservation)
CREATE TABLE Payment (
    PaymentID INT PRIMARY KEY,
    ReservationID INT,
    Amount INT,
    PaymentMode VARCHAR(20),
    CONSTRAINT FK_Payment_Reservation FOREIGN KEY (ReservationID) REFERENCES Reservation(ReservationID)
);
GO


SELECT * FROM Bus;
SELECT * FROM Route;
SELECT * FROM Passenger;
SELECT * FROM Reservation;
SELECT * FROM Payment;

