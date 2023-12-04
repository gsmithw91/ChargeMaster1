USE ChargeMasterDB; -- Make sure we're in the correct database
SELECT * FROM dbo.HospitalSystem WHERE SystemID IS NULL;

ALTER TABLE dbo.HospitalSystem
ALTER COLUMN SystemID INT NOT NULL;


ALTER TABLE dbo.HospitalSystem
ADD CONSTRAINT PK_HospitalSystem PRIMARY KEY (SystemID);


CREATE TABLE dbo.Elig_Advocate (
    EligibilityID INT PRIMARY KEY IDENTITY(1,1),
    SystemID INT NOT NULL,
    LocationID INT NOT NULL,
    InsuranceTypeID INT NOT NULL,
    Carrier VARCHAR(255) NOT NULL,
    InNetwork BIT NOT NULL,
    EligibilityYear INT NOT NULL,
    PlanName VARCHAR(255) NOT NULL,
    CONSTRAINT FK_Elig_Advocate_SystemID FOREIGN KEY (SystemID) REFERENCES dbo.HospitalSystem(SystemID),
    CONSTRAINT FK_Elig_Advocate_LocationID FOREIGN KEY (LocationID) REFERENCES dbo.HospitalLocation(LocationID),
    CONSTRAINT FK_Elig_Advocate_InsuranceTypeID FOREIGN KEY (InsuranceTypeID) REFERENCES dbo.InsuranceTypes(InsuranceTypeID)
);

-- Add any additional indices and constraints as necessary to match dbo.Elig_Northwestern
-- The following indexes are examples, add or remove based on your actual dbo.Elig_Northwestern indexes
CREATE INDEX IDX_Elig_Advocate_SystemID ON dbo.Elig_Advocate(SystemID);
CREATE INDEX IDX_Elig_Advocate_LocationID ON dbo.Elig_Advocate(LocationID);
CREATE INDEX IDX_Elig_Advocate_InsuranceTypeID ON dbo.Elig_Advocate(InsuranceTypeID);



CREATE TABLE dbo.Elig_Loyola (
    EligibilityID INT PRIMARY KEY IDENTITY(1,1),
    SystemID INT NOT NULL,
    LocationID INT NOT NULL,
    InsuranceTypeID INT NOT NULL,
    Carrier VARCHAR(255) NOT NULL,
    InNetwork BIT NOT NULL,
    EligibilityYear INT NOT NULL,
    PlanName VARCHAR(255) NOT NULL,
    CONSTRAINT FK_Elig_Loyola_SystemID FOREIGN KEY (SystemID) REFERENCES dbo.HospitalSystem(SystemID),
    CONSTRAINT FK_Elig_Loyola_LocationID FOREIGN KEY (LocationID) REFERENCES dbo.HospitalLocation(LocationID),
    CONSTRAINT FK_Elig_Loyola_InsuranceTypeID FOREIGN KEY (InsuranceTypeID) REFERENCES dbo.InsuranceTypes(InsuranceTypeID)
);

-- Add any additional indices and constraints as necessary to match dbo.Elig_Northwestern
-- The following indexes are examples, add or remove based on your actual dbo.Elig_Northwestern indexes
CREATE INDEX IDX_Elig_Loyola_SystemID ON dbo.Elig_Loyola(SystemID);
CREATE INDEX IDX_Elig_Loyola_LocationID ON dbo.Elig_Loyola(LocationID);
CREATE INDEX IDX_Elig_Loyola_InsuranceTypeID ON dbo.Elig_Loyola(InsuranceTypeID);



CREATE TABLE dbo.Elig_Northshore (
    EligibilityID INT PRIMARY KEY IDENTITY(1,1),
    SystemID INT NOT NULL,
    LocationID INT NOT NULL,
    InsuranceTypeID INT NOT NULL,
    Carrier VARCHAR(255) NOT NULL,
    InNetwork BIT NOT NULL,
    EligibilityYear INT NOT NULL,
    PlanName VARCHAR(255) NOT NULL,
    CONSTRAINT FK_Elig_Northshore_SystemID FOREIGN KEY (SystemID) REFERENCES dbo.HospitalSystem(SystemID),
    CONSTRAINT FK_Elig_Northshore_LocationID FOREIGN KEY (LocationID) REFERENCES dbo.HospitalLocation(LocationID),
    CONSTRAINT FK_Elig_Northshore_InsuranceTypeID FOREIGN KEY (InsuranceTypeID) REFERENCES dbo.InsuranceTypes(InsuranceTypeID)
);

-- Add any additional indices and constraints as necessary to match dbo.Elig_Northwestern
-- The following indexes are examples, add or remove based on your actual dbo.Elig_Northwestern indexes
CREATE INDEX IDX_Elig_Northshore_SystemID ON dbo.Elig_Northshore(SystemID);
CREATE INDEX IDX_Elig_Northshore_LocationID ON dbo.Elig_Northshore(LocationID);
CREATE INDEX IDX_Elig_Northshore_InsuranceTypeID ON dbo.Elig_Northshore(InsuranceTypeID);

CREATE TABLE dbo.Elig_Rush (
    EligibilityID INT PRIMARY KEY IDENTITY(1,1),
    SystemID INT NOT NULL,
    LocationID INT NOT NULL,
    InsuranceTypeID INT NOT NULL,
    Carrier VARCHAR(255) NOT NULL,
    InNetwork BIT NOT NULL,
    EligibilityYear INT NOT NULL,
    PlanName VARCHAR(255) NOT NULL,
    CONSTRAINT FK_Elig_Rush_SystemID FOREIGN KEY (SystemID) REFERENCES dbo.HospitalSystem(SystemID),
    CONSTRAINT FK_Elig_Rush_LocationID FOREIGN KEY (LocationID) REFERENCES dbo.HospitalLocation(LocationID),
    CONSTRAINT FK_Elig_Rush_InsuranceTypeID FOREIGN KEY (InsuranceTypeID) REFERENCES dbo.InsuranceTypes(InsuranceTypeID)
);

-- Add any additional indices and constraints as necessary to match dbo.Elig_Rush
-- The following indexes are examples, add or remove based on your actual dbo.Elig_Rush indexes
CREATE INDEX IDX_Elig_Rush_SystemID ON dbo.Elig_Rush(SystemID);
CREATE INDEX IDX_Elig_Rush_LocationID ON dbo.Elig_Rush(LocationID);
CREATE INDEX IDX_Elig_Rush_InsuranceTypeID ON dbo.Elig_Rush(InsuranceTypeID);


CREATE TABLE dbo.Elig_UCMC (
    EligibilityID INT PRIMARY KEY IDENTITY(1,1),
    SystemID INT NOT NULL,
    LocationID INT NOT NULL,
    InsuranceTypeID INT NOT NULL,
    Carrier VARCHAR(255) NOT NULL,
    InNetwork BIT NOT NULL,
    EligibilityYear INT NOT NULL,
    PlanName VARCHAR(255) NOT NULL,
    CONSTRAINT FK_Elig_UCMC_SystemID FOREIGN KEY (SystemID) REFERENCES dbo.HospitalSystem(SystemID),
    CONSTRAINT FK_Elig_UCMC_LocationID FOREIGN KEY (LocationID) REFERENCES dbo.HospitalLocation(LocationID),
    CONSTRAINT FK_Elig_UCMC_InsuranceTypeID FOREIGN KEY (InsuranceTypeID) REFERENCES dbo.InsuranceTypes(InsuranceTypeID)
);

-- Add any additional indices and constraints as necessary to match dbo.Elig_UCMC
-- The following indexes are examples, add or remove based on your actual dbo.Elig_UCMC indexes
CREATE INDEX IDX_Elig_UCMC_SystemID ON dbo.Elig_UCMC(SystemID);
CREATE INDEX IDX_Elig_UCMC_LocationID ON dbo.Elig_UCMC(LocationID);
CREATE INDEX IDX_Elig_UCMC_InsuranceTypeID ON dbo.Elig_UCMC(InsuranceTypeID);










