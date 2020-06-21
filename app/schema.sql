DROP TABLE IF EXISTS user_table;
DROP TABLE IF EXISTS account_table;
DROP TABLE IF EXISTS video_table;
DROP TABLE IF EXISTS image_table;
DROP TABLE IF EXISTS caption_table;


CREATE TABLE user_table (
  userid VARCHAR(50) primary key,
  accountid VARCHAR(50) not null,
  username VARCHAR(50) not null,
  password VARCHAR(50) not null,
  salt VARCHAR(50) not null
);

create table account_table (
   account_id VARCHAR(50) primary key,
   history_id VARCHAR(50) not null,
   nickname VARCHAR(50) not null);

create table video_table (
  videoid VARCHAR(50) primary key AUTOINCREMENT,
  video_url VARCHAR(150) not null,
  video_filepath VARCHAR(150) not null,
  video_imagepath VARCHAR(150) not null
);

create table image_table(
 imageid VARCHAR(50) primary key AUTOINCREMENT,
 imagepath VARCHAR(150) not null,
 videoid VARCHAR(50) references video_table(videoid) on delete cascade on update cascade
);

create table caption_table(
 captionid VARCHAR(50) primary key AUTOINCREMENT,
 videoid VARCHAR(50) references video_table(videoid) on delete cascade on update cascade,
 content VARCHAR(100) not null,
 count INT not null check(count > 0),
 timestamp INT not null check(timestamp > 0)
);