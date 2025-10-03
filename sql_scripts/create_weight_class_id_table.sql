CREATE TABLE fighter_weight_class (
  id INTEGER NOT NULL,
  description TEXT NOT NULL
);

INSERT INTO fighter_weight_class (id, description)
VALUES
  (1, 'Heavyweight'),
  (2, 'Light Heavyweight'),
  (3, 'Middleweight'),
  (4, 'Welterweight'),
  (5, 'Lightweight'),
  (6, 'Featherweight'),
  (7, 'Bantamweight'),
  (8, 'Flyweight'),
  (9, 'Women''s Featherweight'),
  (10, 'Women''s Bantamweight'),
  (11, 'Women''s Flyweight'),
  (12, 'Women''s Strawweight');
