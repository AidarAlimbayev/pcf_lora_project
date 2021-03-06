BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Processed_Data" (
	"ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"COW_ID"	TEXT NOT NULL,
	"WEIGHT"	NUMERIC NOT NULL,
	"TIMESTAMP"	NUMERIC NOT NULL
);
CREATE TABLE IF NOT EXISTS "Raw_Data" (
	"ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"COW_ID"	TEXT NOT NULL,
	"WEIGHT"	NUMERIC NOT NULL,
	"TIMESTAMP"	NUMERIC NOT NULL
);
CREATE TABLE IF NOT EXISTS "Cow" (
	"ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"rfidID"	TEXT NOT NULL,
	"SprayPeriod"	NUMERIC NOT NULL,
	"NextSprayTime"	NUMERIC NOT NULL,
	"LastDrinkDuration"	INTEGER NOT NULL
);
COMMIT;