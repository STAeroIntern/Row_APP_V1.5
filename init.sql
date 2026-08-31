-- Table to store all relevant information for report list display on the app

CREATE TABLE IF NOT EXISTS reports (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(250) NOT NULL,
    uav_id INT NOT NULL,
    inspection_datetime DATETIME NOT NULL,
    safe_clearance_distance INT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Pending'
);


-- Table to store output file paths of every uploaded report

CREATE TABLE IF NOT EXISTS report_files (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    report_id INT NOT NULL,
    report_path VARCHAR(500) NOT NULL,
    video_path VARCHAR(250) NOT NULL,
    debug_path VARCHAR(250),
    FOREIGN KEY (report_id) REFERENCES reports(id)
);
