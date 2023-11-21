CREATE database assignment;
USE assignment;

CREATE TABLE USER (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    given_name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    city VARCHAR(255),
    phone_number VARCHAR(20),
    profile_description TEXT,
    password VARCHAR(255) NOT NULL
);


INSERT INTO USER (user_id, email, given_name, surname, city, phone_number, profile_description, password)
VALUES
    (1, 'caregiver1@gmail.com', 'Aygul', 'Murat', 'Astana', '+7 777-111-2233', 'Babysitter', 'password1'),
    (2, 'caregiver2@gmail.com', 'Adilet', 'Adiletov', 'Astana', '+7 701-222-3344', 'Caregiver for elderly', 'password2'),
    (3, 'caregiver3@gmail.com', 'Gulnaz', 'Murat', 'Astana', '+7 777-333-4455', 'Playmate for children', 'password3'),
    (4, 'caregiver4@gmail.com', 'Aizhan', 'Murat', 'Astana', '+7 701-444-5566', 'Babysitter', 'password4'),
    (5, 'caregiver5@gmail.com', 'Erbol', 'Erbolov', 'Astana', '+7 702-555-6677', 'Caregiver for elderly', 'password5'),
    (6, 'caregiver6@gmail.com', 'Saule', 'Murat', 'Astana', '+7 701-666-7788', 'Caregiver for elderly', 'password6'),
    (7, 'caregiver7@gmail.com', 'Madina', 'Murat', 'Astana', '+7 702-777-8899', 'Caregiver for elderly', 'password7'),
    (8, 'caregiver8@gmail.com', 'Elzhan', 'Murat', 'Astana', '+7 701-888-9900', 'Babysitter', 'password8'),
    (9, 'caregiver9@gmail.com', 'Ayna', 'Rakhat', 'Astana', '+7 702-999-0011', 'Babysitter', 'password9'),
    (10, 'caregiver10@gmail.com', 'Bakyt', 'Bakytov', 'Astana', '+7 701-001-1122', 'Caregiver for elderly', 'password10'),

    (11, 'family11@email.com', 'Bolat', 'Bolatov', 'Astana', '+7 777-111-2233', 'Looking for a babysitter for my child', 'password11'),
    (12, 'family12@email.com', 'Askar', 'Askarov', 'Astana', '+7 701-222-3344', 'Looking for elderly caregiver', 'password12'),
    (13, 'family13@email.com', 'Doszhan', 'Doszhanov', 'Astana', '+7 777-333-4455', 'Looking for a playmate for my children', 'password13'),
    (14, 'family14@email.com', 'Kasym', 'Kasymova', 'Astana', '+7 701-444-5566', 'Looking for a babysitter for my son', 'password14'),
    (15, 'family15@email.com', 'Bekzhan', 'Bekzhanov', 'Astana', '+7 702-555-6677', 'Looking for an elderly caregiver', 'password15'),
    (16, 'family16@email.com', 'Suleimen', 'Suleimenova', 'Astana', '+7 701-666-7788', 'Looking for an elderly caregiver', 'password16'),
    (17, 'family17@email.com', 'Ismail', 'Ismailova', 'Astana', '+7 702-777-8899', 'Looking for an elderly caregiver', 'password17'),
    (18, 'family18@email.com', 'Kenzhebek', 'Kenzhebekov', 'Astana', '+7 701-888-9900', 'Looking for a babysitter for my child', 'password18'),
    (19, 'family19@email.com', 'Ait', 'Aitkhozhina', 'Astana', '+7 702-999-0011', 'Looking for a babysitter for my child', 'password19'),
    (20, 'family20@email.com', 'Serik', 'Serikov', 'Astana', '+7 701-001-1122', 'Looking for an elderly caregiver', 'password20');

DROP TABLE USER;
DROP TABLE CAREGIVER;
DROP TABLE JOB_APPLICATION;
DROP TABLE JOB;
DROP TABLE APPOINTMENT;
DROP TABLE MEMBER;
DROP TABLE ADDRESS;
SELECT * FROM USER;

CREATE TABLE CAREGIVER (
    caregiver_user_id INT PRIMARY KEY,
    photo BLOB,
    gender VARCHAR(20),
    caregiving_type VARCHAR(255),
    hourly_rate INT,
    FOREIGN KEY (caregiver_user_id) REFERENCES USER(user_id) on delete cascade
);

INSERT INTO CAREGIVER (caregiver_user_id, photo, gender, caregiving_type, hourly_rate)
VALUES
    (1, NULL, 'Female', 'Babysitter', 20),
    (2, NULL, 'Male', 'Caregiver for elderly', 22),
    (3, NULL, 'Female', 'Playmate for children', 15),
    (4, NULL, 'Female', 'Babysitter', 20),
    (5, NULL, 'Male', 'Caregiver for elderly', 18),
    (6, NULL, 'Female', 'Caregivr for elderly', 15),
    (7, NULL, 'Female', 'Caregiver for elderly', 20),
    (8, NULL, 'Female', 'Babysitter', 15),
    (9, NULL, 'Female', 'Babysitter', 25),
    (10, NULL, 'Male', 'Caregiver for elderly', 20);


CREATE TABLE MEMBER (
    member_user_id INT PRIMARY KEY,
    house_rules TEXT,
    FOREIGN KEY (member_user_id) REFERENCES USER(user_id) on delete cascade
);

INSERT INTO MEMBER (member_user_id, house_rules)
VALUES
    (11, 'Hygiene and cleanliness are a must.'),
    (12, 'No pets.'),
    (13, 'Provide a safe play area for children.'),
    (14, 'Hygiene and cleanliness are a must.'),
    (15, 'Hygiene and cleanliness are a must.'),
    (16, 'No pets.'),
    (17, 'Need.'),
    (18, 'Hygiene and cleanliness are a must.'),
    (19, 'No pets.'),
    (20, 'Hygiene and cleanliness are a must.');

CREATE TABLE ADDRESS (
    member_user_id INT PRIMARY KEY,
    house_number INT,
    street VARCHAR(255),
    town VARCHAR(255),
    FOREIGN KEY (member_user_id) REFERENCES MEMBER(member_user_id) ON delete cascade
);

INSERT INTO ADDRESS (member_user_id, house_number, street, town)
VALUES
    (11, 5, 'Turan', 'Astana'),
    (12, 4, 'Sauran', 'Astana'),
    (13, 78, 'Syganak', 'Astana'),
    (14, 10, 'Dostyk', 'Astana'),
    (15, 20, 'Turan', 'Astana'),
    (16, 3, 'Sarayshyk', 'Astana'),
    (17, 12, 'Turan', 'Astana'),
    (18, 5, 'Dostyk', 'Astana'),
    (19, 6, 'Respublika', 'Astana'),
    (20, 7, 'Dostyk', 'Astana');

CREATE TABLE JOB (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    member_user_id INT,
    required_caregiving_type VARCHAR(255),
    other_requirements TEXT,
    date_posted DATE,
    FOREIGN KEY (member_user_id) REFERENCES MEMBER(member_user_id) on delete cascade
);

INSERT INTO JOB (job_id, member_user_id, required_caregiving_type, other_requirements, date_posted)
VALUES
    (1, 11, 'Babysitter', 'Must be gentle with children.', '2023-10-30'),
    (2, 12, 'Caregiver for elderly', 'No pets.', '2023-11-01'),
    (3, 13, 'Playmate for children', 'Provide a safe play area for children.', '2023-11-05'),
    (4, 14, 'Babysitter', 'Nust be gentle with children.', '2023-10-20'),
    (5, 15, 'Caregiver for elderly', 'Hygiene and cleanliness are a must.', '2023-11-04'),
    (6, 16, 'Caregiver for elderly', 'No pets.', '2023-11-02'),
    (7, 17, 'Caregiver for elderly', 'No pets.', '2023-10-31'),
    (8, 18, 'Babysitter', 'Hygiene and cleanliness are a must.', '2023-11-04'),
    (9, 19, 'Babysitter', 'No pets.', '2023-11-05'),
    (10, 20, 'Caregiver for elderly', 'Hygiene and cleanliness are a must.', '2023-10-25');

CREATE TABLE JOB_APPLICATION (
    caregiver_user_id INT,
    job_id INT,
    date_applied DATE,
    PRIMARY KEY (caregiver_user_id, job_id),
    FOREIGN KEY (caregiver_user_id) REFERENCES CAREGIVER(caregiver_user_id) on delete cascade,
    FOREIGN KEY (job_id) REFERENCES JOB(job_id) ON DELETE CASCADE
);

INSERT INTO JOB_APPLICATION (caregiver_user_id, job_id, date_applied)
VALUES
    (1, 1, '2023-11-01'),
    (2, 2, '2023-11-02'),
    (3, 3, '2023-11-06'),
    (4, 4, '2023-11-04'),
    (5, 5, '2023-11-05'),
    (6, 10, '2023-11-06'),
    (7, 6, '2023-11-07'),
    (8, 9, '2023-11-08'),
    (9, 8, '2023-11-09'),
    (10, 7, '2023-11-10');


CREATE TABLE APPOINTMENT (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    caregiver_user_id INT,
    member_user_id INT,
    appointment_date DATE,
    appointment_time TIME,
    work_hours VARCHAR(50),
    status VARCHAR(50),
    FOREIGN KEY (caregiver_user_id) REFERENCES CAREGIVER(caregiver_user_id) on delete cascade,
    FOREIGN KEY (member_user_id) REFERENCES MEMBER(member_user_id) on delete cascade
);

INSERT INTO APPOINTMENT (caregiver_user_id, member_user_id, appointment_date, appointment_time, work_hours, status)
VALUES
    (1, 11, '2023-11-15', '10:00:00', '4 hours', 'Confirmed'),
    (2, 12, '2023-11-17', '14:00:00', '3 hours', 'Confirmed'),
    (3, 13, '2023-11-18', '15:30:00', '5 hours', 'Confirmed'),
    (4, 14, '2023-11-21', '09:00:00', '6 hours', 'Confirmed'),
    (5, 15, '2023-11-23', '13:45:00', '7 hours', 'Declined'),
    (6, 20, '2023-11-24', '11:00:00', '4 hours', 'Confirmed'),
    (7, 16, '2023-11-26', '14:30:00', '5 hours', 'Confirmed'),
    (8, 19, '2023-11-27', '09:30:00', '4 hours', 'Declined'),
    (9, 18, '2023-11-29', '15:15:00', '8 hours', 'Confirmed'),
    (10, 17, '2023-11-30', '12:00:00', '3 hours', 'Confirmed');
SELECT * FROM user;
#3.1
UPDATE USER
SET phone_number = '+77771010001'
WHERE given_name = 'Askar' AND surname = 'Askarov';

#3.2
UPDATE CAREGIVER 
SET hourly_rate = 
    CASE
        WHEN hourly_rate < 9 THEN hourly_rate + 0.5
        ELSE hourly_rate * 1.1
    END;

#4.1
DELETE FROM JOB
WHERE member_user_id = (SELECT user_id FROM USER WHERE given_name = 'Bolat' AND surname = 'Bolatov');
 
#4.2
DELETE FROM MEMBER
WHERE member_user_id IN (SELECT member_user_id FROM ADDRESS WHERE street = 'Turan');

#5.1
SELECT a.appointment_id, a.caregiver_user_id AS caregiver_id, c.given_name AS caregiver_name, a.member_user_id AS member_id, m.given_name AS member_name
FROM appointment AS a, user AS c, user AS m
WHERE a.caregiver_user_id = c.user_id
AND a.member_user_id = m.user_id
AND a.status = 'Confirmed';

#5.2
SELECT job_id FROM JOB WHERE other_requirements LIKE '%gentle%';

#5.3
SELECT
    A.appointment_id,
    U.given_name AS caregiver_given_name,
    U.surname AS caregiver_surname,
    J.required_caregiving_type,
    A.work_hours
FROM
    APPOINTMENT A
JOIN
    CAREGIVER C ON A.caregiver_user_id = C.caregiver_user_id
JOIN
    USER U ON C.caregiver_user_id = U.user_id
JOIN
    JOB J ON A.member_user_id = J.member_user_id
WHERE
    J.required_caregiving_type = 'Babysitter';

#5.4
SELECT u.user_id, u.given_name, u.surname
FROM user AS u
WHERE u.user_id IN (
    SELECT m.member_user_id
    FROM member AS m
    WHERE m.member_user_id IN (
        SELECT a.member_user_id
        FROM address AS a
        WHERE a.town = 'Astana'
    ) 
    AND m.member_user_id IN (
        SELECT j.member_user_id
        FROM job AS j
        WHERE j.required_caregiving_type = 'Caregiver for elderly'
        AND j.other_requirements = 'No pets.'
    )
);

#6.1
SELECT J.job_id, COUNT(JA.caregiver_user_id) AS num_applicants
        FROM JOB AS J
        LEFT JOIN JOB_APPLICATION AS JA ON J.job_id = JA.job_id
        GROUP BY J.job_id;

#6.2
SELECT a.caregiver_user_id AS caregiver_id, c.given_name AS caregiver_name, 
       SUM(a.work_hours) AS total_hours
FROM appointment AS a
JOIN user AS c ON a.caregiver_user_id = c.user_id
WHERE a.status = 'Confirmed'
GROUP BY caregiver_id, caregiver_name;

#6.3
SELECT U.given_name, U.surname, AVG(C.hourly_rate) AS avg_hourly_rate
FROM APPOINTMENT AS A
JOIN USER AS U ON A.caregiver_user_id = U.user_id
JOIN CAREGIVER AS C ON U.user_id = C.caregiver_user_id
WHERE A.status = 'Confirmed'
GROUP BY U.given_name, U.surname;

#6.4
SELECT U.user_id, U.given_name, U.surname, C.hourly_rate
FROM USER AS U
JOIN CAREGIVER AS C ON U.user_id = C.caregiver_user_id
WHERE C.hourly_rate > (
    SELECT AVG(C2.hourly_rate)
    FROM CAREGIVER AS C2
    JOIN APPOINTMENT AS A ON C2.caregiver_user_id = A.caregiver_user_id
    WHERE A.status = 'Confirmed'
);

#7
SELECT A.caregiver_user_id, U.given_name, U.surname, SUM(TIME_TO_SEC(A.work_hours) * C.hourly_rate) AS total_cost
FROM APPOINTMENT AS A
JOIN USER AS U ON A.caregiver_user_id = U.user_id
JOIN CAREGIVER AS C ON A.caregiver_user_id = C.caregiver_user_id
WHERE A.status = 'Confirmed'
GROUP BY A.caregiver_user_id, U.given_name, U.surname;

#8
CREATE VIEW JobApplicationsView AS
SELECT JA.job_id, J.member_user_id AS family_id, U1.given_name AS family_given_name, U1.surname AS family_surname,
       J.required_caregiving_type, J.other_requirements, U2.given_name AS caregiver_given_name, U2.surname AS caregiver_surname
FROM JOB_APPLICATION AS JA
JOIN JOB AS J ON JA.job_id = J.job_id
JOIN USER AS U1 ON J.member_user_id = U1.user_id
JOIN USER AS U2 ON JA.caregiver_user_id = U2.user_id;
SELECT * FROM JobApplicationsView;



SELECT * FROM job;
SELECT * FROM user;
ALTER TABLE user
ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'caregiver';

UPDATE user
SET role = 'family'
WHERE user_id BETWEEN 11 AND 20;

DELETE FROM user
WHERE user_id = 24;

DROP VIEW jobapplicationsview;








SHOW GRANTS FOR 'root'@'localhost';

