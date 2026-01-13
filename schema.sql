-- Create participants table
CREATE TABLE IF NOT EXISTS participants (
    participant_id INT PRIMARY KEY,
    name TEXT,
    prompted BOOLEAN,
    consent BOOLEAN,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create responses table
CREATE TABLE IF NOT EXISTS responses (
    participant_id INT PRIMARY KEY REFERENCES participants(participant_id),
    task1_id INT,
    task1_r1 TEXT,
    task1_r2 TEXT,
    task1_r3 TEXT,
    task2_id INT,
    task2_r1 TEXT,
    task2_r2 TEXT,
    task2_r3 TEXT,
    task3_id INT,
    task3_r1 TEXT,
    task3_r2 TEXT,
    task3_r3 TEXT,
    task4_id INT,
    task4_r1 TEXT,
    task4_r2 TEXT,
    task4_r3 TEXT,
    expert_id INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
