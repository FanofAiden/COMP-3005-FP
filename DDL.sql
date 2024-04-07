-- Admin Table
CREATE TABLE Admin (
    adminID INT PRIMARY KEY,
    name VARCHAR(255)
);
-- ExerciseRoutine Table
CREATE TABLE ExerciseRoutine (
    routineID SERIAL PRIMARY KEY,
    Name VARCHAR(255)
);
-- Activity Table
CREATE TABLE Activity (
    actID SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

-- Room Table
CREATE TABLE Room (
    roomID SERIAL PRIMARY KEY,
    Name VARCHAR(255)
);

-- Equipment Table
CREATE TABLE Equipment (
    equipmentID SERIAL PRIMARY KEY,
    equipmentName VARCHAR(256),
    lastChecked DATE,   --changed from INT TO DATE
    nextCheck DATE
);
-- Member Table
CREATE TABLE Member (
    memID SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    age INT,
    goal VARCHAR(255),
    weight INT,
    height VARCHAR(10), --changed to string
    routineID INT DEFAULT NULL,
    billingType VARCHAR(255),
    monthlyBill INT,
    FOREIGN KEY (routineID) REFERENCES ExerciseRoutine(routineID)
);

-- Trainer Table
CREATE TABLE Trainer (
    trainerID INT PRIMARY KEY,
    name VARCHAR(255)
);

-- TrainerAvailable Table
CREATE TABLE TrainerAvailable (
    trainerAvaID SERIAL PRIMARY KEY,
    trainerID INT,
    days VARCHAR(255),
    time VARCHAR(255),
    FOREIGN KEY (trainerID) REFERENCES Trainer(trainerID)
);

-- Exercise Table
CREATE TABLE Exercise (
    exerciseID SERIAL PRIMARY KEY,
	exerciseName VARCHAR(256),
    routineID INT,
    FOREIGN KEY (routineID) REFERENCES ExerciseRoutine(routineID)
);

-- Session Table
CREATE TABLE Session (
    sesID SERIAL PRIMARY KEY,
    sesName VARCHAR(256),
    trainerAvaID INT,
    roomID INT,
    capacity INT,
    FOREIGN KEY (trainerAvaID) REFERENCES TrainerAvailable(trainerAvaID),
    FOREIGN KEY (roomID) REFERENCES Room(roomID)
);

CREATE TABLE SessionMemberTable (
    sesID INT,
    memID INT,
    FOREIGN KEY (sesID) REFERENCES Session(sesID),
    FOREIGN KEY (memID) REFERENCES Member(memID)
);