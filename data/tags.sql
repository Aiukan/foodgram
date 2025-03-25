CREATE TEMP TABLE tags_tag_staging (
    name TEXT,
    slug TEXT
);

COPY tags_tag_staging(name, slug) 
FROM '/data/tags.csv' 
DELIMITER ',' CSV QUOTE '"';

INSERT INTO tags_tag(name, slug)
SELECT name, slug
FROM tags_tag_staging
ON CONFLICT (slug) DO NOTHING;
