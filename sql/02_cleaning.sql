-- ============================================================
-- DATA CLEANING & TRANSFORMATION
-- ============================================================

-- Insert raw data (assumes CSV loaded via .import)
-- .mode csv
-- .import data/raw/Space_Corrected.csv raw_launches

-- Clean date parsing
UPDATE raw_launches SET datum = TRIM(REPLACE(REPLACE(datum, 'Mon ', ''), 'Tue ', ''));
UPDATE raw_launches SET datum = TRIM(REPLACE(REPLACE(datum, 'Wed ', ''), 'Thu ', ''));
UPDATE raw_launches SET datum = TRIM(REPLACE(REPLACE(datum, 'Fri ', ''), 'Sat ', ''));
UPDATE raw_launches SET datum = TRIM(REPLACE(datum, 'Sun ', ''));

-- Standardize organisation names
UPDATE raw_launches SET organisation = 'SpaceX' WHERE organisation LIKE '%SpaceX%';
UPDATE raw_launches SET organisation = 'CASC' WHERE organisation LIKE '%CASC%' OR organisation LIKE '%China%';
UPDATE raw_launches SET organisation = 'Roscosmos' WHERE organisation LIKE '%Roscosmos%' OR organisation LIKE '%Russian%';
UPDATE raw_launches SET organisation = 'ULA' WHERE organisation LIKE '%ULA%' OR organisation LIKE '%United Launch%';
UPDATE raw_launches SET organisation = 'Arianespace' WHERE organisation LIKE '%Arianespace%' OR organisation LIKE '%Arian%';
UPDATE raw_launches SET organisation = 'NASA' WHERE organisation LIKE '%NASA%' AND organisation NOT LIKE '%SpaceX%';
UPDATE raw_launches SET organisation = 'ISRO' WHERE organisation LIKE '%ISRO%' OR organisation LIKE '%India%';
UPDATE raw_launches SET organisation = 'JAXA' WHERE organisation LIKE '%JAXA%' OR organisation LIKE '%Japan%';
UPDATE raw_launches SET organisation = 'Rocket Lab' WHERE organisation LIKE '%Rocket Lab%';
UPDATE raw_launches SET organisation = 'Northrop' WHERE organisation LIKE '%Northrop%' OR organisation LIKE '%Orbital%';
UPDATE raw_launches SET organisation = 'Blue Origin' WHERE organisation LIKE '%Blue Origin%';
UPDATE raw_launches SET organisation = 'VKS RF' WHERE organisation LIKE '%VKS%' OR organisation LIKE '%Russian Space Forces%';
UPDATE raw_launches SET organisation = 'MHI' WHERE organisation LIKE '%MHI%' OR organisation LIKE '%Mitsubishi%';
