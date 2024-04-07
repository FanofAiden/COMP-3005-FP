-- Admin Table
INSERT INTO Admin(adminID,name) VALUES
(0,'Admin');

-- ExerciseRoutine Table
INSERT INTO ExerciseRoutine(Name) VALUES
('push/pull/legs'),
('cardio'),
('HIIT'),
('Balanced');



-- Room Table
INSERT INTO Room(Name) VALUES
('Weight room'),
('Yoga room'),
('Dance room'),
('boxing room');

-- Equipment Table
INSERT INTO Equipment(equipmentName, lastChecked, nextCheck) VALUES
('Chest Press','2024-01-01', '2024-06-01'),
('Leg Extension', '2024-01-01', '2024-06-01'),
('Leg Press', '2024-01-01', '2024-06-01'),
('Pulldown Machine', '2024-01-01', '2024-06-01'),
('Treadmill', '2024-01-01', '2024-06-01');

-- Member Table
INSERT INTO Member(name, email, age, goal, weight, height, routineID, billingType, monthlyBill) VALUES
('Aiden','aiden@gym.ca',19,'build muscle',160, '5"10',1,'CREDIT',40),
('Momo','momo@hello.ca',19,'build muscle',190, '6"4',2,'CREDIT',40);

-- Trainer Table
INSERT INTO Trainer (trainerID, name) VALUES 
    (100001,'Mark'),
    (100002,'Nolan'),
    (100003,'Allen');

-- TrainerAvailable Table
INSERT INTO TrainerAvailable (trainerID, days, time) VALUES 
    (100001,'Monday', '12pm-1pm'),
    (100002,'Tuesday', '10:30am-11:30am'),
    (100003,'Wednesday', '11am-12pm');

-- Exercise Table
INSERT INTO Exercise (exerciseName, routineID) VALUES 
    ('Chest Press, Lat Pulldown, Leg Extension', 1),
    ('30 min treadmill, 30 min exercise bike', 2),
    ('run 5k', 3);

-- Session Table
-- Assuming the first member and activity have IDs 1 based on your inserts
-- Assuming the first room has ID 1 based on your inserts
INSERT INTO Session (trainerAvaID, roomID, capacity, sesName) VALUES 
    (1, 1, 1,'Personal Training'),
    (2, 2, 10, 'Group Bike Ride');
