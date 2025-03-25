CREATE TEMP TABLE ingredients_ingredient_staging (
    name TEXT,
    measurement_unit TEXT
);

COPY ingredients_ingredient_staging(name, measurement_unit) 
FROM '/data/ingredients.csv' 
DELIMITER ',' CSV QUOTE '"';

INSERT INTO ingredients_ingredient(name, measurement_unit)
SELECT name, measurement_unit
FROM ingredients_ingredient_staging
ON CONFLICT (name) DO NOTHING;
