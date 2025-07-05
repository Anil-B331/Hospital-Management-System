BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "appointments" (
	"ID"	INTEGER,
	"name"	TEXT,
	"age"	TEXT,
	"gender"	TEXT,
	"location"	TEXT,
	"phone"	INTEGER,
	"scheduled_time"	TEXT,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
INSERT INTO "appointments" VALUES (1,'Michael Scott','40','Male','Scranton',98989898,'1Pm');
INSERT INTO "appointments" VALUES (7,'Awais','23','Male','Layyah',923021111111,'10:40PM');
INSERT INTO "appointments" VALUES (8,'Awais','23','Male','Layyah',923021111111,'10:40PM');
COMMIT;
