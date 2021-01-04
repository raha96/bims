DROP TABLE IF EXISTS vials;

CREATE TABLE vials (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  serial TEXT NOT NULL,
  tissue TEXT NOT NULL,
  donner TEXT NOT NULL, 
  vialnum TEXT NOT NULL,
  passage TEXT NOT NULL, 
  date_yy TEXT NOT NULL, 
  date_mm TEXT NOT NULL,
  date_dd TEXT NOT NULL, 
  location TEXT NOT NULL, 
  injection TEXT
);
