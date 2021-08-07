-- Creation of post_stats table
CREATE TABLE IF NOT EXISTS post_stats (
  post_id varchar(250) NOT NULL,
  views INT NOT NULL,
  likes INT NOT NULL,
  comments INT NOT NULL,
  PRIMARY KEY (post_id)
);