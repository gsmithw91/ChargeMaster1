-- Hospital Location Table
CREATE TABLE HospitalLocation (
    LocationID INT PRIMARY KEY IDENTITY(1,1),
    SystemID INT NOT NULL,
    LocationName NVARCHAR(255) NOT NULL,
    Address NVARCHAR(255) NOT NULL,
    City NVARCHAR(255) NOT NULL,
    State CHAR(2) NOT NULL,
    ZipCode NVARCHAR(10),
    Phone NVARCHAR(20),
    CONSTRAINT FK_HospitalSystem FOREIGN KEY (SystemID) REFERENCES HospitalSystem(SystemID)
);
GO