use ChargeMasterDB ;
GO




CREATE TABLE dbo.CarrierType (
  CarrierTypeID INT IDENTITY(1,1) PRIMARY KEY,
  CarrierType NVARCHAR(255) NOT NULL
);

CREATE TABLE dbo.Carriers (
  CarrierID INT IDENTITY(1,1) PRIMARY KEY,
  CarrierName NVARCHAR(255) NOT NULL,
  CarrierTypeID INT FOREIGN KEY REFERENCES dbo.CarrierType(CarrierTypeID),
  CarrierAddress NVARCHAR(255)
);

CREATE TABLE [dbo].[InsurancePlans](
	[PlanID] [int] IDENTITY(1,1) NOT NULL,
	[CarrierID] [int] not Null FOREIGN KEY REFERENCES dbo.Carriers(CarrierID),
	[PlanName] [nvarchar](255) NOT NULL
) ON [PRIMARY]

-- Template for creating an Eligibility Table for a given HospitalSystem
-- Example: dbo.Eligibility_Advocate, dbo.Eligibility_Northwestern, etc.
CREATE TABLE dbo.Eligibility_Loyola (
  EligibilityID INT IDENTITY(1,1) PRIMARY KEY,
  LocationID INT FOREIGN KEY REFERENCES dbo.HospitalLocation(LocationID),
  PlanID INT FOREIGN KEY REFERENCES dbo.InsurancePlans(PlanID),
  InNetwork BIT NOT NULL,
  EligibilityYear INT NOT NULL
);
-- Template for creating an Eligibility Table for a given HospitalSystem
-- Example: dbo.Eligibility_Advocate, dbo.Eligibility_Northwestern, etc.
CREATE TABLE dbo.Eligibility_Northwestern( 
  EligibilityID INT IDENTITY(1,1) PRIMARY KEY,
  LocationID INT FOREIGN KEY REFERENCES dbo.HospitalLocation(LocationID),
  PlanID INT FOREIGN KEY REFERENCES dbo.InsurancePlans(PlanID),
  InNetwork BIT NOT NULL,
  EligibilityYear INT NOT NULL
);
-- Template for creating an Eligibility Table for a given HospitalSystem
-- Example: dbo.Eligibility_Advocate, dbo.Eligibility_Northwestern, etc.
CREATE TABLE dbo.Eligibility_Northshore  (
  EligibilityID INT IDENTITY(1,1) PRIMARY KEY,
  LocationID INT FOREIGN KEY REFERENCES dbo.HospitalLocation(LocationID),
  PlanID INT FOREIGN KEY REFERENCES dbo.InsurancePlans(PlanID),
  InNetwork BIT NOT NULL,
  EligibilityYear INT NOT NULL
);
-- Template for creating an Eligibility Table for a given HospitalSystem
-- Example: dbo.Eligibility_Advocate, dbo.Eligibility_Northwestern, etc.
CREATE TABLE dbo.Eligibility_Rush (
  EligibilityID INT IDENTITY(1,1) PRIMARY KEY,
  LocationID INT FOREIGN KEY REFERENCES dbo.HospitalLocation(LocationID),
  PlanID INT FOREIGN KEY REFERENCES dbo.InsurancePlans(PlanID),
  InNetwork BIT NOT NULL,
  EligibilityYear INT NOT NULL
);
-- Template for creating an Eligibility Table for a given HospitalSystem
-- Example: dbo.Eligibility_Advocate, dbo.Eligibility_Northwestern, etc.
CREATE TABLE dbo.Eligibility_UCMC(
  EligibilityID INT IDENTITY(1,1) PRIMARY KEY,
  LocationID INT FOREIGN KEY REFERENCES dbo.HospitalLocation(LocationID),
  PlanID INT FOREIGN KEY REFERENCES dbo.InsurancePlans(PlanID),
  InNetwork BIT NOT NULL,
  EligibilityYear INT NOT NULL
);

